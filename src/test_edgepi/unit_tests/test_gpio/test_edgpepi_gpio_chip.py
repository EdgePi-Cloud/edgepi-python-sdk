"""unit tests for edgepi_gpio_chip module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.digital_input.digital_input_constants import DinPins
from edgepi.gpio.gpio_configs import generate_gpiochip_pin_info
from edgepi.gpio.edgepi_gpio_chip import EdgePiGPIOChip


@pytest.fixture(name='mock_gpio')
def fixture_mock_i2c_lib(mocker):
    yield mocker.patch('edgepi.peripherals.gpio.GPIO')

def test_edgepi_gpio_init():
    gpio = EdgePiGPIOChip()
    assert gpio.gpiochip_pins_dict == generate_gpiochip_pin_info()

# pylint: disable=no-member
@pytest.mark.parametrize("pin_name, mock_value, result", [(DinPins.DIN1.value,[True], True)])
def test_read_gpio_pin_state(mocker, pin_name, mock_value, result):
    mocker.patch("edgepi.peripherals.gpio.GPIO")
    mocker.patch("edgepi.peripherals.gpio.GpioDevice.read_state", return_value = mock_value[0])
    gpio_chip = EdgePiGPIOChip()
    assert gpio_chip.read_gpio_pin_state(pin_name) == result
    gpio_chip.gpio.close.assert_called_once()

# pylint: disable=no-member
@pytest.mark.parametrize("pin_name, mock_value, result", [(DinPins.DIN1.value,[True], True),
                                                          (DinPins.DIN1.value,[False], False)])
def test_write_gpio_pin_state(mocker, pin_name, mock_value, result):
    mocker.patch("edgepi.peripherals.gpio.GPIO")
    mocker.patch("edgepi.peripherals.gpio.GpioDevice.read_state", return_value = mock_value[0])
    gpio_chip = EdgePiGPIOChip()
    assert gpio_chip.write_gpio_pin_state(pin_name, mock_value[0]) == result
    gpio_chip.gpio.close.assert_called_once()
