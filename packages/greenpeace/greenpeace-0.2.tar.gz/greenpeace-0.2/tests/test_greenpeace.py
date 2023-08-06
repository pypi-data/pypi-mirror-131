import greenpeace as gp
import os


def __get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "files", name)


def __check_requirement(requirements, package, specifier, version):
    assert package in requirements
    assert requirements[package][gp.requirements.SPECIFIER] == specifier
    assert requirements[package][gp.requirements.VERSION] == version


def test_isolate_py_script(tmpdir):
    py_file = __get_file("_script.py")

    isolated_folder = os.path.join(tmpdir, "isolate")
    gp.isolate(py_file, isolated_folder)

    assert os.path.exists(isolated_folder)
    assert os.path.exists(os.path.join(isolated_folder, "requirements.txt"))
    assert os.path.exists(os.path.join(isolated_folder, "_script.py"))
    assert os.path.exists(os.path.join(isolated_folder, "_other.py"))
    assert os.path.exists(os.path.join(isolated_folder, "greenpeace", "pypi_server.py"))

    requirements = gp.read_requirements(
        os.path.join(isolated_folder, "requirements.txt")
    )
    __check_requirement(requirements, "numpy", None, None)
    __check_requirement(requirements, "pandas", None, None)
    __check_requirement(requirements, "requests", "==", "2.26.0")
    __check_requirement(requirements, "yarg", "==", "0.1.9")


def test_isolate_notebook(tmpdir):
    py_file = __get_file("notebook.ipynb")

    isolated_folder = os.path.join(tmpdir, "isolate")
    gp.isolate(py_file, isolated_folder)

    assert os.path.exists(isolated_folder)
    assert os.path.exists(os.path.join(isolated_folder, "requirements.txt"))
    assert os.path.exists(os.path.join(isolated_folder, "notebook.ipynb"))
    assert os.path.exists(os.path.join(isolated_folder, "_other.py"))
    assert os.path.exists(os.path.join(isolated_folder, "greenpeace", "pypi_server.py"))

    requirements = gp.read_requirements(
        os.path.join(isolated_folder, "requirements.txt")
    )
    __check_requirement(requirements, "numpy", None, None)
    __check_requirement(requirements, "pandas", None, None)
    __check_requirement(requirements, "requests", "==", "2.26.0")
    __check_requirement(requirements, "yarg", "==", "0.1.9")


def test_cleanup_requirements(tmpdir):

    file_path = os.path.join(tmpdir, "requirements.txt")
    gp.cleanup_requirements(".", output_path=file_path)

    assert os.path.exists(file_path)

    requirements = gp.read_requirements(file_path)

    __check_requirement(requirements, "setuptools", None, None)
    __check_requirement(requirements, "numpy", None, None)
    __check_requirement(requirements, "pandas", None, None)
    __check_requirement(requirements, "requests", "==", "2.26.0")
    __check_requirement(requirements, "yarg", "==", "0.1.9")
