###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Entry point functions for nightly build operations.
"""
import json
import os
import pathlib
import socket
from multiprocessing import Pool
from pathlib import Path
from subprocess import STDOUT, check_output, run
from time import sleep

import archspec.cpu
from lb.nightly.configuration import (
    DataProject,
    Package,
    Project,
    get,
    lbnightly_settings,
    service_config,
)
from lb.nightly.db import connect as db
from lb.nightly.utils import Repository

from . import CMAKE_DIR
from .common import download_and_unzip, get_build_method


def checkout(project_id: str, worker_task_id: str, gitlab_token=None):
    from .checkout import git, notify_gitlab, update_nightly_git_archive

    conf = service_config()

    gitlab_token = (
        gitlab_token
        or conf.get("gitlab", {}).get("token")
        or os.environ.get("GITLAB_TOKEN")
    )

    project = get(project_id)
    if not isinstance(project, (Project, Package)):
        raise ValueError(
            f"project_id {project_id} does not identify a nightly builds Project instance"
        )

    db().checkout_start(project, worker_task_id)

    # checkout the project
    report = git(project)

    # record the working directory
    report.cwd = os.getcwd()

    if gitlab_token:
        if isinstance(project, DataProject):
            for pkg, pkg_report in zip(project.packages, report.packages):
                notify_gitlab(pkg, pkg_report, gitlab_token)
        else:
            report = notify_gitlab(project, report, gitlab_token)

    # gitlab archive and dependencies are not possible for data projects
    if not isinstance(project, (DataProject, Package)):
        try:
            report = update_nightly_git_archive(project, report)
        except Exception as err:
            report.warning(f"failed to update Git archive: {err}")

        # resolve and update dependencies
        db().set_dependencies(project)

    if isinstance(project, Package):
        dir_to_pack = os.path.join(
            project.container.name, project.name, project.version
        )
    else:
        dir_to_pack = project.name
    archive_name = os.path.basename(project.artifacts("checkout"))

    report.info(f"packing {dir_to_pack} into {archive_name}")
    report.log(
        "stdout",
        "debug",
        check_output(
            [
                "zip",
                "-r",
                archive_name,
                dir_to_pack,
            ],
            stderr=STDOUT,
        ).decode(),
    )

    report.info(f"adding logs to {archive_name}")

    log_dir = pathlib.Path(project.name) / ".logs" / "checkout"
    os.makedirs(log_dir)
    with open(log_dir / "report.json", "w") as f:
        json.dump(report.to_dict(), f, indent=2)
    with open(log_dir / "report.md", "w") as f:
        f.write(report.md())

    report.log(
        "stdout",
        "debug",
        check_output(
            ["zip", "-r", archive_name, log_dir],
            stderr=STDOUT,
        ).decode(),
    )

    if "artifacts" in conf:
        artifacts_repo = Repository.connect(conf["artifacts"]["uri"])
        assert artifacts_repo.push(
            open(archive_name, "rb"), project.artifacts("checkout")
        ), "failed to upload artifacts"
    else:
        report.warning("artifacts repository not configured: no publishing")

    if "logs" in conf:
        logs_repo = Repository.connect(conf["logs"]["uri"])
        assert logs_repo.push(
            open(log_dir / "report.json", "rb"),
            project.artifacts("checkout") + "-report.json",
        ), "failed to upload log"

    else:
        report.warning("logs repository not configured: no publishing")

    db().checkout_complete(project, report, worker_task_id)

    return report


def build(
    project_id: str,
    platform: str,
    worker_task_id: str,
    gitlab_token=None,
):

    conf = service_config()
    repo = Repository.connect()

    project = get(project_id)
    if not isinstance(project, Project):
        raise ValueError(
            f"project_id {project_id} does not identify a nightly builds Project instance"
        )

    db().build_start(project, platform, worker_task_id)

    project_sources_dir = project.get_deployment_directory()
    attempts = 0
    while attempts < 10:
        if project_sources_dir.exists():
            break
        sleep(300)
        attempts += 1
    else:
        raise RuntimeError(
            f"cannot find project sources directory {project_sources_dir}"
        )

    build_env = {}
    build_env["BINARY_TAG"] = build_env["CMTCONFIG"] = platform
    build_env["PATH"] = os.environ["PATH"]
    build_env["LBENV_CURRENT_WORKSPACE"] = str(project.slot.get_deployment_directory())
    build_env[
        "CMAKE_PREFIX_PATH"
    ] = f"{build_env['LBENV_CURRENT_WORKSPACE']}:/cvmfs/lhcb.cern.ch/lib/lhcb:/cvmfs/lhcb.cern.ch/lib/lcg/releases:{CMAKE_DIR}:/cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/vtune_amplifier"

    if "TASK_LOGFILE" in os.environ:
        build_env["TASK_LOGFILE"] = os.environ["TASK_LOGFILE"]
    if "CONDA_ENV" in os.environ:
        build_env["CONDA_ENV"] = os.environ["CONDA_ENV"]
    build_env["NIGHTLIES_CACHE"] = lbnightly_settings().installations.path
    if "CMAKE_USE_CCACHE" not in project.slot.cache_entries:
        project.slot.cache_entries["CMAKE_USE_CCACHE"] = True

    report, build_logs = get_build_method(project)(project).build(
        jobs=int(os.environ.get("LBN_BUILD_JOBS") or "0") or os.cpu_count() or 1,
        init_env=build_env,
        worker_task_id=worker_task_id,
        cache_entries=project.slot.cache_entries,
    )
    archive_name = os.path.basename(project.artifacts("build", platform))
    report["script"].info(f"packing {project.name} into {archive_name}")
    report["script"].log(
        "stdout",
        "debug",
        check_output(
            [
                "zip",
                "-r",
                archive_name,
                project.name,
                "-i",
                f"{project.name}/build/*",
                f"{project.name}/InstallArea/*",
            ],
            stderr=STDOUT,
        ).decode(),
    )

    report["script"].info(f"adding logs to {archive_name}")

    log_dir = pathlib.Path(project.name) / ".logs" / platform / "build"
    os.makedirs(log_dir, exist_ok=True)
    with open(log_dir / "report.md", "w") as f:
        for step in report.values():
            f.write(step.md())
            f.write("\n")

    jreport = {}
    from .build_log import generate_build_report

    try:
        completed = report["install"].completed
    except AttributeError:
        try:
            completed = report["build"].completed
        except AttributeError:
            completed = report["configure"].completed
    retcodes = set()
    for rep in report.values():
        try:
            retcodes.add(rep.returncode)
        except AttributeError:
            pass

    reports_json = {k: v.to_dict() for k, v in report.items()}
    for val in reports_json.values():
        try:
            val["stdout"] = val["stdout"].decode(errors="surrogateescape")
            val["stderr"] = val["stderr"].decode(errors="surrogateescape")
        except KeyError:
            pass

    jreport = generate_build_report(
        build_logs=build_logs,
        proj_build_root=project.name,
        exceptions={
            "warning": project.slot.warning_exceptions,
            "error": project.slot.error_exceptions,
        },
        extra_info={
            "project": project.name,
            "version": project.version,
            "slot": project.slot.name,
            "slot_build_id": project.slot.build_id,
            "host": socket.gethostname(),
            "platform": platform,
            "started": report["configure"].started,
            "completed": completed,
            "retcode": max(retcodes),
            "environment": build_env,
            "cpu": archspec.cpu.detect.raw_info_dictionary(),
            "reports": reports_json,
        },
    )

    with open(log_dir / "report.json", "w") as f:
        json.dump(jreport, f, indent=2)

    report["script"].log(
        "stdout",
        "debug",
        check_output(["zip", "-r", archive_name, log_dir], stderr=STDOUT).decode(),
    )

    assert repo.push(
        open(archive_name, "rb"), project.artifacts("build", platform)
    ), "failed to upload artifacts"

    if "logs" in conf:
        logs_repo = Repository.connect(conf["logs"]["uri"])
        assert logs_repo.push(
            open(log_dir / "report.json", "rb"),
            project.artifacts("build", platform) + "-report.json",
        ), "failed to upload log"

    else:
        report["script"].warning("logs repository not configured: no publishing")

    db().build_complete(project, platform, jreport, worker_task_id)

    return report


def test(
    project_id: str,
    platform: str,
    worker_task_id: str = None,
    gitlab_token=None,
):

    conf = service_config()
    repo = Repository.connect()

    project = get(project_id)
    if not isinstance(project, Project):
        raise ValueError(
            f"project_id {project_id} does not identify a nightly builds "
            "Project instance"
        )

    db().tests_start(project, platform, worker_task_id)

    download_and_unzip(repo, project.artifacts("build", platform))

    build_env = {}
    build_env["BINARY_TAG"] = build_env["CMTCONFIG"] = platform
    build_env["PATH"] = os.environ["PATH"]
    build_env["LBENV_CURRENT_WORKSPACE"] = str(project.slot.get_deployment_directory())
    build_env[
        "CMAKE_PREFIX_PATH"
    ] = f"{build_env['LBENV_CURRENT_WORKSPACE']}:/cvmfs/lhcb.cern.ch/lib/lhcb:/cvmfs/lhcb.cern.ch/lib/lcg/releases:{CMAKE_DIR}:/cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/vtune_amplifier"
    if "TASK_LOGFILE" in os.environ:
        build_env["TASK_LOGFILE"] = os.environ["TASK_LOGFILE"]
    if "CONDA_ENV" in os.environ:
        build_env["CONDA_ENV"] = os.environ["CONDA_ENV"]
    build_env["NIGHTLIES_CACHE"] = lbnightly_settings().installations.path

    try:
        krb_auth = (
            lbnightly_settings()["kerberos"]["user"],
            lbnightly_settings()["kerberos"]["password"],
        )
    except KeyError:
        krb_auth = None

    try:
        os.remove(os.path.join(project.name, "build", "CMakeCache.txt"))
    except (OSError, FileNotFoundError):
        pass

    report = get_build_method(project)(project).test(
        init_env=build_env,
        krb_auth=krb_auth,
        worker_task_id=worker_task_id,
    )

    reports = {"report": report, "results": {}}

    from xml.etree import ElementTree as ET

    try:
        xml = ET.parse(next(pathlib.Path(".").glob("**/Test.xml")))
        status_translation = {
            "passed": "PASS",
            "failed": "FAIL",
            "skipped": "SKIPPED",
            "notrun": "SKIPPED",
            "error": "ERROR",
            "untested": "UNTESTED",
        }
        from itertools import groupby

        tests = sorted(
            xml.findall("./Testing/Test[@Status]"),
            key=lambda test: test.attrib["Status"],
        )
        summary = {
            status_translation[key]: sorted(test.find("Name").text for test in group)
            for key, group in groupby(tests, key=lambda test: test.attrib["Status"])
        }
        reports["results"] = summary
    except StopIteration:
        report["script"].error("failed to parse Test.xml (file is missing)")

    archive_name = os.path.basename(project.artifacts("test", platform))
    report["script"].info(f"packing {project.name} into {archive_name}")
    report["script"].info(f"adding logs to {archive_name}")

    log_dir = pathlib.Path(project.name) / ".logs" / platform / "test"
    os.makedirs(log_dir, exist_ok=True)
    for step in report.keys():
        with open(log_dir / "report.md", "a") as f:
            f.write(f"{report[step].md()}\n")

    reports_json = {k: v.to_dict() for k, v in report.items()}
    for val in reports_json.values():
        try:
            val["stdout"] = val["stdout"].decode(errors="surrogateescape")
            val["stderr"] = val["stderr"].decode(errors="surrogateescape")
        except KeyError:
            pass

    with open(log_dir / "report.json", "w") as f:
        json.dump(reports_json, f, indent=2)

    report["script"].log(
        "stdout",
        "debug",
        check_output(
            [
                "zip",
                "-r",
                archive_name,
                log_dir,
            ],
            stderr=STDOUT,
        ).decode(),
    )

    assert repo.push(
        open(archive_name, "rb"), project.artifacts("test", platform)
    ), "failed to upload artifacts"

    if "logs" in conf:
        logs_repo = Repository.connect(conf["logs"]["uri"])
        assert logs_repo.push(
            open(log_dir / "report.json", "rb"),
            project.artifacts("test", platform) + "-report.json",
        ), "failed to upload log"
        try:
            with open(f"{project.name}/build/Testing/TAG") as tagfile:
                assert logs_repo.push(
                    open(
                        f"{project.name}/build/Testing/{tagfile.readline().strip()}/Test.xml",
                        "rb",
                    ),
                    project.artifacts("build", platform) + "-Test.xml",
                ), "failed to upload Test.xml (pushing to repo failed)"
        except FileNotFoundError:
            report["script"].error("failed to upload Test.xml (file is missing)")

    else:
        report["script"].warning("logs repository not configured: no publishing")

    db().tests_complete(project, platform, reports, worker_task_id)

    return report


if __name__ == "__main__":  # pragma: no cover
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG)
    globals()[sys.argv[1]](*sys.argv[2:])
