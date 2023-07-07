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
eeprom_data = edgepi_eeprom.read_edgepi_data()
```
## Writing EdgePi Reserved Memory
__NOTE__: To write to the eeprom memory, the memory needs to be read first.
```python
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM

edgepi_eeprom = EdgePiEEPROM()
# Read the eeprom memory first
eeprom_data = edgepi_eeprom.read_edgepi_data()
# Changing Config_key certificate
eeprom_data.config_key.certificate = "Changed Config key certificate"
# Write the modified dataclass to the memory
edgepi_eeprom.write_edgepi_data(eeprom_data)
```

## Reset EdgePi Reserved Memory
__NOTE__: Memory can be reset to custom data set when a custom bin file is avalable. Replace the default_bin with the bin file content in bytes and pass the md5sum of the content.

__WARNING__: This method overwrites private keys and certificate which may affect the accessability.
```python
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM
from edgepi.eeprom.eeprom_constants import DEFAULT_EEPROM_BIN_B64
import base64
import hashlib

edgepi_eeprom = EdgePiEEPROM()

default_bin = base64.b64decode(DEFAULT_EEPROM_BIN_B64)
hash_res = hashlib.md5(default_bin)
edgepi_eeprom.reset_edgepi_memory(hash_res.hexdigest(), default_bin)
```

# Functionalities

# User Guide

# Limitations