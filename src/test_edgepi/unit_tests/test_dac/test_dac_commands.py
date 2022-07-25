"""unit test for dac module"""


import pytest
from edgepi.dac.dac_constants import EdgePiDacChannel as CH
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_constants import EdgePiDacCalibrationConstants as CALIB_CONSTS, PowerMode
from edgepi.dac.dac_calibration import DAChWCalibConst, DACsWCalibConst


@pytest.fixture(name="dac_ops")
def fixture_test_dac_ops():
    dac_ops = DACCommands(DAChWCalibConst, [DACsWCalibConst] * 8)
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
    [(0, 0, 10, True), (0, 10, 10, True), (0, 5, 10, True), (0.5, 1, 1.1, True)],
)
def test_dac_check_range(range_min, target, range_max, result, dac_ops):
    assert dac_ops.check_range(target, range_min, range_max) == result


@pytest.mark.parametrize(
    "range_min, target, range_max, error",
    [
        (0, -1, len(CH), ValueError),
        (0, 11, len(CH), ValueError),
        (0, -5, CALIB_CONSTS.RANGE.value, ValueError),
        (0, 65536, CALIB_CONSTS.RANGE.value, ValueError),
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


@pytest.mark.parametrize(
    "ch, expected, result", [(1, 2.345, 30030), (0, 2.345, 30030), (3, 2.345, 30030)]
)
def test_dac_voltage_to_code(ch, expected, result, dac_ops):
    assert dac_ops.voltage_to_code(ch, expected) == result


@pytest.mark.parametrize(
    "ch, code, result",
    [
        (1, 30030, 2.345),
        (0, 30030, 2.345),
        (3, 30030, 2.345),
    ],
)
def test_dac_code_to_voltage(ch, code, result, dac_ops):
    assert dac_ops.code_to_voltage(ch, code) == result


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


@pytest.mark.parametrize(
    "voltage, result",
    [
        (0, True),
        (1.1, True),
        (3.34, True),
        (4.345, True),
        (0.1234, False),
        (1.1111, False),
        (3.3444, False),
        (4.3455, False),
    ],
)
def test_dac_validate_voltage_precision(voltage, result, dac_ops):
    assert dac_ops.validate_voltage_precision(voltage) == result
