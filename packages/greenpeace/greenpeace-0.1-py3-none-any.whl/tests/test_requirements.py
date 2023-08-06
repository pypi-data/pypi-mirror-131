from typing import Dict, List
import greenpeace as gp
import os


def __get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "files", name)


def __check_package(packages: Dict[str, Dict[str, str]], name, specifier, version):
    assert name in packages
    assert packages[name]["specifier"] == specifier
    assert packages[name]["version"] == version


def test_read_requirements():
    packages = gp.read_requirements(__get_file("requirements.txt"))

    # Requirements without Version Specifiers
    __check_package(packages, "pytest", specifier=None, version=None)
    __check_package(packages, "pytest-cov", specifier=None, version=None)
    __check_package(packages, "beautifulsoup4", specifier=None, version=None)

    # Requirements with Version Specifiers
    __check_package(packages, "docopt", specifier="==", version="0.6.1")
    __check_package(packages, "keyring", specifier=">=", version="4.1.1")
    __check_package(packages, "coverage", specifier="!=", version="3.5")
    __check_package(packages, "Mopidy-Dirble", specifier="~=", version="1.1")
    __check_package(
        packages,
        "pythonnet",
        specifier="@",
        version="git+https://github.com/pythonnet/pythonnet@09ecf1b22b9d51691c3da96eb70bf9a615bddb43",
    )
    __check_package(packages, "numpy", specifier=">", version="1.20.0")
    __check_package(packages, "treebuilder", specifier="===", version="1.20.0")
    __check_package(packages, "yarg", specifier="<", version="1.0.0")
    __check_package(packages, "requests", specifier="<=", version="2.0.0")

    # Refer to other requirements files
    __check_package(packages, "other-requirements.txt", specifier="-r", version=None)

    # A particular file
    __check_package(
        packages,
        "./downloads/numpy-1.9.2-cp34-none-win32.whl",
        specifier=None,
        version=None,
    )
    __check_package(
        packages,
        "http://wxpython.org/Phoenix/snapshot-builds/wxPython_Phoenix-3.0.3.dev1820+49a8884-cp34-none-win_amd64.whl",
        specifier=None,
        version=None,
    )

    # Additional Requirements without Version Specifiers
    __check_package(packages, "rejected", specifier=None, version=None)
    __check_package(packages, "green", specifier=None, version=None)


def test_write_requirements(tmpdir):
    requirements = gp.read_requirements(__get_file("requirements.txt"))

    file_path = os.path.join(tmpdir, "requirements.txt")
    gp.write_requirements(file_path, requirements)

    assert os.path.exists(file_path)

    with open(file_path, mode="r") as f:
        lines = f.readlines()
    lines.sort()

    assert len(lines) == 17
    assert lines[0] == "-r other-requirements.txt\n"
    assert lines[1] == "./downloads/numpy-1.9.2-cp34-none-win32.whl\n"
    assert lines[2] == "Mopidy-Dirble ~= 1.1\n"
    assert lines[3] == "beautifulsoup4\n"
    assert lines[4] == "coverage != 3.5\n"
    assert lines[5] == "docopt == 0.6.1\n"
    assert lines[6] == "green\n"
    assert (
        lines[7]
        == "http://wxpython.org/Phoenix/snapshot-builds/wxPython_Phoenix-3.0.3.dev1820+49a8884-cp34-none-win_amd64.whl\n"
    )
    assert lines[8] == "keyring >= 4.1.1\n"
    assert lines[9] == "numpy > 1.20.0\n"
    assert lines[10] == "pytest\n"
    assert lines[11] == "pytest-cov\n"
    assert (
        lines[12]
        == "pythonnet @ git+https://github.com/pythonnet/pythonnet@09ecf1b22b9d51691c3da96eb70bf9a615bddb43\n"
    )
    assert lines[13] == "rejected\n"
    assert lines[14] == "requests <= 2.0.0\n"
    assert lines[15] == "treebuilder === 1.20.0\n"
    assert lines[16] == "yarg < 1.0.0\n"


def test_write_requirements_as_list(tmpdir):
    packages = ["numpy", "pandas"]

    file_path = os.path.join(tmpdir, "requirements.txt")
    gp.write_requirements(file_path, packages)

    assert os.path.exists(file_path)

    with open(file_path, mode="r") as f:
        lines = f.readlines()
    lines.sort()

    assert len(lines) == 2
    assert lines[0] == "numpy\n"
    assert lines[1] == "pandas\n"


def test_write_requirements_as_dict(tmpdir):
    packages = {"numpy": "1.20.0", "pandas": "1.3.3"}

    file_path = os.path.join(tmpdir, "requirements.txt")
    gp.write_requirements(file_path, packages)

    assert os.path.exists(file_path)

    with open(file_path, mode="r") as f:
        lines = f.readlines()
    lines.sort()

    assert len(lines) == 2
    assert lines[0] == "numpy == 1.20.0\n"
    assert lines[1] == "pandas == 1.3.3\n"


def test_freeze():
    packages = gp.freeze()
    assert "pytest" in packages
