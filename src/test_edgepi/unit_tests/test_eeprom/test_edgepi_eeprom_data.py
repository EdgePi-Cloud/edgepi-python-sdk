'''unit test for edgepi eeprom data'''
# pylint: disable=C0413
# pylint: disable=no-member
# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372
from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.eeprom.edgepi_eeprom_data import EepromDataClass
from edgepi.eeprom.proto_files import (
    edgepi_module_pb2,
    dac_module_pb2,
    adc_module_pb2,
    rtd_module_pb2,
    tc_module_pb2
)

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/edgepi_default_bin","rb") as fd:
        b_string = fd.read()
    return b_string

def test_init_data_class():
    edgepi_eeprom_data = EepromDataClass()
    edgepi_eeprom_data = edgepi_eeprom_data.__dict__
    for val in edgepi_eeprom_data.values():
        assert val is None

