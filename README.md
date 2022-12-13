![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-unit-test.yml/badge.svg)
![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-lint.yml/badge.svg)
---
# What is EdgePi?


![Image](https://user-images.githubusercontent.com/3793563/207419171-c6d4ad94-edca-4daa-ad78-689c16ade4a7.png)


A DIN rail-mounted, Raspberry Pi 4 industrial PC with the features of a Programmable Logic Controller (PLC) and Internet of Things (IoT) cloud edge device. Visit [edgepi.com](https://www.edgepi.com) for more information.

# How to Use EdgePi SDK
## How to Install
The latest stable release of the EdgePi SDK will be available for download via The Python Package Index (PyPi). To install the EdgePi SDK from PyPi via pip, you may use the following command from terminal:

```
python3 -m pip install EdgePi-Python-SDK
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
For more sample code, please refer to each module's documentation by following the links provided in the section below.
# Implemented Modules

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
