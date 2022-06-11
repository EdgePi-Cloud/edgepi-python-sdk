# EdgePi Thermocouple Module User Guide
____
## Installing EdgePi SDK Package via Pip
- Inside a virtual environment, run the following:
- `$  pip install https://github.com/osensa/edgepi-python-sdk/tree/abstract-config`
____
## Importing Thermocouple Module from SDK Package
```
from edgepi.edgepi_tc import EdgePiTC

edgepi_tc = EdgePiTC()
```
___
## Using Thermocouple Module
- Configuring multiple thermocouple settings at once:
    * `edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE, tc_type=TCType.TYPE_K, average_mode=AvgMode.AVG_1)`
- Configuring thermocouple settings individually:
    * `edgepi_tc.set_average_mode(AvgMode.AVG_4)`
- Using thermocouple to make a single temperature measurement
    * `edgepi_tc.single_sample()`