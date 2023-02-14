'''unit test for access eeprom'''

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))

from contextlib import nullcontext as does_not_raise
import json
import pytest

from edgepi.calibration.eeprom_constants import MessageFieldNumber, EdgePiMemoryInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM, MemoryOutOfBound
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

@pytest.fixture(name="eeprom")
def fixture_test_dac():
    eeprom = EdgePiEEPROM()
    eeprom.init_memory()
    return eeprom

def read_dummy_json(file_name: str):
    with open(PATH +"/"+file_name, "r") as f:
        dummy = json.loads(f.read())
    return dummy

@pytest.mark.parametrize("data",
                        [
                         
                        ])
def test__byte_write_register(data, eeprom):
check =1


@pytest.mark.parametrize("data",
                        [
                         
                        ])
def test__page_write_register(data, eeprom):
    check =1



@pytest.mark.parametrize("data",
                        [
                         (read_dummy_json("dummy_0.json"))
                        ])
def test_write_memory(data, eeprom):
    dummy = bytes(data)
    

