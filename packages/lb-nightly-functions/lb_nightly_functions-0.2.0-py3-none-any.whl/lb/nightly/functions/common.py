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
import asyncio
import json
import logging
import os
import socket
from collections import namedtuple
from contextlib import redirect_stderr
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from shutil import copyfileobj
from ssl import create_default_context
from subprocess import CalledProcessError, run
from tempfile import NamedTemporaryFile
from typing import Optional, Union
from zlib import decompress

from git import GitCommandError
from lb.nightly.configuration import DataProject, Package, Project

from . import DATA_DIR


class Report:
    """
    Class used to collect reports.

    Record messages and forward them to a logger.

    Apart from normal logging levels, accept extra type of messages, like
    ``git_error``.
    """

    def __init__(self, logger=__name__):
        self.logger = logging.getLogger(logger)
        self.records = []

    def log(self, type, level, fmt, args=None):
        record = {"type": type, "level": level, "text": (fmt % args if args else fmt)}
        if type in ("error", "warning") and f"{type}:" not in record["text"]:
            record["text"] = "{}: {}".format(type, record["text"])
        self.records.append(record)
        getattr(self.logger, level)(fmt, *(() if args is None else args))

    def debug(self, fmt, *args):
        self.log("debug", "debug", fmt, args)

    def info(self, fmt, *args):
        self.log("info", "info", fmt, args)

    def warning(self, fmt, *args):
        self.log("warning", "warning", fmt, args)

    warn = warning

    def error(self, fmt, *args):
        self.log("error", "error", fmt, args)

    def git_error(self, msg, err: GitCommandError):
        """
        Special handling for GitCommandError
        """
        self.warning("%s: GitCommand status %s", msg, err.status)
        # FIXME: this is very much subject to the internal details of GitCommandError
        self.log("command", "debug", "> %s", (err._cmdline,))
        if "'" in err.stdout:
            self.log(
                "stdout", "debug", err.stdout[err.stdout.index("'") + 1 : -1].rstrip()
            )
        if "'" in err.stderr:
            self.log(
                "stderr", "debug", err.stderr[err.stderr.index("'") + 1 : -1].rstrip()
            )

    def md(self):
        """
        Format as markdown.
        """
        out = []
        if hasattr(self, "project"):
            out.append("# {name}/{version}".format(**self.project))
        for r in self.records:
            lines = r["text"].splitlines()
            if r["type"] in ("stdout", "stderr", "command"):
                out.append("  ```")
                out.extend("  " + l for l in lines)
                out.append("  ```")
            else:
                out.append("- " + lines.pop(0))
                out.extend("  " + l for l in lines)
        if hasattr(self, "packages"):
            out.extend(pkg.md() for pkg in self.packages)
        return "\n".join(out)

    def __str__(self):
        out = []
        if hasattr(self, "project"):
            out.append("{name}/{version}".format(**self.project))
            out.append("-" * len(out[-1]))
            out.append("")
        out.extend(r["text"] for r in self.records)
        if hasattr(self, "packages"):
            out.extend(str(pkg) for pkg in self.packages)
        return "\n".join(out)

    def to_dict(self):
        from copy import deepcopy

        data = deepcopy(self.__dict__)
        data["logger"] = self.logger.name
        if "packages" in data:
            data["packages"] = [pkg.to_dict() for pkg in data["packages"]]

        return data


def ensure_dir(path, rep: Report):
    """
    Make sure that a directory exist, creating it
    and passing a warning to Report object if dir does not exist.
    """
    if not os.path.exists(path):
        rep.warning(f"directory {path} is missing, I create it")
        os.makedirs(path)


