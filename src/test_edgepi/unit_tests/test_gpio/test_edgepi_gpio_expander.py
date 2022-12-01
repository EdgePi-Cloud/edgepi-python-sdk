"""unit tests for edgepi_gpio_expander module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from copy import deepcopy

import pytest
from edgepi.gpio.gpio_configs import GpioConfigs, DACPins
from edgepi.gpio.edgepi_gpio_expander import EdgePiGPIOExpander

@pytest.fixture(name='mock_i2c')
def fixture_mock_i2c_lib(mocker):
    yield mocker.patch('edgepi.peripherals.i2c.I2C')

@pytest.mark.parametrize("mock_expect,config, result",
                        [(['/dev/i2c-10'],GpioConfigs.DAC.value,[GpioConfigs.DAC.value,7,3]),
                         (['/dev/i2c-10'],GpioConfigs.ADC.value,[GpioConfigs.ADC.value,6,2]),
                         (['/dev/i2c-10'],GpioConfigs.RTD.value,[GpioConfigs.RTD.value,6,2]),
                         (['/dev/i2c-10'],GpioConfigs.LED.value,[GpioConfigs.LED.value,6,2]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
def test_edgepi_expander_init(mock_i2c_device, mock_expect, config, result, mock_i2c):
    mock_i2c.return_value = None
    mock_i2c_device.fd = mock_expect[0]
    gpio_ctrl = EdgePiGPIOExpander(config)
    assert gpio_ctrl.pin_config_address == result[1]
    assert gpio_ctrl.pin_out_address == result[2]

@pytest.mark.parametrize("config, dev_address, out",
                        [(GpioConfigs.DAC.value,32, 255),
                         (GpioConfigs.ADC.value,33, 255),
                         (GpioConfigs.RTD.value,33, 255),
                         (GpioConfigs.LED.value,32, 255),
                        ])
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_read_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.transfer')
def test_edgepi_expander_read_register(mock_data, mock_msg, config, dev_address, out, mock_i2c):
    mock_i2c.return_value = None
    mock_msg.data = [255]
    mock_msg.return_value = (mock_msg ,mock_msg)
    mock_data.return_value = out
    gpio_ctrl = EdgePiGPIOExpander(config)
    out_data = gpio_ctrl._EdgePiGPIOExpander__read_register(gpio_ctrl.pin_config_address,
                                                            dev_address)
    assert out_data == out

# TODO: these need to be refactored to work with new methods
@pytest.mark.parametrize("config, pin_name, mock_value, result",
                         [(GpioConfigs.DAC.value, DACPins.A0_EN1.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN2.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN3.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN4.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN5.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN6.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN7.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN8.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN1.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN2.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN3.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN4.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN5.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN6.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN7.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN8.value, 85, True)])
def test_read_expander_pin_state(mocker, config, pin_name, mock_value, result):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
                  return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander(config)
    assert gpio_ctrl.read_expander_pin(pin_name) == result

@pytest.mark.parametrize("config, pin_name, mock_value, result",
                         [(GpioConfigs.DAC.value, DACPins.A0_EN1.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN2.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN3.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN4.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN5.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN6.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN7.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN8.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN1.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN2.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN3.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN4.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN5.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN6.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN7.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN8.value, 85, True)])
def test_get_pin_direction(mocker, config, pin_name, mock_value, result):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
                  return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander(config)
    assert gpio_ctrl.get_pin_direction(pin_name) == result

@pytest.mark.parametrize("config, pin_name, mock_value",
                         [(GpioConfigs.DAC.value, DACPins.A0_EN4.value, 0)])
def test_clear_expander_pin(mocker, config, pin_name, mock_value):
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander(config)
    prev_pin_config = deepcopy(gpio_ctrl.dict_pin[pin_name])
    gpio_ctrl.clear_expander_pin(pin_name)
    assert prev_pin_config != gpio_ctrl.dict_pin[pin_name]

@pytest.mark.parametrize("config, pin_name, mock_value",
                         [(GpioConfigs.DAC.value, DACPins.A0_EN4.value, 0)])
def test_set_expander_pin(mocker, config, pin_name, mock_value, mock_i2c):
    mock_i2c.return_value = None
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    set_pin_dir = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_pin_direction_out")
    gpio_ctrl = EdgePiGPIOExpander(config)
    prev_pin_config = deepcopy(gpio_ctrl.dict_pin[pin_name])
    gpio_ctrl.set_expander_pin(pin_name)
    if set_pin_dir.call_count == 1:
        gpio_ctrl.dict_pin[pin_name].is_out = True
    assert prev_pin_config != gpio_ctrl.dict_pin[pin_name]

@pytest.mark.parametrize("config, pin_name, mock_value",
                         [(GpioConfigs.DAC.value, DACPins.A0_EN4.value, 0)])
def test_set_pin_direction_out(mocker, config, pin_name, mock_value, mock_i2c):
    mock_i2c.return_value = None
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    clear_pin = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.clear_expander_pin")
    gpio_ctrl = EdgePiGPIOExpander(config)
    prev_pin_config = deepcopy(gpio_ctrl.dict_pin[pin_name])
    gpio_ctrl.set_pin_direction_out(pin_name)
    if clear_pin.call_count == 1:
        gpio_ctrl.dict_pin[pin_name].is_high = False
    assert prev_pin_config != gpio_ctrl.dict_pin[pin_name]

@pytest.mark.parametrize("config, pin_name, mock_value",
                         [(GpioConfigs.DAC.value, DACPins.A0_EN4.value, 0)])
def test_set_pin_direction_in(mocker, config, pin_name, mock_value, mock_i2c):
    mock_i2c.return_value = None
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander(config)
    prev_pin_config = deepcopy(gpio_ctrl.dict_pin[pin_name])
    gpio_ctrl.set_pin_direction_in(pin_name)
    assert prev_pin_config != gpio_ctrl.dict_pin[pin_name]

@pytest.mark.parametrize("config, pin_name, mock_value, result",
                         [(GpioConfigs.DAC.value, DACPins.A0_EN1.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN2.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN3.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN4.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN5.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN6.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN7.value, 170, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN8.value, 170, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN1.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN2.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN3.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN4.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN5.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN6.value, 85, True),
                          (GpioConfigs.DAC.value, DACPins.A0_EN7.value, 85, False),
                          (GpioConfigs.DAC.value, DACPins.A0_EN8.value, 85, True)])
def test_toggle_expander_pin(mocker, config, pin_name, mock_value, result):
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander(config)
    gpio_ctrl.toggle_expander_pin(pin_name)
    assert gpio_ctrl.dict_pin[pin_name] != result
