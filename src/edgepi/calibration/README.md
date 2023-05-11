# EdgePi DAC Module User Guide
___
## Quick Use Example

### Writing Voltage to Analog Out Pin
```python
from edgepi.calibration.eeprom_constants import MessageFieldNumber
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM
from edgepi.calibration.protobuf_mapping import EdgePiEEPROMData

# initialize EEPROM
edgepi_eeprom = EdgePiEEPROM()

# get eeprom dataclass, check EdgePiEEPROMData() dataclass for available attributes
edgepi_eeprom_data = edgepi_eeprom.get_edgepi_reserved_data()


```