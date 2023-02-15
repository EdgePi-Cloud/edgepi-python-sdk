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
    with open(file_name, "r") as f:
        dummy = json.load(f)
    return dummy

def test__page_write_register(eeprom):
    for val in range(0, 256):
        _logger.info(f"test__page_write_register: Test Value = {val}")
        data = [val]*16384
        initial_data = eeprom.read_memory(0, len(data))
        _logger.info(f"test__page_write_register: Initial Value = {len(initial_data)}")
        addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value
        page_n = eeprom._EdgePiEEPROM__generate_list_of_pages(addrx, data)
        for indx, page in enumerate(page_n):
            eeprom._EdgePiEEPROM__page_write_register(addrx + (indx*EEPROMInfo.PAGE_SIZE.value), page)
            time.sleep(0.002)
        _logger.info(f"test__page_write_register: Page Written = {len(page_n)}")
        new_data = eeprom.read_memory(0, len(data))
        _logger.info(f"test__page_write_register: New Value = {len(new_data)}")
        for indx, init_data in enumerate(initial_data):
            assert init_data != new_data[indx]
            assert new_data[indx] == data[indx]
    
    # reset_data = [255]*EEPROMInfo.PAGE_SIZE.value*num_page
    # addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    # page_n = eeprom._EdgePiEEPROM__generate_list_of_pages(addrx, reset_data)
    # for indx, page in enumerate(page_n):
    #     eeprom._EdgePiEEPROM__page_write_register(addrx + (indx*EEPROMInfo.PAGE_SIZE.value), page)
    #     time.sleep(0.001)


def test_eeprom_reset(eeprom):
    eeprom.eeprom_reset()
    reset_vals = eeprom.read_memory(0, 16384)
    for val in reset_vals:
        assert val == 255

def test_write_json(eeprom):
    json_data = read_dummy_json(PATH+"/dummy_0.json")
    json_data_b = bytes(json.dumps(json_data), "utf-8")
    json_data = read_dummy_json(PATH+"/dummy_0.json")
    json_data_b = bytes(json.dumps(json_data), "utf-8")
    json_data_l = list(json_data_b)
    # _logger.info(f"test_write_memory: {json_data} of data to be written\n type = {type(json_data)}\n length = {len(json_data)}")
    _logger.info(f"test_write_memory: {json_data_b} of data to be written\n type = {type(json_data_b)}\n length = {len(json_data_b)}")
    # _logger.info(f"test_write_memory: {json_data_l} of data to be written\n type = {type(json_data_l)}\n length = {len(json_data_l)}")
    eeprom.write_memory(json_data_b, True)

# TODO test write to different memory location, 
# initially empty memory
def test_write_memory(eeprom):
    
    # is_full, is_empty = eeprom.init_memory()
    # assert is_empty == True
    # assert is_full == False

    # # when empty every value is 255
    # initial_data = eeprom.read_memory(0, 0x4000)
    # _logger.info(f"test_write_memory: {len(initial_data)} of initial data")
    # for data in initial_data:
    #     assert data == 255

    json_data = read_dummy_json(PATH+"/dummy_0.json")
    json_data_b = bytes(json.dumps(json_data,indent=0,sort_keys=False,separators=(',', ':')), "utf-8")
    json_data_l = list(json_data_b)
    _logger.info(f"test_write_memory: {json_data_b} of data to be written\n type = {type(json_data_b)}\n length = {len(json_data_b)}")
    _logger.info(f"test_write_memory: {json_data_l} of data to be written\n type = {type(json_data_l)}\n length = {len(json_data_l)}")
    eeprom.write_memory(json_data_b, True)
    time.sleep(0.002)
    
    # # # # new data
    new_data = eeprom.read_memory(2,len(json_data_b))
    new_data_b = bytes(new_data)
    # new_data_s = new_data_b.decode("utf-8")
    _logger.info(f"test_write_memory: {new_data} of data to be written\n type = {type(new_data)}\n length = {len(new_data)}")
    _logger.info(f"test_write_memory: {new_data_b} of new data")

    for indx, data_l in enumerate(json_data_l):
        if data_l != new_data[indx]:
            _logger.info(f"{indx}nt index, data byte = {data_l}, old = {new_data[indx]} ")
    new_data_parsed = json.loads(new_data_b)
    _logger.info(f"test_write_memory: {new_data_parsed} of new data")
    # for indx, data in enumerate(new_data_parsed):
    #     assert data == fill_data[indx]

    
