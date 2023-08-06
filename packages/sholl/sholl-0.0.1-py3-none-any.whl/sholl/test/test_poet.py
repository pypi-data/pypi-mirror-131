# Integration tests for sholl

import subprocess
import sys


def sholl(*args):
    return subprocess.check_output(
        ["sholl"] + list(args),
        stderr=subprocess.STDOUT)


def test_version():
    assert b"sholl" in sholl("-V")


def test_single():
    result = sholl("-s", "nose", "six")
    assert b'resource "nose"' in result
    assert b'resource "six"' in result


def test_formula():
    result = sholl("-f", "pytest")
    assert b'resource "py" do' in result
    if sys.version_info.major == 2:
        assert b'depends_on "python"' in result
    else:
        assert b'depends_on "python3"' in result


def test_case_sensitivity():
    sholl("-f", "FoBiS.py")


def test_resources():
    result = sholl("pytest")
    assert b'resource "py" do' in result
    result = sholl("py.test")
    assert b'PackageNotInstalledWarning' in result


def test_uses_sha256_from_json(monkeypatch):
    monkeypatch.setenv("sholl_DEBUG", 10)
    result = sholl("pytest")
    assert b"Using provided checksum for py\n" in result


def test_audit(tmpdir):
    home = tmpdir.chdir()
    try:
        with open("pytest.rb", "wb") as f:
            subprocess.check_call(["sholl", "-f", "pytest"], stdout=f)
        subprocess.check_call(["brew", "audit", "--strict", "./pytest.rb"])
    finally:
        tmpdir.join("pytest.rb").remove(ignore_errors=True)
        home.chdir()


def test_lint(tmpdir):
    home = tmpdir.chdir()
    try:
        with open("pytest.rb", "wb") as f:
            subprocess.check_call(["sholl", "-f", "pytest"], stdout=f)
        subprocess.check_call(["sholl_lint", "pytest.rb"])
    finally:
        tmpdir.join("pytest.rb").remove(ignore_errors=True)
        home.chdir()


def test_camel_case():
    result = sholl("-f", "magic-wormhole")
    assert b"class MagicWormhole < Formula" in result
