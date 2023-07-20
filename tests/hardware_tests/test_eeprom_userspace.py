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
from edgepi.eeprom.eeprom_constants import EEPROMInfo
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM


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

def test_reset_user_space(eeprom):
    reset_vals = []
    eeprom.reset_user_space()
    num_of_pages = int(EEPROMInfo.NUM_OF_PAGE.value / 2)
    for page in range(num_of_pages, EEPROMInfo.NUM_OF_PAGE.value):
        # pylint: disable=line-too-long
        # pylint: disable=protected-access
        reset_vals += eeprom._EdgePiEEPROM__sequential_read(page * EEPROMInfo.PAGE_SIZE.value,EEPROMInfo.PAGE_SIZE.value)
    for val in reset_vals:
        assert val == 255

def test_write_user_space(eeprom):

    json_data = read_dummy_json(PATH+"/dummy_0.json")
    json_data_s = json.dumps(json_data, indent=0, sort_keys=False, separators=(',', ':'))
    json_data_b = bytes(json_data_s,"utf-8")
    _logger.info(f"test_write_user_space: {json_data_b} of data to be written\n")
    _logger.info(f"test_write_user_space: type = {type(json_data_b)}")
    _logger.info(f"test_write_user_space: length = {len(json_data_b)}")
    eeprom.write_user_space(json_data_b)
    time.sleep(0.002)

    # # # # new data
    _logger.info("\nCheck the memory by reading back\n")
    eeprom.init_memory()
    new_data = eeprom.read_user_space(eeprom.used_size)
    new_data_b = bytes(new_data)
    _logger.info(f"test_write_user_space: {new_data_b} read from the memory")
    _logger.info(f"test_write_user_space: New Data type = {type(new_data_b)}")
    _logger.info(f"test_write_user_space: New Data length = {len(new_data_b)}")
    new_data_parsed = json.loads(new_data_b)

    assert json_data == new_data_parsed
