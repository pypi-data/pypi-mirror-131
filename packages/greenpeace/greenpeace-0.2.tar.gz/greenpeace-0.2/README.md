# greenpeace

![build](https://github.com/fdieulle/greenpeace/actions/workflows/build.yml/badge.svg)
[![codecov](https://codecov.io/gh/fdieulle/greenpeace/branch/main/graph/badge.svg?token=7AAFH9JUHG)](https://codecov.io/gh/fdieulle/greenpeace)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![license](https://img.shields.io/badge/license-MIT-blue.svg?maxAge=3600)](./LICENSE) 
[![pypi](https://img.shields.io/pypi/v/greenpeace.svg)](https://pypi.org/project/greenpeace/)
[![python supported](https://img.shields.io/pypi/pyversions/greenpeace.svg)](https://pypi.org/project/greenpeace/)

Python environment clean up. 

The package allows you to generate your package dependencies requirements directly from your source code. Python scripts `.py` and notebooks `.ipynb` are supported. You can also pin the package versions extracted with your current environment.

```python
import greenpeace as gp

gp.cleanup_requirements(".", output_path="requirements.txt")
```

The package is also able to extract from a python script or a notbook the modules dependencies in your project. This feature is useful if you want to isolate a script or notebook from you project into a dedicated folder.

```python
import greenpeace as gp

gp.isolate("[YOUR_PATH]/notebook.ipynb", "./isolated")
```

The isolated folder will contains all you project dependencies and a `requirements.txt` file for all package dependencies in use.

