"""
Hardware-dependent integration tests for DAC

Requirements:
    - SPI, I2C capable device
    - AD5676 DAC
    - EdgePi analog out (AO_ENx) GPIO pin mapping (see edgepi.gpio)
"""

from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.dac.dac_constants import UPPER_LIMIT
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
    for i in range(NUM_PINS):
        assert not dac.gpio.dict_pin[dac._EdgePiDAC__analog_out_pin_map[i + 1].value].is_high


@pytest.mark.parametrize(
    "analog_out, voltage, raises",
    [
        (1, LOWER_VOLT_LIMIT, does_not_raise()),
        (1, 2.5, does_not_raise()),
        (1, UPPER_VOLT_LIMIT, does_not_raise()),
        (2, LOWER_VOLT_LIMIT, does_not_raise()),
        (2, 2.5, does_not_raise()),
        (2, UPPER_VOLT_LIMIT, does_not_raise()),
        # (3, LOWER_VOLT_LIMIT, does_not_raise()),
        # (3, 2.5, does_not_raise()),
        # (3, UPPER_VOLT_LIMIT, does_not_raise()),
        # (4, LOWER_VOLT_LIMIT, does_not_raise()),
        # (4, 2.5, does_not_raise()),
        # (4, UPPER_VOLT_LIMIT, does_not_raise()),
        # (5, LOWER_VOLT_LIMIT, does_not_raise()),
        # (5, 2.5, does_not_raise()),
        # (5, UPPER_VOLT_LIMIT, does_not_raise()),
        # (6, LOWER_VOLT_LIMIT, does_not_raise()),
        # (6, 2.5, does_not_raise()),
        # (6, UPPER_VOLT_LIMIT, does_not_raise()),
        # (7, LOWER_VOLT_LIMIT, does_not_raise()),
        # (7, 2.5, does_not_raise()),
        # (7, UPPER_VOLT_LIMIT, does_not_raise()),
        # (8, LOWER_VOLT_LIMIT, does_not_raise()),
        # (8, 2.5, does_not_raise()),
        # (8, UPPER_VOLT_LIMIT, does_not_raise()),
        # (1, -0.1, pytest.raises(ValueError)),
        # (1, 5.118, pytest.raises(ValueError)),
        # (1, 5.1111, pytest.raises(ValueError)),
        # (0, 1.1, pytest.raises(ValueError)),
        # (9, 1.1, pytest.raises(ValueError)),
    ],
)
def test_dac_write_and_read_voltages(analog_out, voltage, raises, dac):
    with raises:
        dac.write_voltage(analog_out, voltage)
        assert dac.compute_expected_voltage(analog_out) == pytest.approx(voltage, FLOAT_ERROR)
        if voltage > 0:
            assert dac.gpio.dict_pin[dac._EdgePiDAC__analog_out_pin_map[analog_out].value].is_high
        else:
            assert not dac.gpio.dict_pin[
                dac._EdgePiDAC__analog_out_pin_map[analog_out].value
            ].is_high


# TODO: test actual A/D OUT pin voltages on writes via ADC module


def test_dac_reset(dac):
    voltage = 2.2
    for i in range(NUM_PINS):
        dac.write_voltage(i + 1, voltage)

    for i in range(NUM_PINS):
        assert dac.compute_expected_voltage(i + 1) == pytest.approx(voltage, FLOAT_ERROR)

    dac.reset()

    for i in range(NUM_PINS):
        assert dac.compute_expected_voltage(i + 1) == 0
        assert not dac.gpio.dict_pin[dac._EdgePiDAC__analog_out_pin_map[i + 1].value].is_high
