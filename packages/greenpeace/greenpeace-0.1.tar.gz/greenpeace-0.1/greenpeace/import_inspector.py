import os
import sys
import glob
import ast
import logging
from typing import List, Tuple, Dict, Set
import json
from .pypi_server import package_exists


NAME = "name"
RELATIVE_PATH = "relative_path"
ABSOLUTE_PATH = "absolute_path"


def list_base_packages():
    if sys.platform == "win32":
        sub_path = "Lib"
    else:
        sub_path = f"lib/python{sys.version_info.major}.{sys.version_info.minor}"

    py_files = [
        f
        for f in glob.glob(f"{sys.base_prefix}/{sub_path}/**/*.py", recursive=True)
        if "site-packages" not in f and "__pycache__" not in f
    ]

    packages = set(sys.builtin_module_names)
    base_lib = os.path.normpath(os.path.join(sys.base_prefix, sub_path))
    for py_file in py_files:
        module_name = os.path.basename(py_file)[:-3]
        py_folder = os.path.dirname(py_file)

        if module_name == "__init__":
            module_name = os.path.basename(py_folder)
            py_folder = os.path.normpath(os.path.join(py_folder, ".."))

        while os.path.normpath(py_folder) != base_lib:
            module_name = f"{os.path.basename(py_folder)}.{module_name}"
            py_folder = os.path.normpath(os.path.join(py_folder, ".."))

        packages.add(module_name)

    return packages


def ipynb_to_py(file_path: str) -> str:
    with open(file_path, "r") as f:
        data = json.load(f)
        sources = [
            cell["source"] for cell in data["cells"] if cell["cell_type"] == "code"
        ]

        code = []
        for source in sources:
            [code.append(line) for line in source]
            code.append("\n")
        content = str.join("", code)

    return content


def get_imports(file_path: str) -> Set[str]:
    if file_path is None or not os.path.exists(file_path):
        return set()

    imports = set()
    try:
        if file_path.endswith(".ipynb"):
            content = ipynb_to_py(file_path)
        else:
            with open(file_path, "r") as f:
                content = f.read()

        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for child in node.names:
                    imports.add(child.name)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
    except Exception as e:
        logging.error(f"Failed getting imports on file: {file_path}")

    return imports


def __as_local_module(module: str, python_paths: List[str] = ["."]) -> List[str]:
    relative_path = f"{module.replace('.', '/')}.py"
    for python_path in python_paths:
        absoulte_path = os.path.join(python_path, relative_path)
        if os.path.exists(absoulte_path):
            return {
                NAME: module,
                RELATIVE_PATH: os.path.normpath(relative_path),
                ABSOLUTE_PATH: os.path.normpath(absoulte_path),
            }
    return None


def __is_local_module(module: str, python_paths: List[str] = ["."]):
    return __as_local_module(module, python_paths) is not None


def to_package_candidates(module: str) -> List[str]:
    split = module.split(".")
    result = []

    package = split[0]
    result.append(package)
    for i in range(1, len(split)):
        package = f"{package}.{split[i]}"
        result.append(package)

    return result


def inspect_imports(
    file_path: str,
    pypi_servers: List[str] = ["https://pypi.python.org/pypi"],
    proxies=None,
) -> Tuple[List[str], Dict[str, Dict[str, str]]]:
    base_packages = list_base_packages()
    imports = get_imports(file_path)

    python_paths = [
        f
        for f in sys.path
        if sys.base_prefix not in os.path.normpath(f) and "site-packages" not in f
    ]

    packages = set()
    modules = []

    stack = [(i, file_path) for i in imports]  # Copy required here
    while len(stack) > 0:
        module, py_file = stack.pop()
        python_paths_ext = [os.path.dirname(py_file)] + python_paths

        # If/elif order is important here to respect python_paths priority
        if __is_local_module(module, python_paths_ext):
            local_module = __as_local_module(module, python_paths_ext)
            modules.append(local_module)

            py_file = local_module[ABSOLUTE_PATH]
            local_imports = get_imports(py_file)
            # Walk on new imports
            for new_import in local_imports.difference(imports):
                imports.add(new_import)
                stack.append((new_import, py_file))
        elif module not in base_packages:
            candidates = to_package_candidates(module)
            package_name = next(
                (
                    c
                    for p in pypi_servers
                    for c in candidates
                    if package_exists(c, p, proxies=proxies)
                ),
                None,
            )

            if package_name is not None and package_name not in packages:
                packages.add(package_name)

    packages = list(packages)
    packages.sort()
    modules.sort(key=lambda x: x[NAME])
    return packages, modules
