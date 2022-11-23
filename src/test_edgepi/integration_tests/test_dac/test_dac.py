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


@pytest.fixture(name="dac")
def fixture_test_edgepi_dac():
    return EdgePiDAC()


# pylint: disable=protected-access


def test_dac_init(dac):
    for ch in CH:
        assert not dac.gpio.dict_pin[dac._EdgePiDAC__analog_out_pin_map[ch.value].value].is_high


@pytest.mark.parametrize(
    "analog_out, voltage, raises",
    [
        (CH.AOUT0, LOWER_VOLT_LIMIT, does_not_raise()),
        (CH.AOUT0, 2.5, does_not_raise()),
        (CH.AOUT0, UPPER_VOLT_LIMIT, does_not_raise()),
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
        (CH.AOUT0, -0.1, pytest.raises(ValueError)),
        (CH.AOUT0, 5.118, pytest.raises(ValueError)),
        (CH.AOUT0, 5.1111, pytest.raises(ValueError)),
    ],
)
def test_dac_write_and_read_voltages(analog_out, voltage, raises, dac):
    with raises:
        dac.write_voltage(analog_out, voltage)
        assert dac.compute_expected_voltage(analog_out) == pytest.approx(voltage, abs=FLOAT_ERROR)
        if voltage > 0:
            assert dac.gpio.dict_pin[
                    dac._EdgePiDAC__analog_out_pin_map[analog_out.value].value
                ].is_high
        else:
            assert not dac.gpio.dict_pin[
                dac._EdgePiDAC__analog_out_pin_map[analog_out.value].value
            ].is_high


# TODO: test actual A/D OUT pin voltages on writes via ADC module


def test_dac_reset(dac):
    voltage = 2.2
    for ch in CH:
        dac.write_voltage(ch, voltage)

    for ch in CH:
        assert dac.compute_expected_voltage(ch) == pytest.approx(voltage, abs=FLOAT_ERROR)

    dac.reset()

    for ch in CH:
        assert dac.compute_expected_voltage(ch) == pytest.approx(0, abs=FLOAT_ERROR)
        assert not dac.gpio.dict_pin[dac._EdgePiDAC__analog_out_pin_map[ch.value].value].is_high
