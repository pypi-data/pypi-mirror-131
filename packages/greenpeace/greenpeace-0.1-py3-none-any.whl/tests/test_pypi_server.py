from greenpeace.pypi_server import get_latest_version, fetch_pypi_server, package_exists


def test_get_latest_version():
    version = get_latest_version("numpy")
    assert version is not None


def test_fetch_pypi_server():
    data = fetch_pypi_server("numpy", version="1.20.0")
    assert data is not None


def test_fetch_pypi_server_failed():
    data = fetch_pypi_server("numpy", version="1.20.20")
    assert data is None


def test_package_exists():
    assert package_exists("numpy")


def test_package_not_exists():
    assert not package_exists("not_exists_numpy")