def find_path(name, search_path=None):
    """
    Look for a file or directory in a search path.

    If the search path is not specified, the concatenation of CMTPROJECTPATH
    and CMAKE_PREFIX_PATH is used.

    >>> find_path('true', ['/usr/local/bin', '/bin'])
    '/bin/true'
    >>> print(find_path('cannot_find_me', []))
    None
    """
    from os import environ, pathsep
    from os.path import exists, join

    if search_path is None:
        search_path = environ.get("CMAKE_PREFIX_PATH", "").split(pathsep) + environ.get(
            "CMTPROJECTPATH", ""
        ).split(pathsep)

    try:
        return next(
            join(path, name) for path in search_path if exists(join(path, name))
        )
    except StopIteration:
        logging.warning("%s not found in %r", name, search_path)
    return None


def get_build_method(project=None):
    """
    Helper function to get a build method for a project.

    The method is looked up in the following order: build_tool property of a project,
    build_tool property of a slot owning the project, the default build method (cmake).

    If a method is retrieved via build_tool string property, it must be defined in
    lb.nightly.functions.build.
    """
    import lb.nightly.functions.build as build_methods

    try:
        method = project.build_tool or project.slot.build_tool
        return getattr(build_methods, method)
    except (AttributeError, TypeError):
        return build_methods.cmake


def safe_dict(mydict):
    """Helper to return the dictionary without sensitive data
    To be used e.g. to remove secret environment variables.
    >>> d={"PASSWORD": "my_secret_pass", "PASS": "asd", "USER": "me", "KEY": "asd", "TOKEN": "asd", "PRIVATE": "Asd", "HOME": "Asd", "SHA": "asd"}
    >>> safe_dict(d)
    {}
    """
    return {
        k: v
        for k, v in mydict.items()
        if all(
            s not in k.upper()
            for s in [
                "PASS",
                "USER",
                "KEY",
                "TOKEN",
                "PRIVATE",
                "HOME",
                "SHA",
            ]
        )
    }


