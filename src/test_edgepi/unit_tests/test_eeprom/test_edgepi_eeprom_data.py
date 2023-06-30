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

from edgepi.eeprom.edgepi_eeprom_data import EepromDataClass
from edgepi.eeprom.generated_pb2 import edgepi_module_pb2

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/edgepi_default_bin","rb") as fd:
        b_string = fd.read()
    return b_string

def test_init_data_class():
    edgepi_eeprom_data = EepromDataClass()
    edgepi_eeprom_pb = edgepi_module_pb2.EepromData()
    assert edgepi_eeprom_pb.ByteSize() == 0
    for attr in edgepi_eeprom_data.__annotations__:
        assert getattr(edgepi_eeprom_data, attr) is None


def test_deserialize_pb():
    default_bin = read_binfile()
    edgepi_eeprom_pb = edgepi_module_pb2.EepromData()
    edgepi_eeprom_pb.ParseFromString(default_bin)
    edgepi_eeprom_data = EepromDataClass.extract_eeprom_data(edgepi_eeprom_pb)
    for attr in edgepi_eeprom_data.__annotations__:
        assert getattr(edgepi_eeprom_data, attr) is not None

def test_serialize_pb():
    default_bin = read_binfile()
    edgepi_eeprom_pb = edgepi_module_pb2.EepromData()
    edgepi_eeprom_pb_2 = edgepi_module_pb2.EepromData()
    edgepi_eeprom_pb_2.ParseFromString(default_bin)
    assert edgepi_eeprom_pb.ByteSize() == 0
    edgepi_eeprom_data = EepromDataClass.extract_eeprom_data(edgepi_eeprom_pb_2)
    edgepi_eeprom_data.populate_eeprom_module(edgepi_eeprom_pb)
    assert edgepi_eeprom_pb.ByteSize() != 0
