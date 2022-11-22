'''unit test for access eeprom'''
# pylint: disable=C0413
# pylint: disable=no-member
from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

from edgepi.calibration.eeprom_constants import EdgePiEEPROMData, Keys
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/serializedFile","rb") as fd:
        b_string = fd.read()
    return b_string

def test_edgepi_eeprom_data():
    memory_map = EepromLayout()
    memory_map.ParseFromString(read_binfile())
    eeprom_data = EdgePiEEPROMData()
    eeprom_data.dac_calib_parms=eeprom_data.message_to_dict(memory_map.dac)
    eeprom_data.adc_calib_parms=eeprom_data.message_to_dict(memory_map.adc)
    eeprom_data.rtd_calib_parms=eeprom_data.message_to_dict(memory_map.rtd)
    eeprom_data.tc_calib_parms=eeprom_data.message_to_dict(memory_map.tc)
    eeprom_data.config_key=eeprom_data.keys_to_str(memory_map.config_key)
    eeprom_data.data_key=eeprom_data.keys_to_str(memory_map.data_key)
    eeprom_data.serial=memory_map.serial_number
    eeprom_data.model=memory_map.model
    eeprom_data.client_id=memory_map.client_id
    assert isinstance(eeprom_data.dac_calib_parms, dict)
    assert isinstance(eeprom_data.adc_calib_parms, dict)
    assert isinstance(eeprom_data.rtd_calib_parms, dict)
    assert isinstance(eeprom_data.tc_calib_parms, dict)
    assert isinstance(eeprom_data.config_key, Keys)
    assert isinstance(eeprom_data.config_key, Keys)
    assert isinstance(eeprom_data.data_key, Keys)
    assert isinstance(eeprom_data.data_key, Keys)
    assert isinstance(eeprom_data.serial, str)
    assert isinstance(eeprom_data.model, str)
    assert isinstance(eeprom_data.client_id, str)
    assert eeprom_data.dac_calib_parms == eeprom_data.message_to_dict(memory_map.dac)
    assert eeprom_data.adc_calib_parms==eeprom_data.message_to_dict(memory_map.adc)
    assert eeprom_data.rtd_calib_parms==eeprom_data.message_to_dict(memory_map.rtd)
    assert eeprom_data.tc_calib_parms==eeprom_data.message_to_dict(memory_map.tc)
    assert eeprom_data.config_key.certificate == memory_map.config_key.certificate
    assert eeprom_data.config_key.private == memory_map.config_key.private_key
    assert eeprom_data.data_key.certificate == memory_map.data_key.certificate
    assert eeprom_data.data_key.private == memory_map.data_key.private_key
    assert eeprom_data.serial == memory_map.serial_number
    assert eeprom_data.model == memory_map.model
    assert eeprom_data.client_id == memory_map.client_id