def singularity_run(
    cmd: list,
    env: Optional[dict] = None,
    cwd: str = os.curdir,
    task: Optional[dict] = None,
    krb_auth: Optional[tuple] = None,
):
    from spython.main import Client

    try:
        Client.load(get_singularity_root(binary_tag=env["BINARY_TAG"]))
    except AttributeError:
        raise RuntimeError(
            f"Could not find the CernVM image for the "
            f"{env.get('BINARY_TAG', 'not specified BINARY_TAG')}"
        )

    s_env = safe_dict(env)

    # specify workspace in container
    workspace_singularity = pwd = "/workspace"
    if cwd != os.getcwd():
        cwd = os.path.join(workspace_singularity, cwd)
        pwd = cwd

    if krb_auth:
        krb_token = NamedTemporaryFile()
        s_env["KRB5CCNAME"] = f"FILE:{krb_token.name}"

        class KerberosAuthenticationError(Exception):
            pass

        try:
            run(
                ["kinit", "-c", krb_token.name, krb_auth[0]],
                input=krb_auth[1].encode(),
                check=True,
            )
        except (CalledProcessError, IndexError):
            raise KerberosAuthenticationError(
                "Could not authenticate with provided credentials"
            )

    # setting up opensearch where we send logs from singularity
    from lb.nightly.configuration import service_config
    from opensearchpy import OpenSearch

    conf = service_config()
    es_url = conf.get("opensearch", {}).get("uri", "dummy_opensearch_uri")
    capath = conf.get("opensearch", {}).get("capath")
    index_pattern_prefix = conf.get("opensearch", {}).get(
        "index_pattern_prefix",
        "nightlies",
    )
    opensearch = OpenSearch(
        [es_url],
        ssl_context=create_default_context(capath=capath),
    )
    logging.getLogger("opensearch").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    if opensearch.ping():
        # stub of the msg to send to opensearch
        log_body = {
            "host": socket.gethostname(),
            "command": cmd,
            "cwd": cwd,
            "task": task.get("task"),
            "project": task.get("project"),
            "platform": task.get("platform"),
            "worker_task_id": task.get("worker_task_id"),
            "log": None,  # will be overriden just before sending
            "timestamp": None,  # same as above
        }
        log_body.update(
            {
                "log": f"Running command: {cmd} with env: {s_env}",
                "timestamp": datetime.now(timezone.utc),
            }
        )
        opensearch.index(
            index=f"{index_pattern_prefix}-{datetime.now(timezone.utc).strftime('%Y.%m.%d')}-{task.get('task', 'nightlies')}",
            body=log_body,
        )

    if "TASK_LOGFILE" in env:
        with open(env.get("TASK_LOGFILE"), "a") as logfile:
            logfile.write(
                f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}: "
                f"Running command: {cmd} with {s_env}\n"
            )

    # to collect the build messages we communicate through the UNIX socket
    from hashlib import sha256

    hash = sha256()
    hash.update(f"{cmd} {task} {cwd}".encode())
    os.environ["LB_WRAPCMD_SOCKET"] = s_env["LB_WRAPCMD_SOCKET"] = os.path.join(
        "/tmp", hash.hexdigest()[:32]
    )

    Result = namedtuple(
        "Result",
        [
            "returncode",
            "stdout",
            "stderr",
            "args",
            "build_logs",
        ],
    )

    try:
        result = Client.execute(
            cmd,
            bind=[
                "/cvmfs",
                env.get(
                    "CONDA_ENV"
                ),  # safe because spython ignores "false" values in the list
                env.get("NIGHTLIES_CACHE"),
                f"{os.getcwd()}:{workspace_singularity}",
            ],
            options=[f"--pwd={pwd}", "--cleanenv"]
            + [f"--env={k}={v}" for k, v in s_env.items()],
            stream=True,
        )

        stdout = b""
        build_logs = {}

        async def get_stdout(result):
            nonlocal stdout
            for line in result:
                stdout += line.encode(errors="surrogateescape")
                yield line
                await asyncio.sleep(0)

        async def log_to_file(result):
            with open(
                os.environ.get("TASK_LOGFILE"),
                "a",
                buffering=512,
            ) as logfile:
                async for line in result:
                    logfile.write(
                        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}: "
                        f"{line.rstrip()}\n"
                    )
                    yield line
                    await asyncio.sleep(0)

        async def log_to_opensearch(result):
            async for line in result:
                yield dict(
                    log_body,
                    **{
                        "_index": f"{index_pattern_prefix}-{datetime.now(timezone.utc).strftime('%Y.%m.%d')}-{task.get('task', 'nightlies')}",
                        "log": line.rstrip(),
                        "timestamp": datetime.now(timezone.utc),
                    },
                )
                await asyncio.sleep(0)

        from opensearchpy import AsyncOpenSearch
        from opensearchpy.helpers import async_streaming_bulk

        aopensearch = AsyncOpenSearch(
            hosts=[es_url],
            ssl_context=create_default_context(capath=capath),
        )

        async def stream_to_opensearch(result):
            async for _ in async_streaming_bulk(
                aopensearch,
                result,
                chunk_size=100,
                raise_on_exception=False,
                raise_on_error=False,
            ):
                await asyncio.sleep(0)

        async def stream_to_file(result):
            async for _ in log_to_file(result):
                await asyncio.sleep(0)

        if "TASK_LOGFILE" in env:

            async def get_output_and_log(result):
                if opensearch.ping():
                    await stream_to_opensearch(
                        log_to_opensearch(log_to_file(get_stdout(result)))
                    )
                else:
                    await stream_to_file(get_stdout(result))

        else:

            async def get_output_and_log(result):
                if opensearch.ping():
                    await stream_to_opensearch(log_to_opensearch(get_stdout(result)))
                else:
                    async for _ in get_stdout(result):
                        await asyncio.sleep(0)

        async def read_from_singularity(result):
            nonlocal stdout
            await get_output_and_log(result)
            return stdout

        server_address = os.environ["LB_WRAPCMD_SOCKET"]
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        async def _receive(reader, writer):
            buffer = b""
            while True:
                msg = await reader.read(4096)
                if msg:
                    buffer += msg
                else:
                    break
            data = json.loads(decompress(buffer))
            build_logs.setdefault(data.pop("subdir"), {}).setdefault(
                data.pop("target"), []
            ).append(data)

        async def read_socket(server_address):
            server = await asyncio.start_unix_server(
                _receive,
                server_address,
            )
            async with server:
                try:
                    await server.serve_forever()
                except asyncio.exceptions.CancelledError:
                    pass

        async def main_get_read(result, server_address):
            nonlocal stdout
            asyncio.create_task(read_socket(server_address))
            task = asyncio.create_task(read_from_singularity(result))
            try:
                await task
            except asyncio.exceptions.CancelledError:
                pass
            return stdout

        with redirect_stderr(StringIO()) as singularity_stderr:
            stdout = asyncio.run(main_get_read(result, server_address))

        # will be overwritten if CalledProcessError is raised
        retcode = 0

    except CalledProcessError as cpe:
        retcode = cpe.returncode
    finally:
        try:
            os.unlink(server_address)
        except OSError:
            pass
        try:
            del os.environ["LB_WRAPCMD_SOCKET"]
        except KeyError:
            pass
        try:
            krb_token.close()
        except NameError:
            pass
    return Result(
        stdout=stdout,
        returncode=retcode,
        stderr=singularity_stderr.getvalue().encode(errors="surrogateescape"),
        args=cmd,
        build_logs=build_logs,
    )


