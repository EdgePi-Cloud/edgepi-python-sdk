# edgepi-python-sdk

## SDK packaging

- Use setup.py file to edit meta-data when building/created new package
- run ```python -m build``` command in root directory of the SDK create distribution
- run ```py -m twine upload --repository testpypi dist/* --verbose``` command to upload the distribution to TestPyPi

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
