"""unit test for dac module"""

# pylint: disable=C0413
from unittest import mock
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.dac.dac_constants import DACChannel as CH
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_constants import EdgePiDacCalibrationConstants as CALIB_CONSTS, PowerMode
from edgepi.calibration.calibration_constants import CalibParam

dummy_calib_param_dict = {0:CalibParam(gain=1,offset=0),
                          1:CalibParam(gain=1,offset=0),
                          2:CalibParam(gain=1,offset=0),
                          3:CalibParam(gain=1,offset=0),
                          4:CalibParam(gain=1,offset=0),
                          5:CalibParam(gain=1,offset=0),
                          6:CalibParam(gain=1,offset=0),
                          7:CalibParam(gain=1,offset=0)}

@pytest.fixture(name="dac_ops")
def fixture_test_dac_ops(mocker):
    mocker.patch("edgepi.peripherals.i2c.I2C")
    dac_calib_params = dummy_calib_param_dict
    dac_ops = DACCommands(dac_calib_params)
    return dac_ops


# Combine command needs check for interger numbers for op-code, channel and value
# It also needs to check the range of each value.


@pytest.mark.parametrize(
    "sample, result",
    [
        ([1], True),
        ([1, 2, 3, 4, 5], True),
        ([-1, 1, 2, 3], True),
        ([444, 22, 3333, 5], True),
        ([-111, -2222], True),
    ],
)
def test_dac_check_for_int(sample, result, dac_ops):
    assert dac_ops.check_for_int(sample) == result


@pytest.mark.parametrize(
    "sample, error",
    [
        ([1, 2.22, 3, 4, 0], ValueError),
        ([None, 1, 2, 3], ValueError),
        ([], ValueError),
        ([-1, -2.22], ValueError),
    ],
)
def test_dac_check_for_int_exception(sample, error, dac_ops):
    with pytest.raises(Exception) as err:
        dac_ops.check_for_int(sample)
    assert err.type is error


@pytest.mark.parametrize(
    "range_min, target, range_max, result",
    [(0, 0, 10, True),
     (0, 5, 10, True),
     (0.5, 1, 1.1, True)],
)
def test_dac_check_range(range_min, target, range_max, result, dac_ops):
    assert dac_ops.check_range(target, range_min, range_max) == result


@pytest.mark.parametrize(
    "range_min, target, range_max, error",
    [
        (0, -1, len(CH), ValueError),
        (0, 11, len(CH), ValueError),
        (0, -5, CALIB_CONSTS.RANGE.value, ValueError),
        (0, 65536, (CALIB_CONSTS.RANGE.value)-1, ValueError),
    ],
)
def test_dac_check_range_raises(range_min, target, range_max, error, dac_ops):
    with pytest.raises(Exception) as err:
        dac_ops.check_range(target, range_min, range_max)
    assert err.type is error


@pytest.mark.parametrize(
    "a, b, c, d",
    [
        (3, 1, 1000, [49, 3, 232]),
        (3, 0, 1000, [48, 3, 232]),
        (3, 3, 1000, [51, 3, 232]),
    ],
)
def test_dac_combine_command(a, b, c, d, dac_ops):
    # pylint: disable=invalid-name
    assert dac_ops.combine_command(a, b, c) == d


@pytest.mark.parametrize(
    "a, b, c",
    [(1, 1000, [49, 3, 232]), (0, 1000, [48, 3, 232]), (3, 1000, [51, 3, 232])],
)
def test_dac_generate_write_and_update_command(a, b, c, dac_ops):
    # pylint: disable=invalid-name
    assert dac_ops.generate_write_and_update_command(a, b) == c


# voltage to code conversion
# voltage = positive floating number 0~5V ideally
# code = positive integer number 0~65535
# rounding up/down during conversion ?


@pytest.mark.parametrize("ch, expected, dac_gain, result",
                        [
(0, 0.5 , 1, 6553.5),
(1, 1 , 1, 13107),
(2, 1.5 , 1, 19660.5),
(3, 2 , 1, 26214),
(4, 2.5 , 1, 32767.5),
(5, 3 , 1, 39321),
(6, 3.5 , 1, 45874.5),
(7, 4 , 1, 52428),
(0, 4.5 , 1, 58981.5),
(1, 5 , 1, 65535),
(2, 0.5 ,2,3276.75),
(3, 1	 ,2,6553.5),
(4, 1.5 ,2,9830.25),
(5, 2	 ,2,13107),
(6, 2.5 ,2,16383.75),
(7, 3	 ,2,19660.5),
(0, 3.5 ,2,22937.25),
(1, 4	 ,2,26214),
(2, 4.5 ,2,29490.75),
(3, 5	 ,2,32767.5),
(4, 5.5 ,2,36044.25),
(5, 6	 ,2,39321),
(6, 6.5 ,2,42597.75),
(7, 7	 ,2,45874.5),
(0, 7.5 ,2,49151.25),
(2, 8	 ,2,52428),
(3, 8.5 ,2,55704.75),
(4, 9	 ,2,58981.5),
(5, 9.5 ,2,62258.25),
(6, 10  ,2,65535),
                         ])
