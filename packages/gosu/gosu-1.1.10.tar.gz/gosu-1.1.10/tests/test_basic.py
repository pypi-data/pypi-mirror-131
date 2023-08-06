import os

from gosu.cmds.ci import get_version, git_num_changes
from gosu.cmds.python import (
    _get_editable_installs,
    _get_pkg_pyfiles,
    _manage_env_vars,
    env_from_sourcing,
)


def test_get_env_from_sourcing():
    e = env_from_sourcing(".venv/bin/activate")
    assert "PWD" in e


def test_get_env_vars():
    os.chdir("tests")
    e = _manage_env_vars()
    assert e["test"] == "1"


def test_get_pkg_pyfiles():
    e = _get_pkg_pyfiles()
    assert len(e) > 0


def test_get_version():
    assert get_version() != ""


def test_git_num_changes():
    assert git_num_changes() != ""


def test_get_editable_installs():
    assert _get_editable_installs("pyproject.toml")["something"] == "../something"
