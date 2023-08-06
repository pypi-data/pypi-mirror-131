from io import TextIOWrapper
import subprocess, sys
from typing import Dict, List, Union

SPECIFIERS = ["===", "==", "@", ">=", "<=", ">", "<", "!=", "~="]
SPECIFIER = "specifier"
VERSION = "version"


def __try_read_specifier(
    packages: Dict[str, Dict[str, str]], line: str, specifier: str
) -> bool:
    split = line.split(specifier)
    if len(split) >= 2:
        packages[split[0].rstrip()] = {
            SPECIFIER: specifier,
            VERSION: str.join(specifier, split[1:]).lstrip(),
        }
        return True
    return False


def read_requirements_lines(lines: List[str]) -> Dict[str, Dict[str, str]]:
    packages = {}
    for line in lines:
        line = line.strip()

        # Skip empty and commented lines
        if line == "" or line.startswith("#"):
            continue
        if "#" in line:
            line = line.split("#")[0].rstrip()

        # Try detect any specifier
        find = next(
            (s for s in SPECIFIERS if __try_read_specifier(packages, line, s)), None
        )
        if find is not None:
            continue

        # Try detect another requirements file
        if line.startswith("-r"):
            packages[line[2:].strip()] = {SPECIFIER: "-r", VERSION: None}
            continue

        # package without specifier or a particular file
        packages[line] = {SPECIFIER: None, VERSION: None}

    return packages


def read_requirements(file_path: str) -> Dict[str, Dict[str, str]]:
    with open(file_path, mode="r") as f:
        lines = f.readlines()
    return read_requirements_lines(lines)


def __write_requirement_line(package: str, requirement: Dict[str, str]) -> None:
    if SPECIFIER in requirement:
        # Requirement file
        if requirement[SPECIFIER] == "-r":
            return f"-r {package}"
        # Package with specifier
        elif requirement[SPECIFIER] is not None:
            # Keep exception if version is not part of the dictionary
            return f"{package} {requirement[SPECIFIER]} {requirement[VERSION]}"
    # Package without specifier or a particular file
    return package


def write_requirements_lines(
    packages: Union[List[str], Dict[str, str], Dict[str, Dict[str, str]]]
) -> List[str]:
    if isinstance(packages, list):  # Simple list of package names
        return [p for p in packages]
    elif isinstance(packages, dict):
        first = next((packages[v] for v in packages), None)
        if isinstance(first, str):  # Dict of package names with version
            return [f"{p} == {packages[p]}" for p in packages]
        elif isinstance(first, dict):  # Dict of package name with requirement
            return [__write_requirement_line(p, packages[p]) for p in packages]

    raise TypeError(
        f"Only List[str], Dict[str, str], Dict[str, Dict[str, str]] ar supported but you give a {type(packages)}"
    )


def __write_line(f: TextIOWrapper, line: str) -> None:
    f.write(line)
    f.write("\n")


def write_requirements(
    file_path: str,
    packages: Union[List[str], Dict[str, str], Dict[str, Dict[str, str]]],
) -> None:
    with open(file_path, mode="w") as f:
        [__write_line(f, l) for l in write_requirements_lines(packages)]


def freeze():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True
    )
    return read_requirements_lines(result.stdout.split("\n"))
