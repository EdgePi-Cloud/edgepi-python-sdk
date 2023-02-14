'''hardware test for eeprom user space'''

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

import os
PATH = os.path.dirname(os.path.abspath(__file__))

from contextlib import nullcontext as does_not_raise
import json
import time
import logging
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import pytest

from edgepi.calibration.eeprom_constants import MessageFieldNumber, EdgePiMemoryInfo, EEPROMInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM, MemoryOutOfBound
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

@pytest.fixture(name="eeprom")
def fixture_test_dac():
    eeprom = EdgePiEEPROM()
    return eeprom

def read_dummy_json(file_name: str):
    with open(PATH +"/"+file_name, "r") as f:
        dummy = json.loads(f.read())
    return dummy

@pytest.mark.parametrize("data, num_page, address, expected",
                        [
                         (list(range(0,64)), 2, 0, list(range(0,64))),
                         (list(range(0,64)), 4, 0, list(range(0,64))),
                         (list(range(0,64)), 6, 0, list(range(0,64))),
                        ])
def test__page_write_register(data, num_page, address, expected, eeprom):
    data = data*num_page
    initial_data = eeprom.read_memory(address, len(data))
    addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    page_n = eeprom._EdgePiEEPROM__generate_list_of_pages(addrx, data)
    for indx, page in enumerate(page_n):
        eeprom._EdgePiEEPROM__page_write_register(addrx + (indx*EEPROMInfo.PAGE_SIZE.value), page)
        time.sleep(0.001)
    new_data = eeprom.read_memory(address, len(data))
    for indx, init_data in enumerate(initial_data):
        assert init_data != new_data[indx]
        assert new_data[indx] == data[indx]
    
    reset_data = [255]*EEPROMInfo.PAGE_SIZE.value*num_page
    addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    page_n = eeprom._EdgePiEEPROM__generate_list_of_pages(addrx, reset_data)
    for indx, page in enumerate(page_n):
        eeprom._EdgePiEEPROM__page_write_register(addrx + (indx*EEPROMInfo.PAGE_SIZE.value), page)
        time.sleep(0.001)


def test_eeprom_reset(eeprom):
    eeprom.eeprom_reset()
    reset_vals = eeprom.read_memory(0, 16384)
    for val in reset_vals:
        assert val == 255

# initially empty memory
def test_write_memory(eeprom):
    # is_full, is_empty = eeprom.init_memory()
    # assert is_empty == True
    # assert is_full == False

    # when empty every value is 255
    # initial_data = eeprom.read_memory(0, 0x4000)
    # _logger.info(f"test_write_memory: {len(initial_data)} of initial data")
    # for data in initial_data:
    #     assert data == 255

    fill_data = list(range(2,2916))
    fill_data_b = bytes(json.dumps(fill_data), "utf-8")
    _logger.info(f"test_write_memory: {len(fill_data_b)} of data to be written")
    eeprom.write_memory(fill_data_b, True)
    
    # # # new data
    new_data = eeprom.read_memory(2,16380)
    new_data_b = bytes(new_data)
    _logger.info(f"test_write_memory: {new_data_b} of new data")
    new_data_parsed = json.loads(new_data_b)
    _logger.info(f"test_write_memory: {len(new_data_parsed)} of new data")
    for indx, data in enumerate(new_data_parsed):
        assert data == fill_data[indx]

    
