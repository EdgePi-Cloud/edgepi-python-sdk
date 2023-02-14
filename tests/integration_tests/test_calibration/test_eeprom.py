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

@pytest.mark.parametrize("data",
                        [
                         ([1])
                        ])
def test_reset(mocker, data, eeprom):
    eeprom.init()