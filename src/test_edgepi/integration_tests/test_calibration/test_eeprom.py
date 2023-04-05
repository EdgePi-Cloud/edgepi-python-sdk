'''integration test for access eeprom'''

# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# https://github.com/protocolbuffers/protobuf/issues/10372
# TODO: I2C Transaction fails without 0.002ms delay

import os
PATH = os.path.dirname(os.path.abspath(__file__))

import time
import logging
import pytest
_logger = logging.getLogger(__name__)

from edgepi.calibration.eeprom_constants import EdgePiMemoryInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM

@pytest.fixture(name="eeprom")
def fixture_test_eeprom():
    eeprom = EdgePiEEPROM()
    return eeprom

@pytest.mark.parametrize("data, address",
                        [
                         (list(range(0,64)),0),
                         (list(range(64,128)),64),
                        ])
def test__page_write_register(data, address, eeprom):
    addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    initial_data = eeprom._EdgePiEEPROM__sequential_read(addrx,len(data))
    # pylint: disable=protected-access
    eeprom._EdgePiEEPROM__page_write_register(addrx, data)
    time.sleep(0.5)
    new_data = eeprom._EdgePiEEPROM__sequential_read(addrx,len(data))
    # pylint: disable=protected-access
    time.sleep(0.5)
    eeprom._EdgePiEEPROM__page_write_register(addrx, [255]*len(data))
    _logger.info(f"data to write = {data}")
    _logger.info(f"initial data  = {initial_data}")
    _logger.info(f"new data      = {new_data}")
    for indx, init_data in enumerate(initial_data):
        assert init_data != new_data[indx]
        assert new_data[indx] == data[indx]