async def write_to_socket(socket_name, message):
    _, writer = await asyncio.open_unix_connection(socket_name)
    writer.write(message)
    writer.close()


def lb_wrapcmd():
    """
    The script to be used in CMake launcher rules.

    A launcher rule defined as
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "lb-wrapcmd <CMAKE_CURRENT_BINARY_DIR> <TARGET_NAME>")

    Output for each compile command is sent to the socket
    (name taken from LB_WRAPCMD_SOCKET env variable or built as:
    <CMAKE_CURRENT_BINARY_DIR>/1234-<TARGET_NAME>-abc-build.log)
    """
    import sys
    from argparse import REMAINDER, ArgumentParser
    from shutil import which
    from time import time
    from zlib import compress

    parser = ArgumentParser()
    parser.add_argument("log_dir", help="CMAKE_CURRENT_BINARY_DIR")
    parser.add_argument("target", help="TARGET_NAME")
    parser.add_argument("wrap_cmd", nargs=REMAINDER, help="wrapped command")
    args = parser.parse_args()

    with NamedTemporaryFile() as statistics_file:
        time_cmd = [
            which("time"),
            "-f",
            '{"duration": "%E", "maxresident": "%M", "avgresident": "%t", "cpupercentage": "%P"}',
            "-o",
            statistics_file.name,
        ]
        started = time()
        result = run(time_cmd + args.wrap_cmd, capture_output=True)
        completed = time()
        sys.stdout.buffer.write(result.stdout)
        sys.stderr.buffer.write(result.stderr)

        if "LB_WRAPCMD_SOCKET" in os.environ:
            server_address = os.environ["LB_WRAPCMD_SOCKET"]

            output = {
                "subdir": "/".join(args.log_dir.split("/")[4:]),
                "target": args.target,
                "cmd": args.wrap_cmd,
                "stdout": "",
                "stderr": "",
                "returncode": result.returncode,
                "started": started,
                "completed": completed,
            }
            statistics_file.seek(0)
            with open(statistics_file.name, "r") as f:
                statistics = json.loads(f.read())
            output.update(statistics)

            if args.wrap_cmd[0] != "cat":
                output["stdout"] = result.stdout.decode(errors="surrogateescape")
                output["stderr"] = result.stderr.decode(errors="surrogateescape")

            asyncio.run(
                write_to_socket(server_address, compress(json.dumps(output).encode()))
            )

    return result.returncode


def download_and_unzip(repo, artifact):
    """
    Helper function to download the artifact
    and unzip it in the current directory.

    :param repo: ArtifactsRepository object to get the artifact from
    :param artifact: the value returned by the `artifacts`
    method of the Project.

    Returns True if succeded.
    """
    try:
        with NamedTemporaryFile() as lp:
            with repo.pull(artifact) as remote:
                copyfileobj(remote, lp)
            lp.seek(0)
            return not run(["unzip", "-o", lp.name], check=True).returncode
    except Exception:
        return False


