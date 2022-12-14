'''unit test for edgepi_calibration'''

# pylint: disable=C0413
# pylint: disable=protected-access

from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.calibration.edgepi_calibration import EdgePiCalibration
from edgepi.calibration.eeprom_constants import ModuleNames

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/serializedFile","rb") as fd:
        b_string = fd.read()
    return b_string

# @pytest.fixture(name="calib")
# def fixture_test_dac():
#     yield EdgePiCalibration()

@pytest.mark.parametrize("module_name, result", [(ModuleNames.DAC, [0, 8]),
                                                 (ModuleNames.ADC, [1, 8]),
                                                 (ModuleNames.RTD, [2, 1]),
                                                 (ModuleNames.TC, [3, 1])])
def test_init_class(module_name, result):
    edge_calib = EdgePiCalibration(module_name)
    assert edge_calib.module == result[0]
    assert edge_calib.num_of_ch == result[1]

@pytest.mark.parametrize("module_name, num_of_points, result", [(ModuleNames.DAC, 10, 0),
                                                                (ModuleNames.ADC, 5, 0),
                                                                (ModuleNames.RTD, 2, 0),
                                                                (ModuleNames.TC,  7, 0)])
def test_generate_measurements_dict(module_name, num_of_points, result):
    edge_calib = EdgePiCalibration(module_name)
    measurements_dict = edge_calib.generate_measurements_dict(num_of_points)
    for _, value in measurements_dict.items():
        assert value['input_unit'] == result
        assert value['expected_out'] == result
        assert value['actual_out'] == result
    dict_length = len(measurements_dict.keys())
    assert dict_length == num_of_points

@pytest.mark.parametrize("module_name, num_of_points, result", [(ModuleNames.DAC, 10, 0),
                                                                (ModuleNames.ADC, 5, 0),
                                                                (ModuleNames.RTD, 2, 0),
                                                                (ModuleNames.TC,  7, 0)])
def test_generate_channel_measurements_dict(module_name, num_of_points, result):
    edge_calib = EdgePiCalibration(module_name)
    measurements_dict = edge_calib.generate_channel_measurements_dict(num_of_points)
    for ch in range(edge_calib.num_of_ch):
        for keys, _ in measurements_dict[ch].items():
            assert measurements_dict[ch][keys]['input_unit'] == result
            assert measurements_dict[ch][keys]['expected_out'] == result
            assert measurements_dict[ch][keys]['actual_out'] == result
    dict_length = len(measurements_dict.keys())
    assert dict_length == edge_calib.num_of_ch

@pytest.mark.parametrize("module_name, num_of_points, values_to_record",
                        [(ModuleNames.DAC, 10, [[2, 3.45, 5.34],
                                                [26, 3245.24, 123.13],
                                                [25, 325.224, 123.123],
                                                [56, 345.224, 12.123],
                                                [456, 3245.24, 123.123],
                                                [2456, 325.224, 123.23],
                                                [246, 3245.224, 123.123],
                                                [256, 3245.24, 123.13],
                                                [246, 325.224, 123.13],
                                                [245, 325.24, 13.123]]),
                         (ModuleNames.ADC, 5, [[2, 3.45, 5.34],
                                               [246, 325.4, 123.1],
                                               [246, 325.24, 123.3],
                                               [246, 325.22, 12.13],
                                               [246, 3.224, 1.13]]),
                         (ModuleNames.RTD, 2, [[2, 3.45, 5.34],
                                               [246, 325.224, 123.13]]),
                         (ModuleNames.TC,  7, [[2, 3.45, 5.34],
                                              [246, 325.2, 123.13],
                                              [246, 325.224, 23.13],
                                              [246, 325.224, 13.13],
                                              [246, 325.224, 12.13],
                                              [246, 325.224, 123.3],
                                              [246, 325.224, 123.1]])
                        ])
def test_record_measurements(module_name, num_of_points, values_to_record):
    edge_calib = EdgePiCalibration(module_name)
    measurements_dict = edge_calib.generate_measurements_dict(num_of_points)
    for key, value_dict in measurements_dict.items():
        edge_calib.record_measurements(value_dict, values_to_record[key][0],
                                                   values_to_record[key][1],
                                                   values_to_record[key][2])
        assert value_dict['input_unit'] != 0
        assert value_dict['expected_out'] != 0
        assert value_dict['actual_out'] != 0
