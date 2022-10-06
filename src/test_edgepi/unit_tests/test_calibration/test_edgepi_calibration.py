'''unit test for edgepi_calibration'''

# pylint: disable=C0413

from unittest import mock
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.calibration.edgepi_calibration import EdgePiCalibration
from edgepi.calibration.calibration_constants import ConvParam
from edgepi.calibration.eeprom_constants import ModuleNames

# @pytest.fixture(name="calib")
# def fixture_test_dac():
#     yield EdgePiCalibration()

@pytest.mark.parametrize("module_name, result", [(ModuleNames.DAC, [0, 8]),
                                                 (ModuleNames.ADC, [1, 8]),
                                                 (ModuleNames.RTD, [2, 1]),
                                                 (ModuleNames.TC, [3, 1])])
def test_init_class(module_name, result):
    edge_calib = EdgePiCalibration(module_name)
    assert edge_calib.module.value == result[0]
    assert edge_calib.num_of_ch == result[1]

@pytest.mark.parametrize("module_name, result", [(ModuleNames.DAC, [1, 0]),
                                                 (ModuleNames.ADC, [1, 0]),
                                                 (ModuleNames.RTD, [1, 0]),
                                                 (ModuleNames.TC, [1, 0])])
def test_generate_calib_param_dict(module_name, result):
    edge_calib = EdgePiCalibration(module_name)
    calib_dict = edge_calib.generate_calib_param_dict()
    for _, value in calib_dict.items():
        assert value.gain == result[0]
        assert value.offset == result[1]
    dict_length = len(calib_dict.values())
    assert dict_length == edge_calib.num_of_ch

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
                        [(ModuleNames.DAC, 10, [[2, 5.34],
                                                [26, 123.13],
                                                [25, 123.123],
                                                [56, 12.123],
                                                [456, 123.123],
                                                [2456, 123.23],
                                                [246, 123.123],
                                                [256, 123.13],
                                                [246, 123.13],
                                                [245, 13.123]]),
                         (ModuleNames.ADC, 5, [[2, 5.34],
                                               [246, 123.1],
                                               [246, 123.3],
                                               [246, 12.13],
                                               [246, 1.13]]),
                         (ModuleNames.RTD, 2, [[2, 5.34],
                                               [246, 123.13]]),
                         (ModuleNames.TC,  7, [[2, 5.34],
                                              [246, 123.13],
                                              [246, 23.13],
                                              [246, 13.13],
                                              [246, 12.13],
                                              [246, 123.3],
                                              [246, 123.1]])
                        ])
def test_record_measurements(module_name, num_of_points, values_to_record):
    edge_calib = EdgePiCalibration(module_name)
    measurements_dict = edge_calib.generate_measurements_dict(num_of_points)
    for key, value_dict in measurements_dict.items():
        edge_calib.record_measurements(value_dict, values_to_record[key][0],
                                                   values_to_record[key][1])
        assert value_dict['input_unit'] != 0
        assert value_dict['expected_out'] != 0
        assert value_dict['actual_out'] != 0

@pytest.mark.parametrize("module_name, num_of_pnts, result",
                        [(ModuleNames.DAC, 10,[[0,1,2,3,4,5,6,7,8,9],
                                               [15,25,35,45,55,65,75,85,95,105]]),
                         (ModuleNames.ADC, 10,[[0,1,2,3,4,5,6,7,8,9],
                                               [15,25,35,45,55,65,75,85,95,105]]),
                         (ModuleNames.RTD, 10,[[0,1,2,3,4,5,6,7,8,9],
                                               [15,25,35,45,55,65,75,85,95,105]]),
                         (ModuleNames.TC,  10,[[0,1,2,3,4,5,6,7,8,9],
                                               [15,25,35,45,55,65,75,85,95,105]])])
def test_prepare_variable_list(module_name, num_of_pnts, result):
    cls_calib = EdgePiCalibration(module_name)
    ch_meas_dict = cls_calib.generate_channel_measurements_dict(num_of_pnts)
    for ch, _ in ch_meas_dict.items():
        for nth_pnt in range(num_of_pnts):
            cls_calib.record_measurements(_[nth_pnt],
                                          nth_pnt*10,
                                          nth_pnt*10+15-ch)
    _x, _xx, _y, _xy = cls_calib.prepare_variable_list(ch_meas_dict)
    assert len(_x) == num_of_pnts
    result[0] = [val*10*ConvParam[module_name.name].value for val in result[0]]
    assert _x  == result[0]
    assert _xx == [i*i for i in result[0]]
    assert len(_y) == cls_calib.num_of_ch
    # iterate through y and assert on its elements
    for ch, y_n in enumerate(_y):
        for nth, dt_pnt in enumerate(y_n):
            assert dt_pnt == result[1][nth]-ch
    assert len(_xy) == cls_calib.num_of_ch
    for ch, xy_n in enumerate(_xy):
        for nth, dt_pnt in enumerate(xy_n):
            assert dt_pnt == (result[1][nth]-ch) * _x[nth]


@pytest.mark.parametrize("module_name, num_of_pnts, result",
                        [(ModuleNames.DAC, 10,[[32015.14411,32015.14411,32015.14411,32015.14411,
                                                32015.14411,32015.14411,32015.14411,32015.14411],
                                              [15,14,13,12,11,10,9,8]]),
                         (ModuleNames.ADC, 10,[[858993459.2,858993459.2,858993459.2,858993459.2,
                                                858993459.2,858993459.2,858993459.2,858993459.2],
                                               [15,14,13,12,11,10,9,8]]),
                         (ModuleNames.RTD, 10,[[1],[15]]),
                         (ModuleNames.TC,  10,[[1],[15]])])
def test_least_square_regression(module_name, num_of_pnts, result):
    cls_calib = EdgePiCalibration(module_name)
    ch_calib_dict = cls_calib.generate_calib_param_dict()
    ch_meas_dict = cls_calib.generate_channel_measurements_dict(num_of_pnts)
    for ch, _ in ch_meas_dict.items():
        for nth_pnt in range(num_of_pnts):
            cls_calib.record_measurements(_[nth_pnt],
                                          nth_pnt*10,
                                          nth_pnt*10+15-ch)
    cls_calib.least_square_regression(ch_meas_dict, ch_calib_dict)
    for key, value in ch_calib_dict.items():
        assert value.gain == pytest.approx(result[0][key])
        assert value.offset == pytest.approx(result[1][key])