def create_project_makefile(dest, overwrite=False):
    """Write the generic Makefile for CMT projects.
    @param dest: the name of the destination file
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        with open(dest, "w") as f:
            f.write(
                "DEVTOOLS_DATADIR := {0}\n"
                "include $(DEVTOOLS_DATADIR)/Makefile-common.mk\n".format(DATA_DIR)
            )
        return True
    return False


def create_toolchain_file(dest, overwrite=False):
    """Write the generic toolchain.cmake file needed by CMake-based projects.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        with open(dest, "w") as f:
            f.write("include({0})\n".format(os.path.join(DATA_DIR, "toolchain.cmake")))
        return True
    return False


def create_git_ignore(dest, overwrite=False, extra=None, selfignore=True):
    """Write a generic .gitignore file, useful for git repositories.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    @param extra: list of extra patterns to add
    @param selfignore: if the .gitignore should include itself
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        patterns = [
            "/InstallArea/",
            "/build.*/",
            "*.pyc",
            "*~",
            ".*.swp",
            "/.clang-format",
        ]
        if selfignore:
            patterns.insert(0, "/.gitignore")  # I like it as first entry
        if extra:
            patterns.extend(extra)

        with open(dest, "w") as f:
            f.write("\n".join(patterns))
            f.write("\n")
        return True
    return False


def create_clang_format(dest, overwrite=False):
    """Add `.clang-format` file.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        with open(dest, "w") as f:
            f.writelines(open(os.path.join(DATA_DIR, "default.clang-format")))
        return True
    return False


def init_project(path, overwrite=False):
    """
    Initialize the sources for an LHCb project for building.

    Create the (generic) special files required for building LHCb/Gaudi
    projects.

    @param path: path to the root directory of the project
    @param overwrite: whether existing files should be overwritten, set it to
                      True to overwrite all of them or to a list of filenames
    """
    extraignore = []
    factories = [
        ("Makefile", create_project_makefile),
        ("toolchain.cmake", create_toolchain_file),
        (
            ".gitignore",
            lambda dest, overwrite: create_git_ignore(dest, overwrite, extraignore),
        ),
        (".clang-format", create_clang_format),
    ]

    # handle the possible values of overwrite to always have a set of names
    if overwrite in (False, None):
        overwrite = set()
    elif overwrite is True:
        overwrite = set(f[0] for f in factories)
    elif isinstance(overwrite, str):
        overwrite = set([overwrite])
    else:
        overwrite = set(overwrite)

    for filename, factory in factories:
        if factory(os.path.join(path, filename), overwrite=filename in overwrite):
            extraignore.append("/" + filename)


def get_singularity_root(binary_tag: str):
    """
    >>> get_singularity_root("x86_64-centos7-gcc9-opt")
    '/cvmfs/cernvm-prod.cern.ch/cvm4'
    >>> get_singularity_root("x86_64-slc6-gcc9-opt")
    '/cvmfs/cernvm-prod.cern.ch/cvm3'
    >>> get_singularity_root("x86_64-slc5-gcc9-opt")
    '/cvmfs/cernvm-prod.cern.ch/cvm3'
    >>> get_singularity_root("x86_64-ubuntu-gcc9-opt")
    >>>
    """
    from LbPlatformUtils import OS_ALIASES, OS_COMPATIBILITY
    from LbPlatformUtils.inspect import SINGULARITY_ROOTS

    wanted_os = binary_tag.split("-")[1]
    compatible_oss = [wanted_os] + [
        main_os
        for main_os, comp_oss in OS_COMPATIBILITY.items()
        if wanted_os in comp_oss
    ]
    try:
        compatible_aliases = [
            comp_os
            for compatible_os in compatible_oss
            for comp_os in OS_ALIASES[compatible_os]
        ]
        return [path for path, osid in SINGULARITY_ROOTS if osid in compatible_aliases][
            0
        ]
    except (IndexError, KeyError):
        return None
