import os
import re
import subprocess
from enum import Enum

import semver
import toml
import typer
from plumbum import FG, ProcessExecutionError
from plumbum import local as lr

app = typer.Typer()


def git(*args, output=True):
    r = subprocess.check_output(["git"] + list(args))
    if output:
        print(args)  # noqa
        print(r)  # noqa
    return r


def git_num_changes():
    return len(git("status", "--porcelain").splitlines())


def _get_version():
    return git("describe", "--tags").decode().strip()


@app.command()
def push_repo():
    git(
        "remote",
        "set-url",
        "--push",
        "origin",
        re.sub(r".+@([^/]+)/", r"git@\1:", os.environ["CI_REPOSITORY_URL"]),
    )
    git("push", "-o", "ci.skip", "origin", get_version())


class SemverPart(str, Enum):
    patch = "patch"
    minor = "minor"
    major = "major"


@app.command()
def bump_version(semver_part: SemverPart = SemverPart.patch):
    git("fetch", "--tags", "-f")
    git("tag")
    try:
        v = _get_version()
        if semver_part.value == SemverPart.patch:
            n = semver.bump_patch(v)
        elif semver_part.value == SemverPart.minor:
            n = semver.bump_minor(v)
        elif semver_part.value == SemverPart.major:
            n = semver.bump_major(v)
    except (subprocess.CalledProcessError, ValueError):
        print("initialise versioning with 1.0.0")  # noqa
        git("tag", "1.0.0")
        return

    if "-" not in v:
        return

    print(f"bump from {v} to {n}")  # noqa
    data = toml.load("pyproject.toml")
    data["project"]["version"] = n
    with open("pyproject.toml", "w") as f:
        toml.dump(data, f)
    git("add", ".")
    git("commit", "--allow-empty", "-m", f"bump version to {n}")
    git("tag", "-a", n, "-m", f"release {n}")
    git("push", "--follow-tags")


@app.command()
def get_version():
    print(f"current version: {_get_version()}")  # noqa


@app.command()
def local():
    has_changes = git_num_changes() > 0
    try:
        if has_changes:
            git("add", ".")
            git("commit", "-m", "local debug commit")
        (
            lr["gitlab-ci-local"][
                "--privileged",
            ]
            & FG
        )
    except ProcessExecutionError:
        exit(1)
    finally:
        if has_changes:
            git("reset", "HEAD~1")
