import base64
import hashlib
import platform

import pytest

from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM
from edgepi.eeprom.eeprom_constants import DEFAULT_EEPROM_BIN_B64

@pytest.fixture(scope="session", autouse=True)
def eeprom_reset():
    edgepi_eeprom = EdgePiEEPROM()

    if platform.node() == "edgepi-intg2":
        print('loading default eeprom image ...')
        default_bin = base64.b64decode(DEFAULT_EEPROM_BIN_B64)
        hash_res = hashlib.md5(default_bin)
        print('reseting eeprom ...')
        edgepi_eeprom.reset_edgepi_memory(hash_res.hexdigest(), default_bin)
        print('done!')
    else:
        print("dont reset eeprom")
