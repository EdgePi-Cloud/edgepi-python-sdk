"""unit tests for edgepi_gpio module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.gpio.gpio_configs import generate_expander_pin_info, generate_gpiochip_pin_info
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO, PinNameNoneError, PinNameNotFound

def test_edgepi_gpio_init(mocker):
    mocker.patch('edgepi.peripherals.i2c.I2C')
    mocker.patch('edgepi.peripherals.gpio.GPIO')
    edgepi_gpio = EdgePiGPIO()
    expander_pin_dict = generate_expander_pin_info()
    gpiochip_pin_dict = generate_gpiochip_pin_info()
    assert edgepi_gpio.expander_pin_dict == expander_pin_dict
    assert edgepi_gpio.gpiochip_pins_dict == gpiochip_pin_dict

@pytest.mark.parametrize("pin_name, error",
                        [(GpioPins.AO_EN1.value, does_not_raise()),
                         (GpioPins.DIN1.value, does_not_raise()),
                         (None, pytest.raises(PinNameNoneError)),
                         ("Does not exits", pytest.raises(PinNameNotFound))])
def test_edgepi__pin_name_check(pin_name, error):
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio._EdgePiGPIO__pin_name_check(pin_name)

@pytest.mark.parametrize("pin_name, mock_value, result, error",
                        [(GpioPins.AO_EN1.value,[True, None], True, does_not_raise()),
                         (GpioPins.DIN1.value,[None, True], True, does_not_raise()),
                         (None, [None, None], None, pytest.raises(PinNameNoneError)),
                         ("Does not exits",[None, None], None, pytest.raises(PinNameNotFound))])
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
                        [(GpioPins.DIN1.value,[None, True], does_not_raise()),
                         (None, [None, None], pytest.raises(PinNameNoneError)),
                         ("Does not exits",[None, None], pytest.raises(PinNameNotFound))])
def test_edgepi_gpio_set_pin_state(mocker, pin_name, mock_value, error):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.write_gpio_pin_state',
                  return_value = mock_value[1])
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_expander_pin",
                  return_value = mock_value[0])
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio.set_pin_state(pin_name)

@pytest.mark.parametrize("pin_name, mock_value, error",
                        [(GpioPins.DIN1.value,[None, True], does_not_raise()),
                         (None, [None, None], pytest.raises(PinNameNoneError)),
                         ("Does not exits",[None, None], pytest.raises(PinNameNotFound))])
def test_edgepi_gpio_clear_pin_state(mocker, pin_name, mock_value, error):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.write_gpio_pin_state',
                  return_value = mock_value[1])
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.clear_expander_pin",
                  return_value = mock_value[0])
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio.set_pin_state(pin_name)

@pytest.mark.parametrize("pin_name, mock_value, result, error",
                        [(GpioPins.DIN1.value,[None, None], True, does_not_raise()),
                         (GpioPins.DOUT1.value,[None, None], False, does_not_raise()),
                         (GpioPins.AO_EN1.value,[None, False], False, does_not_raise()),
                         (None, [None, None], None, pytest.raises(PinNameNoneError)),
                         ("Does not exits",[None, None], None, pytest.raises(PinNameNotFound))])
def test_edgepi_gpio_get_pin_direction(mocker, pin_name, mock_value, result, error):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.get_expander_pin_direction',
                  return_value = mock_value[1])
    edgepi_gpio = EdgePiGPIO()
    with error:
        direction = edgepi_gpio.get_pin_direction(pin_name)
        assert direction == result

@pytest.mark.parametrize("pin_name, error",
                        [(GpioPins.DIN1.value, does_not_raise()),
                         (GpioPins.DOUT1.value, does_not_raise()),
                         (GpioPins.AO_EN1.value, does_not_raise()),
                         (None, pytest.raises(PinNameNoneError)),
                         ("Does not exits", pytest.raises(PinNameNotFound))])
def test_edgepi_gpio_set_pin_direction_in(mocker, pin_name, error):
    exp = mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_expander_pin_direction_in')
    gpio = mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.set_gpio_pin_dir')
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio.set_pin_direction_in(pin_name)
        # pylint: disable = expression-not-assigned
        exp.assert_called_once_with(pin_name) if pin_name in edgepi_gpio.expander_pin_dict else \
            gpio.assert_called_once_with(pin_name, True)

@pytest.mark.parametrize("pin_name, error",
                        [(GpioPins.DIN1.value, does_not_raise()),
                         (GpioPins.DOUT1.value, does_not_raise()),
                         (GpioPins.AO_EN1.value, does_not_raise()),
                         (None, pytest.raises(PinNameNoneError)),
                         ("Does not exits", pytest.raises(PinNameNotFound))])
def test_edgepi_gpio_set_pin_direction_out(mocker, pin_name, error):
    exp = mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_expander_pin_direction_out')
    gpio = mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.set_gpio_pin_dir')
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio.set_pin_direction_out(pin_name)
        # pylint: disable = expression-not-assigned
        exp.assert_called_once_with(pin_name) if pin_name in edgepi_gpio.expander_pin_dict else \
            gpio.assert_called_once_with(pin_name, False)

@pytest.mark.parametrize("pin_name, error",
                        [(GpioPins.DIN1.value, does_not_raise()),
                         (GpioPins.DOUT1.value, does_not_raise()),
                         (GpioPins.AO_EN1.value, does_not_raise()),
                         (None, pytest.raises(PinNameNoneError)),
                         ("Does not exits", pytest.raises(PinNameNotFound))])
def test_edgepi_gpio_toggle_pin(mocker, pin_name, error):
    exp = mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.toggle_expander_pin')
    gpio = mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.toggle_gpio_pin_state')
    edgepi_gpio = EdgePiGPIO()
    with error:
        edgepi_gpio.toggle_pin(pin_name)
        # pylint: disable = expression-not-assigned
        exp.assert_called_once_with(pin_name) if pin_name in edgepi_gpio.expander_pin_dict else \
            gpio.assert_called_once_with(pin_name)
