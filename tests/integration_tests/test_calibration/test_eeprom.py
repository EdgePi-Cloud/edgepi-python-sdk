'''integration test for access eeprom'''

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

import os
PATH = os.path.dirname(os.path.abspath(__file__))

import time
import pytest

from edgepi.calibration.eeprom_constants import EdgePiMemoryInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM

@pytest.fixture(name="eeprom")
def fixture_test_dac():
    eeprom = EdgePiEEPROM()
    # eeprom.init_memory()
    return eeprom

@pytest.mark.parametrize("data, address, expected",
                        [(32, 0, 32),
                         (32, 32, 32)
                        ])
def test__byte_write_register(data, address, expected, eeprom):
    initial_data = eeprom.read_memory(address, 1)
    addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    # pylint: disable=protected-access
    eeprom._EdgePiEEPROM__byte_write_register(addrx, data)
    time.sleep(0.001)
    new_data = eeprom.read_memory(address, 1)
    # pylint: disable=protected-access
    eeprom._EdgePiEEPROM__byte_write_register(addrx, 255)
    assert initial_data[0] != new_data[0]
    assert new_data[0] == expected


@pytest.mark.parametrize("data, address",
                        [
                         (list(range(0,128)),0)
                        ])
def test__page_write_register(data, address, eeprom):
    initial_data = eeprom.read_memory(address, len(data))
    addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    # pylint: disable=protected-access
    eeprom._EdgePiEEPROM__page_write_register(addrx, data)
    time.sleep(0.001)
    new_data = eeprom.read_memory(address, len(data))
    # pylint: disable=protected-access
    eeprom._EdgePiEEPROM__page_write_register(addrx, [255]*len(data))
    for indx, init_data in enumerate(initial_data):
        assert init_data != new_data[indx]
        assert new_data[indx] == data[indx]
