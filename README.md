![Image](https://user-images.githubusercontent.com/3793563/207438826-bb656ca5-f19d-4699-8cb4-35acccb2ce58.svg)

EdgePi is a DIN rail-mounted, Raspberry Pi 4 industrial PC with the features of a Programmable Logic Controller (PLC), and Internet of Things (IoT) cloud edge device. Visit [edgepi.com](https://www.edgepi.com) for more information.

![](https://github.com/EdgePi-Cloud/edgepi-python-sdk/actions/workflows/python-unit-test.yml/badge.svg)
![](https://github.com/EdgePi-Cloud/edgepi-python-sdk/actions/workflows/python-lint.yml/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/EdgePi-Cloud/edgepi-python-sdk/blob/main/LICENSE)
---
# EdgePi SDK
Use our user-friendly Python SDK to control the EdgePi hardware with just a few lines of simple Python Code.
![Image](https://user-images.githubusercontent.com/3793563/207419171-c6d4ad94-edca-4daa-ad78-689c16ade4a7.png)
# How to Use EdgePi SDK
## How to Install
The latest stable release of the EdgePi SDK will be available to be installed via The Python Package Index (PyPi). To install the EdgePi SDK from PyPi via pip, you may use the following command from terminal:

```
$ python3 -m pip install edgepi-python-sdk
```
## Example Code
The EdgePi SDK provides a wide range of functionality to users, allowing interaction with the many modules onboard the EdgePi. One such module, the ADC, can be used to read voltage continuously from any of the eight EdgePi analog input pins:

```python
from edgepi.dac.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ConvMode

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample input pin 4 (the input pins are 0-indexed)
edgepi_adc.set_config(adc_1_analog_in=ADCChannel.AIN3, conversion_mode=ConvMode.CONTINUOUS)

# send command to start automatic conversions
edgepi_adc.start_conversions()

# perform 10 voltage reads
for _ in range(10):
  out = edgepi_adc.read_voltage()
  print(out)
  
# stop automatic conversions
edgepi_adc.stop_conversions()
```
For further details on this and other modules, please refer to each module's documentation by following the links provided in the `Implemented Modules` section below.
# Implemented Modules
The EdgePi SDK contains modules intended to represent each connected peripheral device onboard the EdgePi. Below is a directory of the currently available modules.
* [Thermocouple](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/src/edgepi/tc)
* [Digital to Analog Converter (DAC)](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/src/edgepi/dac)
* [Analog to Digital Converter (ADC)](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/src/edgepi/adc)
* [LED Array](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/src/edgepi/led)
* [Digital Input (DIN)](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/src/edgepi/digital_input)
* [Digital Output (DOUT)](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/src/edgepi/digital_output)
# Development
Active development SDK versions can be accessed from the following resources:
## Installing from TestPyPi
To install the most recent active development SDK version via [TestPyPi](https://test.pypi.org/project/edgepi-python-sdk/):
```

$ python3 -m pip install -i https://test.pypi.org/simple/edgepi-python-sdk
```
Previous development SDK versions can also be installed by specifiying the version number:
```
$ python3 -m pip install -i https://test.pypi.org/simple/edgepi-python-sdk==<version-number>
```
Please refer to [TestPyPi](https://test.pypi.org/project/edgepi-python-sdk/) for available SDK versions.

## Installing from GitHub
To install the SDK via HTTPS from GitHub:
```
$ python3 -m pip install git+https://github.com/EdgePi-Cloud/edgepi-python-sdk.git@<branch-name>
```

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

# Performance

The following benchmarks were measured on the Rasberry Pi 4, with all edgepi daemons disabled. They're also the slowest average of 3 runs.

The **Performance** column represents how long it takes to call one function, while the **Max Read Frequency** column represents how many times that function could be called every second.

| Feature | Performance | Max Read Frequency | Function | Example | Description |
| -- | -- | -- | -- | -- | -- |
| Single DIN | 0.85ms per 8 DIN | 1171 Hz | `digital_input_state(...)` | [examples/single_din.py](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/examples/single_din.py) | |
| Batched DIN | 0.52ms per 8 DIN | 1936 Hz | `digital_input_state_batch(...)` | [examples/batched_din.py](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/examples/batched_din.py) | |
| Single ADC | 97.3 ms per 8 ADC | 10.3 Hz | `set_config(...)` <br><br> `single_sample()` | [examples/single_adc.py](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/examples/single_adc.py) | Reads from ADC1 only |
| Batched ADC | 6.49 ms per 8 ADC | 154 Hz | `read_samples_adc1_batch(...)` | [examples/batched_adc.py](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/examples/batched_adc.py) | Reads from ADC1 only |
| Batched ADC/Diff | 5.467 ms per 4 ADC, 2 Diff | 183 Hz | `read_samples_adc1_batch(...)` | [examples/batched_adc_diff.py](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/examples/batched_adc_diff.py) | Differential ADC inputs each use two pins. Reads from ADC1 only |
| Thermocouple (TC) | 100.2ms | 9.98 hz | `read_temperatures()` | [examples/single_tc.py](https://github.com/EdgePi-Cloud/edgepi-python-sdk/tree/main/examples/single_tc.py) | Limited by [hardware](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31856.pdf) (see conversion mode). 100ms is needed for accurate (19 bit) readings |

# Bug Reports / Feature Requests
Use [GitHub Issues Page](https://github.com/EdgePi-Cloud/edgepi-python-sdk/issues) to report any issues or feature requests.

# Get involved
Follow [@edgepi_cloud on Twitter](https://twitter.com/edgepi_cloud/).
See the [EdgePi wiki](https://wiki.edgepi.com/) for more information on how to get started with your EdgePi.
If you have a specific question, please check out our [discussion forums](https://www.edgepi.com/forums).

# License
EdgePi SDK is distributed under [MIT License](https://github.com/EdgePi-Cloud/edgepi-python-sdk/blob/main/LICENSE). 
