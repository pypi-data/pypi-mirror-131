from typing import Dict, List
from .requirements import write_requirements, freeze, VERSION, SPECIFIER
from .import_inspector import inspect_imports, NAME, ABSOLUTE_PATH, RELATIVE_PATH
import shutil, os, re


def __pin_packages(packages) -> Dict[str, Dict[str, str]]:
    installed_packages = freeze()
    requirements = {}
    for package in packages:
        if package in installed_packages:
            requirements[package] = installed_packages[package]
        else:
            requirements[package] = {SPECIFIER: None, VERSION: None}
    return requirements


def __merge(
    file_path: str,
    all_packages: set,
    all_modules: Dict,
    visited: set,
    pypi_servers: List[str],
    proxies=None,
):
    file_path = os.path.normpath(file_path)
    if file_path in visited:
        return

    packages, modules = inspect_imports(
        file_path, pypi_servers=pypi_servers, proxies=proxies
    )
    visited.add(file_path)

    # Merge modules
    for module in modules:
        if module[ABSOLUTE_PATH] not in visited:
            all_modules[module[NAME]] = module
            visited.add(module[ABSOLUTE_PATH])

    # Merge packages
    [all_packages.add(p) for p in packages if p not in all_packages]


def __create_folder(folder: str, force=True) -> str:
    if folder is None or folder == "":
        return folder

    if force and os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder


def cleanup_requirements(
    folder: str,
    pypi_servers: List[str] = ["https://pypi.python.org/pypi"],
    proxies=None,
    pin_packages: bool = True,
    output_path: str = None,
    ignore_folders: List[str] = [
        "__pycache__",
        "venv",
        ".git",
        ".pytest_cache",
        ".eggs",
    ],
):

    ignore_folders if ignore_folders is not None else []
    ignore_regex = set([re.compile(f) for f in ignore_folders])

    packages, modules, visited = set(), {}, set()
    for (root, folders, files) in os.walk(folder):
        if any(r.search(root) is not None for r in ignore_regex):
            folders.clear()
            continue

        [
            __merge(
                os.path.join(root, f), packages, modules, visited, pypi_servers, proxies
            )
            for f in files
            if f.endswith(".py") or f.endswith(".ipynb")
        ]

    if pin_packages:
        packages = __pin_packages(packages)

    file_path = os.path.join(folder, "requirements.txt")
    file_path = file_path if output_path is None else output_path
    __create_folder(os.path.dirname(file_path), force=False)

    write_requirements(file_path, packages)


def isolate(
    file_path: str,
    folder: str,
    pypi_servers: List[str] = ["https://pypi.python.org/pypi"],
    proxies=None,
    pin_packages: bool = True,
) -> None:
    packages, modules = inspect_imports(
        file_path, pypi_servers=pypi_servers, proxies=proxies
    )

    if pin_packages:
        packages = __pin_packages(packages)

    __create_folder(folder, force=True)

    # Generate the requirements file
    requirements_file_path = os.path.join(folder, "requirements.txt")
    write_requirements(requirements_file_path, packages)

    # Isolate all modules dependencies
    shutil.copyfile(file_path, os.path.join(folder, os.path.basename(file_path)))
    for module in modules:
        dst = os.path.join(folder, module[RELATIVE_PATH])
        # Create sub folder if necessary
        __create_folder(os.path.dirname(dst), force=False)
        shutil.copyfile(module[ABSOLUTE_PATH], dst)
