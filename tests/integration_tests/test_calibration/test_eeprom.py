'''integration test for access eeprom'''

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))

from contextlib import nullcontext as does_not_raise
import json
import time
import pytest

from edgepi.calibration.eeprom_constants import MessageFieldNumber, EdgePiMemoryInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM, MemoryOutOfBound
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

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
    eeprom._EdgePiEEPROM__byte_write_register(addrx, data)
    time.sleep(0.001)
    new_data = eeprom.read_memory(address, 1)
    eeprom._EdgePiEEPROM__byte_write_register(addrx, 255)
    assert initial_data[0] != new_data[0]
    assert new_data[0] == expected


@pytest.mark.parametrize("data, address, expected",
                        [
                        #  ([2,3,4,5,6,7,8,9,10], 2, [2,3,4,5,6,7,8,9,10]),
                         (list(range(0,128)), 0, list(range(0,128)))
                        ])
def test__page_write_register(data, address, expected, eeprom):
    initial_data = eeprom.read_memory(address, len(data))
    addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    eeprom._EdgePiEEPROM__page_write_register(addrx, data)
    time.sleep(0.001)
    new_data = eeprom.read_memory(address, len(data))
    eeprom._EdgePiEEPROM__page_write_register(addrx, [255]*len(data))
    for indx, init_data in enumerate(initial_data):
        assert init_data != new_data[indx]
        assert new_data[indx] == data[indx]


