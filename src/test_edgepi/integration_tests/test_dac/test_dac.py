"""
Hardware-dependent integration tests for DAC

Requirements:
    - SPI capable device
    - AD5676 DAC
"""
# TODO: update hardware requirements after adding GPIO

from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.dac.edgepi_dac import EdgePiDAC


UPPER_VOLT_LIMIT = 5.117  # upper code limit with 3 dec place precision
LOWER_VOLT_LIMIT = 0  # lower code limit


@pytest.fixture(name="dac")
def fixture_test_edgepi_dac():
    return EdgePiDAC()


@pytest.mark.parametrize(
    "analog_out, voltage, raises",
    [
        (1, LOWER_VOLT_LIMIT, does_not_raise()),
        (1, 2.5, does_not_raise()),
        (1, UPPER_VOLT_LIMIT, does_not_raise()),
        (2, LOWER_VOLT_LIMIT, does_not_raise()),
        (2, 2.5, does_not_raise()),
        (2, UPPER_VOLT_LIMIT, does_not_raise()),
        (3, LOWER_VOLT_LIMIT, does_not_raise()),
        (3, 2.5, does_not_raise()),
        (3, UPPER_VOLT_LIMIT, does_not_raise()),
        (4, LOWER_VOLT_LIMIT, does_not_raise()),
        (4, 2.5, does_not_raise()),
        (4, UPPER_VOLT_LIMIT, does_not_raise()),
        (5, LOWER_VOLT_LIMIT, does_not_raise()),
        (5, 2.5, does_not_raise()),
        (5, UPPER_VOLT_LIMIT, does_not_raise()),
        (6, LOWER_VOLT_LIMIT, does_not_raise()),
        (6, 2.5, does_not_raise()),
        (6, UPPER_VOLT_LIMIT, does_not_raise()),
        (7, LOWER_VOLT_LIMIT, does_not_raise()),
        (7, 2.5, does_not_raise()),
        (7, UPPER_VOLT_LIMIT, does_not_raise()),
        (8, LOWER_VOLT_LIMIT, does_not_raise()),
        (8, 2.5, does_not_raise()),
        (8, UPPER_VOLT_LIMIT, does_not_raise()),
        (1, -0.1, pytest.raises(ValueError)),
        (1, 5.118, pytest.raises(ValueError)),
        (0, 1.1, pytest.raises(ValueError)),
        (9, 1.1, pytest.raises(ValueError)),
    ],
)
def test_write_and_read_voltages(analog_out, voltage, raises, dac):
    with raises:
        dac.write_voltage(analog_out, voltage)
        assert dac.read_voltage(analog_out) == voltage


# TODO: test actual A/D OUT pin voltages on write
