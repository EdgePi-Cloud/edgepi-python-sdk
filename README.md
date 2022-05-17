# edgepi-python-sdk

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
│       ├── DAC
│       │   ├── __init__.py
│       │   └── ...submodules
│       ├── Peripherals
│       │   ├── __init__.py
│       │   └── ...submodules
│       ├── ...subpackages
│       ├── dac.py
│       ├── adc.py
│       ├── tc.py
│       └── ...modules
├── tests
│   ├── test_dac.py
│   ├── test_tc.py
│   └── ...each subpackages
├── readme.md
├── setup.py
└── requirements.txt
```

- test requires the installation of the package to test the package as it is installed on user's machine
- src structure prevents the improting of modules from the current director


Three virtual environment setup
1. src_venv: virtual environment to develop source tree of the package
2. build_venv: virtual environment to build and publish the package
3. test_venv: virtual environment to test the package
   - The testPyPi tries to install the dependency in testPyPi instead of actual PyPi. Therefore, the `install_requires` option fails to install the required package. 