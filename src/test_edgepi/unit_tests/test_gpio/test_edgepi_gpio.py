"""unit tests for edgepi_gpio module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from contextlib import nullcontext as does_not_raise
from edgepi.gpio.gpio_configs import generate_expander_pin_info, generate_gpiochip_pin_info
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO, PinNameError

def test_edgepi_gpio_init(mocker):
    mocker.patch('edgepi.peripherals.i2c.I2C')
    mocker.patch('edgepi.peripherals.gpio.GPIO')
    edgepi_gpio = EdgePiGPIO()
    expander_pin_dict = generate_expander_pin_info()
    gpiochip_pin_dict = generate_gpiochip_pin_info()
    assert edgepi_gpio.expander_pin_dict == expander_pin_dict
    assert edgepi_gpio.gpiochip_pins_dict == gpiochip_pin_dict

@pytest.mark.parametrize("pin_name, mock_value, result, error", 
                        [(GpioPins.AO_EN1,[True, None], True, does_not_raise()),
                         (GpioPins.DIN1,[None, True], True, does_not_raise()),
                         (None, [None, None], None, pytest.raises(PinNameError))])
def test_edgepi_gpio_read_pin_state(mocker, pin_name, mock_value, result, error):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.read_gpio_pin_state',
                  return_value = mock_value[1])
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.read_expander_pin",
                  return_value = mock_value[0])
    edgepi_gpio = EdgePiGPIO()
    with error:
        state = edgepi_gpio.read_pin_state(pin_name)
        assert state == result

@pytest.mark.parametrize("pin_name, mock_value, error", 
                        [(GpioPins.DIN1,[None, True], does_not_raise()),
                         (None, [None, None], pytest.raises(PinNameError))])
def test_edgepi_gpio_set_pin_state(mocker, pin_name, mock_value, error):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.write_gpio_pin_state',
                  return_value = mock_value[1])
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.clear_expander_pin",
                  return_value = mock_value[0])
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio.set_pin_state(pin_name)

@pytest.mark.parametrize("pin_name, mock_value, error", 
                        [(GpioPins.DIN1,[None, True], does_not_raise()),
                         (None, [None, None], pytest.raises(PinNameError))])
def test_edgepi_gpio_clear_pin_state(mocker, pin_name, mock_value, error):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.write_gpio_pin_state',
                  return_value = mock_value[1])
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_expander_pin",
                  return_value = mock_value[0])
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio.set_pin_state(pin_name)