def test_dac_voltage_to_code(ch, expected, dac_gain, result, dac_ops):
    assert dac_ops.voltage_to_code(ch, expected, dac_gain) == round(result)


@pytest.mark.parametrize(
    "ch, code, dac_gain, result",
    [
        (1, 5000, 1, 0.3814755474),
        (2, 10000, 1, 0.7629510948),
        (3, 15000, 1, 1.144426642),
        (4, 20000, 1, 1.52590219),
        (5, 25000, 1, 1.907377737),
        (6, 30000, 1, 2.288853285),
        (7, 35000, 1, 2.670328832),
        (0, 40000, 1, 3.051804379),
        (1, 45000, 1, 3.433279927),
        (2, 50000, 1, 3.814755474),
        (3, 55000, 1, 4.196231022),
        (4, 60000, 1, 4.577706569),
        (5, 65000, 1, 4.959182116),
        (6, 5000, 2, 0.7629510948),
        (7, 10000, 2, 1.52590219),
        (0, 15000, 2, 2.288853285),
        (1, 20000, 2, 3.051804379),
        (2, 25000, 2, 3.814755474),
        (3, 30000, 2, 4.577706569),
        (4, 35000, 2, 5.340657664),
        (5, 40000, 2, 6.103608759),
        (6, 45000, 2, 6.866559854),
        (7, 50000, 2, 7.629510948),
        (0, 55000, 2, 8.392462043),
        (1, 60000, 2, 9.155413138),
        (2, 65000, 2, 9.918364233),
    ],
)
def test_dac_code_to_voltage(ch, code, dac_gain, result, dac_ops):
    assert pytest.approx(dac_ops.code_to_voltage(ch, code, dac_gain), 0.001) == result


@pytest.mark.parametrize(
    "read_code, code_val",
    [
        ([0, 0xFF, 0xFF], 65535),
        ([0, 0, 0], 0),
        ([0, 0x75, 0x30], 30000),
    ],
)
def test_dac_extract_read_data(read_code, code_val, dac_ops):
    assert dac_ops.extract_read_data(read_code) == code_val


@pytest.mark.parametrize(
    "dac_state, expected",
    [
        ([PowerMode.NORMAL.value] * 8, 0x0000),
        ([PowerMode.POWER_DOWN_GROUND.value] + [PowerMode.NORMAL.value] * 7, 0x4000),
        ([PowerMode.POWER_DOWN_3_STATE.value] + [PowerMode.NORMAL.value] * 7, 0xC000),
        (
            [
                PowerMode.NORMAL.value,
                PowerMode.POWER_DOWN_GROUND.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
            ],
            0x1000,
        ),
        (
            [
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.POWER_DOWN_GROUND.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
            ],
            0x0400,
        ),
        (
            [
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.POWER_DOWN_GROUND.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
            ],
            0x0100,
        ),
        (
            [
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.POWER_DOWN_GROUND.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
            ],
            0x0040,
        ),
        (
            [
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.POWER_DOWN_GROUND.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
            ],
            0x0010,
        ),
        (
            [
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.POWER_DOWN_GROUND.value,
                PowerMode.NORMAL.value,
            ],
            0x0004,
        ),
        (
            [
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.NORMAL.value,
                PowerMode.POWER_DOWN_GROUND.value,
            ],
            0x0001,
        ),
    ],
)
def test_dac_generate_power_code(dac_state, expected, dac_ops):
    assert dac_ops.generate_power_code(dac_state) == expected


def test_dac_voltage_precisions(dac_ops):
    """checking if any mV value between 0-5V raises conversion error"""
    i = 0
    step = 0.001
    while i < 5.0:
        dac_ops.voltage_to_code(1, i, 1)
        i += step
    while i < 10.0:
        dac_ops.voltage_to_code(1, i, 2)
        i += step
