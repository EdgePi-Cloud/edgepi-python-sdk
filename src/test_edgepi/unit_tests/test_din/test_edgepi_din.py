"""unit tests for edgepi_gpio module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput, InvalidPinName

@pytest.fixture(name="din")
def fixture_test_dac(mocker):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    yield EdgePiDigitalInput()

@pytest.mark.parametrize("pin_name, mock_value, result, error",
                        [(GpioPins.DIN1, True, True, does_not_raise()),
                         (GpioPins.DIN2, True, True, does_not_raise()),
                         (GpioPins.DIN3, True, True, does_not_raise()),
                         (GpioPins.DIN4, True, True, does_not_raise()),
                         (GpioPins.DIN5, True, True, does_not_raise()),
                         (GpioPins.DIN6, True, True, does_not_raise()),
                         (GpioPins.DIN7, True, True, does_not_raise()),
                         (GpioPins.DIN8, True, True, does_not_raise()),
                         (GpioPins.DIN1, False, False, does_not_raise()),
                         (GpioPins.DIN2, False, False, does_not_raise()),
                         (GpioPins.DIN3, False, False, does_not_raise()),
                         (GpioPins.DIN4, False, False, does_not_raise()),
                         (GpioPins.DIN5, False, False, does_not_raise()),
                         (GpioPins.DIN6, False, False, does_not_raise()),
                         (GpioPins.DIN7, False, False, does_not_raise()),
                         (GpioPins.DIN8, False, False, does_not_raise()),
                         (GpioPins.DOUT2, False, False, pytest.raises(InvalidPinName)),
                         (None, False, False, pytest.raises(InvalidPinName))])
def test_edgepi_digital_input_state(mocker, pin_name, mock_value, result, error, din):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.read_gpio_pin_state",
                 return_value = mock_value)
    with error:
        state = din.digital_input_state(pin_name)
        assert state == result
    