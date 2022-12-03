"""unit tests for edgepi_gpio module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.gpio.gpio_configs import generate_expander_pin_info, generate_gpiochip_pin_info
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

def test_edgepi_gpio_init(mocker):
    mocker.patch('edgepi.peripherals.i2c.I2C')
    mocker.patch('edgepi.peripherals.gpio.GPIO')
    edgepi_gpio = EdgePiGPIO()
    expander_pin_dict = generate_expander_pin_info()
    gpiochip_pin_dict = generate_gpiochip_pin_info()
    assert edgepi_gpio.expander_pin_dict == expander_pin_dict
    assert edgepi_gpio.gpiochip_pins_dict == gpiochip_pin_dict

@pytest.mark.parametrize("pin_name, mock_value, result", [('AO_EN1',[True, None], True),
                                                          ('DIN1',[None, True], True)])
def test_edgepi_gpio_read_pin_state(mocker, pin_name, mock_value, result):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.read_gpio_pin_state',
                  return_value = mock_value[1])
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.read_expander_pin",
                  return_value = mock_value[0])
    edgepi_gpio = EdgePiGPIO()
    state = edgepi_gpio.read_pin_state(pin_name)
    assert state == result
