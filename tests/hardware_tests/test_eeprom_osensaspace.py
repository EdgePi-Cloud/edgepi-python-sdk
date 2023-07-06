'''hardware test for eeprom user space'''

# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# https://github.com/protocolbuffers/protobuf/issues/10372

import logging
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import time
import os
PATH = os.path.dirname(os.path.abspath(__file__))

import pytest
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM

@pytest.fixture(name="eeprom")
def fixture_test_dac():
    eeprom = EdgePiEEPROM()
    return eeprom

# Change ADC DAC Module Param
def test_osensa_space_modify_1(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.read_edgepi_data()
    time.sleep(0.5)
    eeprom_data_modify = eeprom.read_edgepi_data()
    time.sleep(0.5)

    _logger.info(f"Origin Data class {eeprom_data_origin.dac_calib_params}\n")
    _logger.info(f"Modified Data class {eeprom_data_modify.dac_calib_params}\n")

    for ch, calibs in eeprom_data_modify.dac_calib_params.extract_ch_dict().items():
        calibs.gain = ch
        calibs.offset = ch

    for ch, calibs in eeprom_data_modify.adc1_calib_params.extract_ch_dict().items():
        calibs.gain = ch
        calibs.offset = ch

    for ch, calibs in eeprom_data_modify.adc2_calib_params.extract_ch_dict().items():
        calibs.gain = ch
        calibs.offset = ch

    eeprom.write_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.read_edgepi_data()
    _logger.info(f"Origin Data class {eeprom_data_origin.dac_calib_params}\n")
    _logger.info(f"Modified Data class {eeprom_data_modify.dac_calib_params}\n")
    assert eeprom_data_origin.dac_calib_params != eeprom_data_modify.dac_calib_params
    assert eeprom_data_origin.adc1_calib_params != eeprom_data_modify.adc1_calib_params
    assert eeprom_data_origin.adc2_calib_params != eeprom_data_modify.adc2_calib_params

    eeprom.read_edgepi_data(eeprom_data_origin)

# TC and RTD modification
def test_osensa_space_modify_2(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.read_edgepi_data()
    time.sleep(5)
    eeprom_data_modify = eeprom.read_edgepi_data()
    time.sleep(5)

    eeprom_data_modify.rtd_calib_params.rtd.gain = 32.0
    eeprom_data_modify.rtd_calib_params.rtd.offset = -0.9238
    eeprom_data_modify.rtd_calib_params.rtd_resistor = 1923.48
    eeprom_data_modify.tc_calib_params.tc_B.gain = 123.0
    eeprom_data_modify.tc_calib_params.tc_B.offset = 5231.0
    eeprom_data_modify.tc_calib_params.tc_E.gain = 123.0
    eeprom_data_modify.tc_calib_params.tc_E.offset = 5231.0
    eeprom_data_modify.tc_calib_params.tc_J.gain = 123.0
    eeprom_data_modify.tc_calib_params.tc_J.offset = 5231.0

    eeprom.write_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.read_edgepi_data()

    _logger.info(f"Origin RTD Calib Params {eeprom_data_origin.rtd_calib_params}")
    _logger.info(f"Modify RTD Calib Params {eeprom_data_modify.rtd_calib_params}")
    _logger.info(f"Origin TC Calib Params {eeprom_data_origin.tc_calib_params}")
    _logger.info(f"Modify TC Calib Params {eeprom_data_modify.tc_calib_params}")

    assert eeprom_data_origin.rtd_calib_params != eeprom_data_modify.rtd_calib_params
    assert eeprom_data_origin.tc_calib_params != eeprom_data_modify.tc_calib_params

    eeprom.write_edgepi_data(eeprom_data_origin)


def test_osensa_space_modify_3(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.read_edgepi_data()
    time.sleep(0.5)
    eeprom_data_modify = eeprom.read_edgepi_data()
    time.sleep(0.5)

    eeprom_data_modify.config_key.certificate = "yeeeeeeet"
    eeprom_data_modify.config_key.private_key = "ajksbvjkalsbkvalva"
    eeprom_data_modify.data_key.certificate = "asjkdbvakjsnvjka"
    eeprom_data_modify.data_key.private_key = "lozxivhzlnjqq"

    eeprom.write_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.read_edgepi_data()

    _logger.info(f"Origin Config Key {eeprom_data_origin.config_key}")
    _logger.info(f"Origin Data Key {eeprom_data_origin.data_key}")
    _logger.info(f"Modified Config Key {eeprom_data_modify.config_key}")
    _logger.info(f"Modified Data Key {eeprom_data_modify.data_key}")

    assert eeprom_data_origin.config_key != eeprom_data_modify.config_key
    assert eeprom_data_origin.data_key != eeprom_data_modify.data_key

    eeprom.write_edgepi_data(eeprom_data_origin)
