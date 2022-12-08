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
* [Digital to Analog Converter](src/edgepi/dac)
* [Analog to Digital Converter](src/edgepi/adc)
---
## Run Integration/Hardware Tests
There are two ways to run the tests under `tests/`, depending on the virtual environment used. One option is to use a virtual environment with the SDK installed as a package, i.e. from TestPyPi. Note, the latest SDK version on TestPyPi may be out of date as new versions are only published on merge to `staging`, and as such attempting to use this outdated SDK version with your new code will result in pytest errors. Therefore, this approach is recommended for infrequent hardware calibration tests, when you know the SDK version is up to date, not active development. The second approach is to use a virtual environment that does not install the SDK as a package. The tests will then use the latest code in your local repo.


#### Virtual Environment with SDK Installed as a Package
From project root directory run the following:
1. Create virtual env: `python3 -m venv venv_integration`
2. Activate virtual env: `source venv_integration/bin/activate`
3. Install dependencies: `python3 -m pip install -r requirements_integration.txt`
4. Run tests: `python3 -m pytest ./tests/<test_path>`


#### Virtual Environment using local SDK
From project root directory run the following:
1. Create virtual env: `python3 -m venv venv_test`
2. Activate virtual env: `source venv_test/bin/activate`
3. Install dependencies: `python3 -m pip install -r requirements_test.txt`
4. Change directory: `cd ./src`
5. Run tests: `python3 -m pytest ../tests/<test_path>`


#### Generate Test Report
If you wish to generate an HTML test report, choose a virtual environment from above, and replace the "Run tests" step with the following:
* SDK as a package: `python3 -m pytest ./tests/<test_path> --html=<path-to-report> --log-level=INFO`
* Local SDK: `python3 -m pytest ../tests/<test_path> --html=<path-to-report> --log-level=INFO`
    * `<test_path>` can be left blank to run all integration and hardware tests, or a filepath to run a specific test module under `tests/`
    * A folder containing the html test report will be added at `<path-to-report>`. Example path: `./tests/reports/report.html`
    * Include `--log-level=INFO` to add logs with helpful test details in report (recommended)

To view html report:
1. Change directory to report folder: `cd <path-to-report>`
2. Start a simple python webserver on edgepi: `python3 -m http.server`
3. In machine with browser, navigate to `http://<edgepi-address>:8000/`
---
## Configure Self-hosted GitHub Actions Test Runner
The integration tests can be run as part of GitHub Actions workflows, but this requires setting up an EdgePi unit as a self-hosted test runner.
To do so, follow the steps below (as of Dec 2022):
1. Visit https://github.com/osensa/edgepi-python-sdk/settings/actions/runners/
2. Select `New self-hosted runner`
3. Choose OS and architecture -> `Linux` -> `ARM64`
4. Follow all steps under `Download`
5. Run `./config.sh --url https://github.com/osensa/edgepi-python-sdk --token <token>`
6. Run the actions runner as a service: https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service
    * `sudo ./svc.sh install`
    * `sudo ./svc.sh start`
