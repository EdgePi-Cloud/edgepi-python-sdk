"""unit tests for edgepi_gpio module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.digital_input.digital_input_constants import DinPins
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput, InvalidPinName

@pytest.fixture(name="din")
def fixture_test_dac(mocker):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    yield EdgePiDigitalInput()

@pytest.mark.parametrize("pin_name, mock_value, result, error",
                        [(DinPins.DIN1, True, True, does_not_raise()),
                         (DinPins.DIN2, True, True, does_not_raise()),
                         (DinPins.DIN3, True, True, does_not_raise()),
                         (DinPins.DIN4, True, True, does_not_raise()),
                         (DinPins.DIN5, True, True, does_not_raise()),
                         (DinPins.DIN6, True, True, does_not_raise()),
                         (DinPins.DIN7, True, True, does_not_raise()),
                         (DinPins.DIN8, True, True, does_not_raise()),
                         (DinPins.DIN1, False, False, does_not_raise()),
                         (DinPins.DIN2, False, False, does_not_raise()),
                         (DinPins.DIN3, False, False, does_not_raise()),
                         (DinPins.DIN4, False, False, does_not_raise()),
                         (DinPins.DIN5, False, False, does_not_raise()),
                         (DinPins.DIN6, False, False, does_not_raise()),
                         (DinPins.DIN7, False, False, does_not_raise()),
                         (DinPins.DIN8, False, False, does_not_raise()),
                         (GpioPins.DOUT2, False, False, pytest.raises(InvalidPinName)),
                         (None, False, False, pytest.raises(InvalidPinName))])
def test_edgepi_digital_input_state(mocker, pin_name, mock_value, result, error, din):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.read_din_state",
                 return_value = mock_value)
    with error:
        state = din.digital_input_state(pin_name)
        assert state == result

@pytest.mark.parametrize(
    "pin_names, mock_values, error",
    [
        ([DinPins.DIN1], [True], does_not_raise()),
        ([DinPins.DIN2], [True], does_not_raise()),
        ([DinPins.DIN3, DinPins.DIN4, DinPins.DIN5], [True, False, True], does_not_raise()),
        (
            [DinPins.DIN1, DinPins.DIN6, DinPins.DIN7, DinPins.DIN8],
            [True, True, True, True],
            does_not_raise(),
        ),
        (
            [
                DinPins.DIN1, DinPins.DIN2, DinPins.DIN3, DinPins.DIN4,
                DinPins.DIN5, DinPins.DIN6, DinPins.DIN7, DinPins.DIN8,
            ],
            [True, True, True, True, True, False, True, False],
            does_not_raise(),
        ),
        ([DinPins.DIN2, DinPins.DIN2, DinPins.DIN2], [False, False, False], does_not_raise()),
        ([], [], pytest.raises(ValueError)),
        (None, [], pytest.raises(ValueError)),
        ([GpioPins.DOUT2], [], pytest.raises(InvalidPinName)),
        ([DinPins.DIN2, GpioPins.DOUT2], [False], pytest.raises(InvalidPinName)),
        ([DinPins.DIN2, None, DinPins.DIN3], [False, False], pytest.raises(InvalidPinName)),
    ]
)
def test_edgepi_digital_input_state_batch(mocker, pin_names, mock_values, error, din):
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.batch_read_din_state",
        return_value = mock_values
    )
    with error:
        state_list = din.digital_input_state_batch(pin_names)
        assert state_list == mock_values
