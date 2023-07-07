"""
Hardware-dependent integration tests for DAC

Requirements:
    - SPI, I2C capable device
    - AD5676 DAC
    - EdgePi analog out (AO_ENx) GPIO pin mapping (see edgepi.gpio)
"""

from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.dac.dac_constants import UPPER_LIMIT, DACChannel as CH
from edgepi.dac.edgepi_dac import EdgePiDAC


UPPER_VOLT_LIMIT = UPPER_LIMIT  # upper code limit with 3 dec place precision
LOWER_VOLT_LIMIT = 0  # lower code limit
NUM_PINS = 8
FLOAT_ERROR = 1e-3
STORE_ERROR = 1e-3


@pytest.fixture(name="dac")
def fixture_test_edgepi_dac():
    return EdgePiDAC()


# pylint: disable=protected-access


def test_dac_init(dac):
    for ch in CH:
        # pylint: disable=line-too-long
        assert not dac.gpio.expander_pin_dict[dac._EdgePiDAC__analog_out_pin_map[ch.value].value].is_high


@pytest.mark.parametrize(
    "analog_out, voltage, raises",
    [
        (CH.AOUT1, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT1, 2.5, does_not_raise()),
        (CH.AOUT1, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT2, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT2, 2.5, does_not_raise()),
        (CH.AOUT2, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT3, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT3, 2.5, does_not_raise()),
        (CH.AOUT3, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT4, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT4, 2.5, does_not_raise()),
        (CH.AOUT4, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT5, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT5, 2.5, does_not_raise()),
        (CH.AOUT5, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT6, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT6, 2.5, does_not_raise()),
        (CH.AOUT6, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT7, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT7, 2.5, does_not_raise()),
        (CH.AOUT7, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT8, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT8, 2.5, does_not_raise()),
        (CH.AOUT8, UPPER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT1, -0.1, pytest.raises(ValueError)),
        (CH.AOUT2, 5.118, pytest.raises(ValueError)),
        (CH.AOUT3, 5.1111, pytest.raises(ValueError)),
    ],
)
def test_dac_write_and_read_voltages(analog_out, voltage, raises, dac):
    with raises:
        # expected_voltage = (voltage)*dac.dac_ops.dict_calib_param[analog_out.value].gain -\
        #  dac.dac_ops.dict_calib_param[analog_out.value].offset
        dac.write_voltage(analog_out, voltage)
        code, voltage_val, gain_state = dac.get_state(analog_out, True, True, True)
        dac_gain = 2 if gain_state else 1
        expected_voltage = dac.dac_ops.code_to_voltage(analog_out.value, code, dac_gain)
        assert voltage_val == pytest.approx(expected_voltage, abs=STORE_ERROR)
        assert code == dac.dac_ops.voltage_to_code(analog_out.value, voltage, dac_gain)

@pytest.mark.parametrize(
    "gain_enable",
    [True,
     False,
    ],
)
def test_dac_gain(gain_enable,dac):
    dac.set_dac_gain(not gain_enable)
    _, _, initial_gain_state = dac.get_state(None, False, False, True)
    gain_state = dac.set_dac_gain(gain_enable)
    assert initial_gain_state != gain_state
    dac.set_dac_gain(False)

def test_dac_reset(dac):
    voltage = 2.2
    for ch in CH:
        dac.write_voltage(ch, voltage)
        code, _, gain_state = dac.get_state(ch, True, True, True)
        dac_gain = 2 if gain_state else 1
        expected_voltage = dac.dac_ops.code_to_voltage(ch.value, code, dac_gain)
        assert expected_voltage == pytest.approx(voltage, abs=FLOAT_ERROR)

    dac.reset()

    for ch in CH:
        code, _, gain_state = dac.get_state(ch, True, True, True)
        dac_gain = 2 if gain_state else 1
        expected_voltage = dac.dac_ops.code_to_voltage(ch.value, code, dac_gain)
        # pylint: disable=line-too-long
        assert expected_voltage == pytest.approx(dac.dac_ops.dict_calib_param[ch.value].offset , abs=STORE_ERROR)
        # pylint: disable=line-too-long
        assert dac.gpio.expander_pin_dict[dac._EdgePiDAC__analog_out_pin_map[ch.value].value].is_high
