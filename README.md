![Image](https://user-images.githubusercontent.com/3793563/207438826-bb656ca5-f19d-4699-8cb4-35acccb2ce58.svg)

EdgePi is a DIN rail-mounted, Raspberry Pi 4 industrial PC with the features of a Programmable Logic Controller (PLC), and Internet of Things (IoT) cloud edge device. Visit [edgepi.com](https://www.edgepi.com) for more information.

![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-unit-test.yml/badge.svg)
![](https://github.com/osensa/edgepi-python-sdk/actions/workflows/python-lint.yml/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/EdgePi-Cloud/edgepi-python-sdk/blob/main/LICENSE)
---
# EdgePi SDK
Use our user-friendly Python SDK to control the EdgePi hardware with just a few lines of simple Python Code.
![Image](https://user-images.githubusercontent.com/3793563/207419171-c6d4ad94-edca-4daa-ad78-689c16ade4a7.png)
# How to Use EdgePi SDK
## How to Install
The latest stable release of the EdgePi SDK will be available to be installed via The Python Package Index (PyPi). To install the EdgePi SDK from PyPi via pip, you may use the following command from terminal:

```
$ python3 -m pip install EdgePi-Python-SDK
```
## Example Code
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
For further details on this and other modules, please refer to each module's documentation by following the links provided in the `Implemented Modules` section below.
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
 

# Packaging
To build and publish a new SDK version as a package, a build virtual environment is required. This may be configured as follows:
```
$ cd edgepi-python-sdk

$ python3 -m venv venv_build

$ source venv_build/bin/activate 

$ python3 -m pip install -r requirements_build.txt
```
With the build environment configured and activated, a new distribution can be built as follows:
```
$ python3 -m build
```
Note, when the package structure changes, such as after renaming the `src` module or other folders, delete the `.egg-info` file from `/src` and rebuild. This will ensure the file names in the compiled package are updated. Also note that changes in file/folder name capitalization are recognized by git. To disable this:
```
git config --global core.ignorecase false
```

With the new disbtribution created, you may publish to the official Python package repositories:

To publish to TestPyPi:
```
$ python3 -m twine upload --repository testpypi dist/* --verbose
```
To publish to PyPi:
```
$ python3 -m twine upload dist/* --verbose
```

Both TestPyPi and PyPi will prompt you for authentication. For best practices, use a corresponding TestPyPi or PyPi token to authenticate as follows:
```
name: __token__
password: <token-value>
```
Make sure to include the `pypi-` prefix for your token value.

# Tests
## Test Environment
Two separate virtual environments can be configured for testing purposes. One option is to use a virtual environment with the SDK installed as a package, i.e. from TestPyPi. Note, the latest SDK version on TestPyPi may be out of date with active development code, as new versions are only published on merge to `staging`. Attempting to use an outdated SDK version with new test code will result in errors. Therefore, this approach is recommended for infrequent hardware calibration tests, or when you know the SDK version to be installed is up to date with your test code. For active development, it is instead recommended to use a virtual environment that does not install the SDK as a package, but uses local source code instead.
## Run Integration/Hardware Tests
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
### Generate Test Report
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

### Configure Self-hosted GitHub Actions Test Runner
The integration tests can be run as part of GitHub Actions workflows, but this requires setting up an EdgePi unit as a self-hosted test runner.
To do so, follow the steps below (working as of Dec 2022):
1. Visit https://github.com/osensa/edgepi-python-sdk/settings/actions/runners/
2. Select `New self-hosted runner`
3. Choose OS and architecture -> `Linux` -> `ARM64`
4. Follow all steps under `Download`
5. Run `$ ./config.sh --url https://github.com/osensa/edgepi-python-sdk --token <token>`
    * `<token>` here denotes your personal GitHub access token
6. Run the actions runner [as a service](https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service):
```
$ sudo ./svc.sh install
$ sudo ./svc.sh start
```
# Bug Reports / Feature Requests
Use [GitHub Issues Page](https://github.com/EdgePi-Cloud/edgepi-python-sdk/issues) to report any issues or feature requests.

# Get involved
Follow [@edgepi_cloud on Twitter](https://twitter.com/edgepi_cloud/).
Read and subscribe to the [EdgePi blog](https://www.edgepi.com/blog).
If you have a specific question, please check out our [discussion forums](https://www.edgepi.com/forums).

# License
EdgePi SDK is distributed under [MIT License](https://github.com/EdgePi-Cloud/edgepi-python-sdk/blob/main/LICENSE). 
