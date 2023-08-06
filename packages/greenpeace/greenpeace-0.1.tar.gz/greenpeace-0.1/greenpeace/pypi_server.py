import requests
import logging
from yarg import json2package
from yarg.exceptions import HTTPError


def fetch_pypi_server(
    package: str,
    pypi_server: str = "https://pypi.python.org/pypi",
    version: str = None,
    proxies=None,
):
    if pypi_server.endswith("/"):
        pypi_server = pypi_server[:-1]

    url = (
        f"{pypi_server}/{package}/json"
        if version is None
        else f"{pypi_server}/{package}/{version}/json"
    )
    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            if hasattr(response.content, "decode"):
                data = json2package(response.content.decode())
            else:
                data = json2package(response.content)
        elif response.status_code == 300:
            logging.debug(
                f"Package {package} not found on {pypi_server}. Status: {response.status_code}, Reason: {response.reason}"
            )
            return None
        else:
            logging.debug(
                f"Package {package} not found on {pypi_server} with version: {version}. Status: {response.status_code}, Reason: {response.reason}"
            )
            return None
    except HTTPError:
        logging.debug(f"Package {package} does not exist on {pypi_server}")
        return None

    return data


def get_latest_version(
    package: str,
    pypi_server: str = "https://pypi.python.org/pypi",
    proxies=None,
) -> str:
    data = fetch_pypi_server(package, pypi_server, proxies=proxies)
    return data.latest_release_id


def package_exists(
    package: str,
    pypi_server: str = "https://pypi.python.org/pypi",
    version: str = None,
    proxies=None,
) -> bool:
    return (
        fetch_pypi_server(package, pypi_server, version=version, proxies=proxies)
        is not None
    )
