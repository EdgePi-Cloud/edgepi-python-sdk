# EdgePi EEPROM Module
EEPROM module is used to store data to on-board EEPROM via I2C protocol

# Hardware
The on-board EEPROM provide 32768 Bytes of data. The available memory is divided into two sections.
1. EdgePi Reserved Space, 0~16383 Bytes
2. User Space, 16384~32767 Bytes

Each section has separate methods to read/write. 

__It is not recommanded for the end user to write to EdgePi Reserved Space__

# Example Code

## Reading EdgePi Reserved Memory
```python
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM

edgepi_eeprom = EdgePiEEPROM()
eeprom_data = edgepi_eeprom.get_edgepi_data()
```
## Writing EdgePi Reserved Memory
```python
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM
from edgepi.eeprom.eeprom_constants import EepromModuleNames

edgepi_eeprom = EdgePiEEPROM()
eeprom_data = edgepi_eeprom.get_edgepi_data()
# Changing Config_key certificate
eeprom_data.config_key.certificate = "Changed Config key certificate"
# Get Modified dataclass
modified_data = edgepi_eeprom.set_edgepi_dataclass(EepromModuleNames.CONFIG_KEY, eeprom_data.config_key)
# Write the modified dataclass to the memory
edgepi_eeprom.set_edgepi_data(modified_data)
```

## Reset EdgePi Reserved Memory
```python
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM
from edgepi.eeprom.eeprom_constants import EepromModuleNames, DEFUALT_EEPROM_BIN
import base64
import hashlib

edgepi_eeprom = EdgePiEEPROM()

default_bin = base64.b64decode(DEFUALT_EEPROM_BIN)
hash_res = hashlib.md5(default_bin)
edgepi_eeprom.reset_edgepi_memory(hash_res.hexdigest())
```



# Functionalities

# User Guide

# Limitations 