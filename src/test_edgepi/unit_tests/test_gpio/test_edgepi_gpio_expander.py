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
from edgepi.gpio.gpio_configs import DACPins, generate_expander_pin_info
from edgepi.gpio.edgepi_gpio_expander import EdgePiGPIOExpander

@pytest.fixture(name='mock_i2c')
def fixture_mock_i2c_lib(mocker):
    yield mocker.patch('edgepi.peripherals.i2c.I2C')

@pytest.mark.parametrize("mock_expect, result",
                        [(['/dev/i2c-10'],[]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
def test_edgepi_expander_init(mock_i2c_device, mock_expect, result, mock_i2c):
    mock_i2c.return_value = None
    mock_i2c_device.fd = mock_expect[0]
    result = generate_expander_pin_info()
    gpio_ctrl = EdgePiGPIOExpander()
    assert gpio_ctrl.expander_pin_dict == result

@pytest.mark.parametrize("dev_address, out",
                        [(32, 255),
                         (33, 255),
                         (33, 255),
                         (32, 255),
                        ])
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_read_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.transfer')
# pylint: disable=no-member
# pylint: disable=unused-argument
def test_edgepi_expander_read_register(mock_data, mock_msg, dev_address, out, mock_i2c):
    mock_msg.data = [255]
    mock_msg.return_value = (mock_msg ,mock_msg)
    mock_data.return_value = out
    gpio_ctrl = EdgePiGPIOExpander()
    out_data = gpio_ctrl._EdgePiGPIOExpander__read_register(7,
                                                            dev_address)
    assert out_data == out
    mock_msg.assert_called_once()
    mock_data.assert_called_once()
    gpio_ctrl.i2cdev.close.assert_called_once()

@pytest.mark.parametrize("dev_address, reg_dict",
                        [(32, {7:{"value":255, "is_changed":True}}),
                         (33, {7:{"value":255, "is_changed":False}}),
                         (33, {6:{"value":255, "is_changed":True}}),
                         (32, {6:{"value":255, "is_changed":False}}),
                        ])
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_write_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.transfer')
# pylint: disable=no-member
# pylint: disable=unused-argument
def test_edgepi_expander__write_changed_values(mock_data, mock_msg, dev_address, reg_dict,mock_i2c):
    gpio_ctrl = EdgePiGPIOExpander()
    gpio_ctrl._EdgePiGPIOExpander__write_changed_values(reg_dict,
                                                            dev_address)
    for reg_addx, entry in reg_dict.items():
        if entry["is_changed"]:
            mock_msg.assert_called_once_with(reg_addx, [entry["value"]])
            mock_data.assert_called_once()
        else:
            assert mock_msg.call_count == 0
            assert mock_data.call_count == 0
    gpio_ctrl.i2cdev.close.assert_called_once()

@pytest.mark.parametrize("pin_name, mock_value, result",
                         [(DACPins.AO_EN1.value, 170, True),
                          (DACPins.AO_EN2.value, 170, False),
                          (DACPins.AO_EN3.value, 170, True),
                          (DACPins.AO_EN4.value, 170, False),
                          (DACPins.AO_EN5.value, 170, True),
                          (DACPins.AO_EN6.value, 170, False),
                          (DACPins.AO_EN7.value, 170, True),
                          (DACPins.AO_EN8.value, 170, False),
                          (DACPins.AO_EN1.value, 85, False),
                          (DACPins.AO_EN2.value, 85, True),
                          (DACPins.AO_EN3.value, 85, False),
                          (DACPins.AO_EN4.value, 85, True),
                          (DACPins.AO_EN5.value, 85, False),
                          (DACPins.AO_EN6.value, 85, True),
                          (DACPins.AO_EN7.value, 85, False),
                          (DACPins.AO_EN8.value, 85, True)])
def test_read_expander_pin_state(mocker, pin_name, mock_value, result):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
                  return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander()
    assert gpio_ctrl.read_expander_pin(pin_name) == result

@pytest.mark.parametrize("pin_name, mock_value, result",
                         [(DACPins.AO_EN1.value, 170, True),
                          (DACPins.AO_EN2.value, 170, False),
                          (DACPins.AO_EN3.value, 170, True),
                          (DACPins.AO_EN4.value, 170, False),
                          (DACPins.AO_EN5.value, 170, True),
                          (DACPins.AO_EN6.value, 170, False),
                          (DACPins.AO_EN7.value, 170, True),
                          (DACPins.AO_EN8.value, 170, False),
                          (DACPins.AO_EN1.value, 85, False),
                          (DACPins.AO_EN2.value, 85, True),
                          (DACPins.AO_EN3.value, 85, False),
                          (DACPins.AO_EN4.value, 85, True),
                          (DACPins.AO_EN5.value, 85, False),
                          (DACPins.AO_EN6.value, 85, True),
                          (DACPins.AO_EN7.value, 85, False),
                          (DACPins.AO_EN8.value, 85, True)])
def test_get_expander_pin_direction(mocker, pin_name, mock_value, result):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
                  return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander()
    assert gpio_ctrl.get_expander_pin_direction(pin_name) == result

@pytest.mark.parametrize("pin_name, mock_value",
                         [(DACPins.AO_EN4.value, 0)])
def test_clear_expander_pin(mocker, pin_name, mock_value):
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander()
    prev_pin_config = deepcopy(gpio_ctrl.expander_pin_dict[pin_name])
    gpio_ctrl.clear_expander_pin(pin_name)
    assert prev_pin_config != gpio_ctrl.expander_pin_dict[pin_name]

@pytest.mark.parametrize("pin_name, mock_value",
                         [(DACPins.AO_EN4.value, 0)])
def test_set_expander_pin(mocker, pin_name, mock_value, mock_i2c):
    mock_i2c.return_value = None
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    set_pin_dir = mocker.patch(
                        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.set_expander_pin_direction_out")
    gpio_ctrl = EdgePiGPIOExpander()
    prev_pin_config = deepcopy(gpio_ctrl.expander_pin_dict[pin_name])
    gpio_ctrl.set_expander_pin(pin_name)
    if set_pin_dir.call_count == 1:
        gpio_ctrl.expander_pin_dict[pin_name].is_out = True
    assert prev_pin_config != gpio_ctrl.expander_pin_dict[pin_name]

@pytest.mark.parametrize("pin_name, mock_value",
                         [(DACPins.AO_EN4.value, 0)])
def test_set_pin_direction_out(mocker, pin_name, mock_value, mock_i2c):
    mock_i2c.return_value = None
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    clear_pin = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander.clear_expander_pin")
    gpio_ctrl = EdgePiGPIOExpander()
    prev_pin_config = deepcopy(gpio_ctrl.expander_pin_dict[pin_name])
    gpio_ctrl.set_expander_pin_direction_out(pin_name)
    if clear_pin.call_count == 1:
        gpio_ctrl.expander_pin_dict[pin_name].is_high = False
    assert prev_pin_config != gpio_ctrl.expander_pin_dict[pin_name]

@pytest.mark.parametrize("pin_name, mock_value",
                         [(DACPins.AO_EN4.value, 0)])
def test_set_pin_direction_in(mocker, pin_name, mock_value, mock_i2c):
    mock_i2c.return_value = None
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander()
    prev_pin_config = deepcopy(gpio_ctrl.expander_pin_dict[pin_name])
    gpio_ctrl.set_expander_pin_direction_in(pin_name)
    assert prev_pin_config != gpio_ctrl.expander_pin_dict[pin_name]

@pytest.mark.parametrize("pin_name, mock_value, result",
                         [(DACPins.AO_EN1.value, 170, True),
                          (DACPins.AO_EN2.value, 170, False),
                          (DACPins.AO_EN3.value, 170, True),
                          (DACPins.AO_EN4.value, 170, False),
                          (DACPins.AO_EN5.value, 170, True),
                          (DACPins.AO_EN6.value, 170, False),
                          (DACPins.AO_EN7.value, 170, True),
                          (DACPins.AO_EN8.value, 170, False),
                          (DACPins.AO_EN1.value, 85, False),
                          (DACPins.AO_EN2.value, 85, True),
                          (DACPins.AO_EN3.value, 85, False),
                          (DACPins.AO_EN4.value, 85, True),
                          (DACPins.AO_EN5.value, 85, False),
                          (DACPins.AO_EN6.value, 85, True),
                          (DACPins.AO_EN7.value, 85, False),
                          (DACPins.AO_EN8.value, 85, True)])
def test_toggle_expander_pin(mocker, pin_name, mock_value, result):
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__apply_code_to_register")
    mocker.patch(
        "edgepi.gpio.edgepi_gpio.EdgePiGPIOExpander._EdgePiGPIOExpander__read_register",
        return_value = mock_value)
    gpio_ctrl = EdgePiGPIOExpander()
    gpio_ctrl.toggle_expander_pin(pin_name)
    assert gpio_ctrl.expander_pin_dict[pin_name] != result
