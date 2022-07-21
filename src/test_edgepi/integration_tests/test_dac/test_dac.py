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


@pytest.fixture(name="dac")
def fixture_test_edgepi_dac():
    return EdgePiDAC()


@pytest.mark.parametrize(
    "analog_out, voltage, raises",
    [
        (8, 0, does_not_raise()),  # lower code limit
        (8, 2.5, does_not_raise()),
        (8, 5.117, does_not_raise()),  # upper code limit with 3 dec place precision
        (1, 0, does_not_raise()),
        (1, 2.5, does_not_raise()),
        (1, 5.117, does_not_raise()),
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
