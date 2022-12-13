![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-unit-test.yml/badge.svg)
![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-lint.yml/badge.svg)
---
# What is EdgePi?


![Image](https://user-images.githubusercontent.com/3793563/207419171-c6d4ad94-edca-4daa-ad78-689c16ade4a7.png)


EdgePi is a DIN rail-mounted, Raspberry Pi 4 industrial PC with the features of a Programmable Logic Controller (PLC), and Internet of Things (IoT) cloud edge device. Visit [edgepi.com](https://www.edgepi.com) for more information.

# How to Use EdgePi SDK
## How to Install
The latest stable release of the EdgePi SDK will be available for download via The Python Package Index (PyPi). To install the EdgePi SDK from PyPi via pip, you may use the following command from terminal:

```
$ python3 -m pip install EdgePi-Python-SDK
```
## Sample Code
The EdgePi SDK provides a wide range of functionality to users, allowing interaction with the many modules onboard the EdgePi. One such module, the ADC, can be used to read voltage continuously from any of the eight EdgePi analog input pins:

```
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ConvMode, ADCNum

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample analog input pin AIN3
edgepi_adc.set_config(adc_1_analog_in=ADCChannel.AIN3, conversion_mode=ConvMode.CONTINUOUS)

# send command to start continuous conversions
edgepi_adc.start_conversions(ADCNum.ADC_1)

# perform 10 voltage reads
for _ in range(10):
  out = edgepi_adc.read_voltage(ADCNum.ADC_1)
  print(out)
  
# stop continuous conversions
edgepi_adc.stop_conversions(ADCNum.ADC_1)
```
For more sample code, please refer to each module's documentation by following the links provided in the 'Implemented Modules' section below.
# Implemented Modules
The EdgePi SDK contains modules intended to represent each connected peripheral device onboard the EdgePi. Below is a directory of the currently available modules.
* [Thermocouple](src/edgepi/tc)
* [Digital to Analog Converter (DAC)](src/edgepi/dac)
* [Analog to Digital Converter (ADC)](src/edgepi/adc)
* [LED Array](src/edgepi/led)
# Development
Active development SDK versions active can be accessed from the following resources:
## Installing from TestPyPi
To install the most recent active development SDK version via [TestPyPi](https://test.pypi.org/project/EdgePi-Python-SDK/):
```
$ python3 -m pip install -i https://test.pypi.org/simple/ EdgePi-Python-SDK
```
Previous development SDK versions can also be installed by specifiying the version number:
```
$ python3 -m pip install -i https://test.pypi.org/simple/ EdgePi-Python-SDK==<version-number>
```
Please refer to [TestPyPi](https://test.pypi.org/project/EdgePi-Python-SDK/) for available SDK versions.
## Installing from GitHub
To install the SDK via HTTPS from GitHub:
```
$ python3 -m pip install git+https://github.com/osensa/edgepi-python-sdk.git@<branch-name>
```
## Dev Environment
Two separate virtual environments can be configured for development purposes. One option is to use a virtual environment with the SDK installed as a package, i.e. from TestPyPi. Note, the latest SDK version on TestPyPi may be out of date with active development code, as new versions are only published on merge to staging. As such, attempting to use this outdated SDK version with your new code will result in errors. Therefore, this approach is recommended for infrequent hardware calibration tests, or when you know the SDK version is up to date. For active development, it is instead recommended to use a virtual environment that does not install the SDK as a package, but uses local source code instead.
### Virtual Environment with SDK Installed as a Package
From the project root directory run the following:
1. Create virtual env:
```
$ python3 -m venv venv_integration
```
2. Activate virtual env:
```
$ source venv_integration/bin/activate
```
3. Install dependencies:
```
$ python3 -m pip install -r requirements_integration.txt
```
4. Run tests:
```
$ python3 -m pytest ./tests/<test_path>
```
### Virtual Environment using local SDK
From project root directory run the following:
1. Create virtual env:
```
$ python3 -m venv venv_test
```
2. Activate virtual env:
```
$ source venv_test/bin/activate
```
3. Install dependencies:
```
$ python3 -m pip install -r requirements_test.txt
```
4. Change directory:
```
$ cd ./src
```
5. Run tests:
```
$ python3 -m pytest ../tests/<test_path>
```
#### Generate Test Report
If you wish to generate an HTML test report, choose a virtual environment from above, and replace the "Run tests" step with either of the following commands:
* SDK as a package:
```
$ python3 -m pytest ./tests/<test_path> --html=<path-to-report> --log-level=INFO
```
* Local SDK:
```
$ python3 -m pytest ../tests/<test_path> --html=<path-to-report> --log-level=INFO
```
The `<test_path>` can be left blank to run all integration and hardware tests, or set to a filepath to run a specific test module under `tests/`. A folder containing the HTML test report will be added at `<path-to-report>`. An example path is: `./tests/reports/report.html`. Include the `--log-level=INFO` tag to add logs with helpful test details in report (recommended).

To view the HTML report:
1. Change directory to report folder:
```
$ cd <path-to-report>
```
2. Start a simple python webserver on edgepi:
```
$ python3 -m http.server
```
3. In a browser-enabled machine, navigate to `http://<edgepi-address>:8000/`
4. The HTML test report folder should be visible.

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

