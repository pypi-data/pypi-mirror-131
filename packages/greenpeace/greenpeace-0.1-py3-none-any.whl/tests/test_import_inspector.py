import os
from greenpeace.import_inspector import (
    to_package_candidates,
    get_imports,
    inspect_imports,
    NAME,
    RELATIVE_PATH,
    ABSOLUTE_PATH,
)


def __get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "files", name)


def test_get_imports():
    py_file = __get_file("_script.py")
    imports = get_imports(py_file)

    assert imports == set(
        [
            "math",
            "numpy",
            "pandas",
            "random",
            "datetime",
            "greenpeace.pypi_server",
            "_other",
        ]
    )


def test_get_imports_from_notebook():
    py_file = __get_file("notebook.ipynb")
    imports = get_imports(py_file)

    assert imports == set(
        [
            "numpy",
            "pandas",
            "random",
            "greenpeace.pypi_server",
            "_other",
        ]
    )


def test_to_package_candidates():
    candidates = to_package_candidates("numpy")
    assert candidates == ["numpy"]

    candidates = to_package_candidates("django.config")
    assert candidates == ["django", "django.config"]

    candidates = to_package_candidates("a.b.c")
    assert candidates == ["a", "a.b", "a.b.c"]


def test_inspect_imports():
    py_file = __get_file("_script.py")
    packages, modules = inspect_imports(py_file)

    assert packages == ["numpy", "pandas", "requests", "yarg"]

    assert modules[0][NAME] == "_other"
    assert modules[0][RELATIVE_PATH] == "_other.py"
    assert modules[0][ABSOLUTE_PATH].endswith(
        os.path.join("tests", "files", "_other.py")
    )
    assert modules[1][NAME] == "greenpeace.pypi_server"
    assert modules[1][RELATIVE_PATH] == os.path.join("greenpeace", "pypi_server.py")
    assert modules[1][ABSOLUTE_PATH].endswith(
        os.path.join("greenpeace", "pypi_server.py")
    )
