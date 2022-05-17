# edgepi-python-sdk

## Develop Environment Setup
Two separate virtual environment is needed.
1. venv_build: building environement where the package is compiled and published. import requirements_build.txt for pip dependencies.
2. venv_test 
   - TDD environment where the package source tree can be tested as bug fix / new features are implemented.The `testPyPi` tries to install the dependency in `testPyPi` instead of actual `PyPi`. Therefore, the `install_requires` option fails to install the required package. 
   - This environment is also used to test the package after it is published. Install the package using `pip` and run test scripts inside `test` folder. This will import the installed package, not the modules in the `src` directory.

## SDK packaging

- Use setup.py file to edit meta-data when building/created new package
- run ```python -m build``` command in root directory of the SDK create distribution
- run ```py -m twine upload --repository testpypi dist/* --verbose``` command to upload the distribution to TestPyPi

__NOTE__ when package structure name, such as folder or module src file name, changes, delete '.egg-info' file and rebuild. This will ensure the file name in compiled package is changed.

Change in capitalization in file/folder names are recognized by git
```
git config --global core.ignorecase false
```

## SDK Structure
```
EDGEPI-PYTHON-SDK
├── src
│   └── edgepi
│       ├── __init__.py
│       ├── dac
│       │   ├── __init__.py
│       │   └── ...submodules
│       ├── peripherals
│       │   ├── __init__.py
│       │   └── ...submodules
│       ├── ...subpackages
│       ├── edgepi_dac.py
│       ├── edgepi_adc.py
│       ├── edgepi_tc.py
│       └── ...modules
│   └── test_edgepi
│       ├── __init__.py
│       ├── test_dac
│       │   ├── __init__.py
│       │   └── ...submodules
│       ├── test_peripherals
│       │   ├── __init__.py
│       │   └── ...submodules
│       ├── ...test_subpackages
├── tests
│   ├── test_dac.py
│   ├── test_tc.py
│   └── ...each subpackages
├── readme.md
├── setup.py
└── requirements.txt
```