# edgepi-python-sdk
---
![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-unit-test.yml/badge.svg)
![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-lint.yml/badge.svg)
---
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
---
## Installing EdgePi-Python-SDK Package via Pip
- Inside a virtual environment, run either of the following commands to install:
- Via GitHub HTTPS 
    * `$ python3 -m pip install git+https://github.com/osensa/edgepi-python-sdk.git@staging`
        - The latest semi-stable version is available on the `staging` branch, but the intention is to eventually have a stable version on our `main` branch. Once we have this, `staging` here will have to replaced with `main`.
    * Note: since this repository is currently private, you will be required to input your personal access token. See this [guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for creating a personal access token, if you do not yet have one.
- Via TestPyPi
    * `$ python3 -m pip install -i https://test.pypi.org/simple/ EdgePi-Python-SDK`
- Via PyPi
    * ` $ python3 -m pip install EdgePi-Python-SDK`
        - The latest stable release will be published here. Note, the SDK is not yet available on PyPi. The package name here is a placeholder and will have to be replaced.
---
## EdgePi-Python-SDK Modules
This SDK contains modules intended to represent each connected peripheral device on the EdgePi. Below is a directory of the available modules.
* [Thermocouple](src/edgepi/tc)
* [Digital to Analogue Converter](src/edgepi/dac)
* [Analog to Digital Converter](src/edgepi/adc)
---
## Run Integration/Hardware Tests
From project root directory run the following:
1. `python3 -m venv venv_integration`
2. `source venv_integration/bin/activate`
3. `python3 -m pip install -r requirements_integration.txt`
4. `python3 -m pytest ./tests/test_voltage_rw.py --html=<path-to-report> --log-level=INFO`
    * A folder containing the html test report will be added at `<path-to-report>`. Example path: `./tests/reports/report.html`

To view html report:
1. Copy report folder to machine with browser
2. Change directory inside report folder
3. Start a simple python webserver: on Windows `python http.server`
4. In browser, navigate to `http://localhost:8000/`