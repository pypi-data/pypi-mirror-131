from setuptools import setup, find_packages
import os


def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


version = "0.1"
if "PROJECT_VERSION" in os.environ:
    version = os.environ["PROJECT_VERSION"]
    print(f"version found: {version}")

setup(
    name="greenpeace",
    version=version,
    author="Fabien Dieulle",
    author_email="fabiendieulle@hotmail.fr",
    description="Python environment clean up.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/fdieulle/greenpeace",
    packages=find_packages(),
    install_requires=["requests", "yarg"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
