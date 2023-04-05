'''hardware test for eeprom user space'''

# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# https://github.com/protocolbuffers/protobuf/issues/10372

import logging
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import json
import time
import os
PATH = os.path.dirname(os.path.abspath(__file__))

import pytest
from edgepi.calibration.eeprom_constants import EdgePiMemoryInfo, EEPROMInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM


@pytest.fixture(name="eeprom")
def fixture_test_dac():
    eeprom = EdgePiEEPROM()
    return eeprom

def read_dummy_json(file_name: str):
    """
    Read dummy json file
    """
    # pylint: disable=unspecified-encoding
    with open(file_name, "r") as file:
        dummy = json.load(file)
    return dummy

def test__page_write_register(eeprom):
    for val in range(0, 256):
        _logger.info(f"test__page_write_register: Test Value = {val}")
        data = [val]*16384
        initial_data = eeprom.read_memory(0, len(data))
        _logger.info(f"test__page_write_register: Initial Value = {len(initial_data)}")
        addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value
        # pylint: disable=protected-access
        page_n = eeprom._EdgePiEEPROM__generate_list_of_pages(addrx, data)
        for indx, page in enumerate(page_n):
            # pylint: disable=protected-access
            eeprom._EdgePiEEPROM__page_write_register(addrx+(indx*EEPROMInfo.PAGE_SIZE.value), page)
            time.sleep(0.002)
        _logger.info(f"test__page_write_register: Page Written = {len(page_n)}")
        new_data = eeprom.read_memory(0, len(data))
        _logger.info(f"test__page_write_register: New Value = {len(new_data)}")
        for indx, init_data in enumerate(initial_data):
            assert init_data != new_data[indx]
            assert new_data[indx] == data[indx]

def test_eeprom_reset(eeprom):
    reset_vals = []
    eeprom.eeprom_reset()
    num_of_pages = int(EEPROMInfo.NUM_OF_PAGE.value / 2)
    for page in range(num_of_pages, EEPROMInfo.NUM_OF_PAGE.value):
        reset_vals += eeprom._EdgePiEEPROM__sequential_read(page * EEPROMInfo.PAGE_SIZE.value,EEPROMInfo.PAGE_SIZE.value)
    for val in reset_vals:
        assert val == 255

def test_write_memory(eeprom):

    json_data = read_dummy_json(PATH+"/dummy_0.json")
    json_data_s = json.dumps(json_data, indent=0, sort_keys=False, separators=(',', ':'))
    json_data_b = bytes(json_data_s,"utf-8")
    _logger.info(f"test_write_memory: {json_data_b} of data to be written\n")
    _logger.info(f"test_write_memory: type = {type(json_data_b)}")
    _logger.info(f"test_write_memory: length = {len(json_data_b)}")
    eeprom.write_memory(json_data_b)
    time.sleep(0.002)

    # # # # new data
    _logger.info(f"\nCheck the memory by reading back\n")
    eeprom.init_memory()
    new_data = eeprom.read_memory(eeprom.used_size)
    new_data_b = bytes(new_data)
    _logger.info(f"test_write_memory: {new_data_b} read from the memory")
    _logger.info(f"test_write_memory: New Data type = {type(new_data_b)}")
    _logger.info(f"test_write_memory: New Data length = {len(new_data_b)}")
    new_data_parsed = json.loads(new_data_b)

    assert json_data == new_data_parsed


