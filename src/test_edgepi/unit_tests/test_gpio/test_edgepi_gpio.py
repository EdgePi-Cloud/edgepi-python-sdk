"""unit tests for edgepi_gpio module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
import pytest
from edgepi.gpio.gpio_configs import GpioConfigs, generate_pin_info
from edgepi.gpio.gpio_commands import check_multiple_dev
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

@pytest.fixture(name='mock_i2c')
def fixture_mock_i2c_lib(mocker):
    yield mocker.patch('edgepi.peripherals.i2c.I2C')

@pytest.mark.parametrize("mock_expect,config, result",
                        [(['/dev/i2c-10'],GpioConfigs.DAC.value,[GpioConfigs.DAC.value,6,2]),
                         (['/dev/i2c-10'],GpioConfigs.ADC.value,[GpioConfigs.ADC.value,7,3]),
                         (['/dev/i2c-10'],GpioConfigs.RTD.value,[GpioConfigs.RTD.value,7,3]),
                         (['/dev/i2c-10'],GpioConfigs.LED.value,[GpioConfigs.LED.value,7,3]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
def test_edgepi_gpio_init(mock_i2c_device, mock_expect, config, result, mock_i2c):
    mock_i2c.return_value = None
    mock_i2c_device.fd = mock_expect[0]
    gpio_ctrl = EdgePiGPIO(config)
    assert gpio_ctrl.config == result[0]
    assert gpio_ctrl.pin_config_address == result[1]
    assert gpio_ctrl.pin_out_address == result[2]

# generate_write_message with default values and state
# trnsfer_message
# return pin state
# def test_edgepi_gpio_set_default():

@pytest.mark.parametrize("config, dev_address, out",
                        [(GpioConfigs.DAC.value,32, 255),
                         (GpioConfigs.ADC.value,33, 255),
                         (GpioConfigs.RTD.value,33, 255),
                         (GpioConfigs.LED.value,32, 255),
                        ])
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_read_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')
def test_edgepi_gpio_read_register(mock_data, mock_msg, config, dev_address, out, mock_i2c):
    mock_i2c.return_value = None
    mock_msg.data = [255]
    mock_msg.return_value = (mock_msg ,mock_msg)
    mock_data.return_value = out
    gpio_ctrl = EdgePiGPIO(config)
    out_data = gpio_ctrl._EdgePiGPIO__read_register(gpio_ctrl.pin_config_address, dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, dev_address, out",
                        [(GpioConfigs.DAC.value, 32, {2 : 255, 6 : 255}),
                         (GpioConfigs.ADC.value, 32, {3 : 255, 7 : 255}),
                         (GpioConfigs.RTD.value, 33, {3 : 255, 7 : 255}),
                         (GpioConfigs.LED.value, 33, {3 : 255, 7 : 255}),
                        ])
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO._EdgePiGPIO__read_register')
def test_edgepi_gpio_map_reg_address_value_dict(mock_data, config, dev_address, out, mock_i2c):
    mock_i2c.return_value = None
    mock_data.return_value = 255
    gpio_ctrl = EdgePiGPIO(config)
    out_data = gpio_ctrl._EdgePiGPIO__map_reg_address_value_dict(dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, result",
                        [(GpioConfigs.DAC.value, {32:{2 : 255, 6 : 255}, 33:{2 : 255, 6 : 255}}),
                         (GpioConfigs.ADC.value, {33:{2 : 255, 6 : 255}}),
                        ])
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO._EdgePiGPIO__map_reg_address_value_dict')
def test_generate_default_reg_dict(mock_dict,config, result, mock_i2c):
    mock_i2c.return_value = None
    mock_dict.side_effect = [{2 : 255, 6 : 255}, {2 : 255, 6 : 255}]
    gpio_ctrl = EdgePiGPIO(config)
    pin_dict = generate_pin_info(config)
    list_address = check_multiple_dev(pin_dict)
    list_dict= gpio_ctrl._EdgePiGPIO__generate_default_reg_dict(list_address)
    assert list_dict == result


@pytest.mark.parametrize("config, mock_vals, result",[
                        (GpioConfigs.DAC.value,
                         [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, [0]],
                         {32: {2 : 0, 6 : 0}, 33: {2 : 0, 6 : 0}}),
                        (GpioConfigs.ADC.value,
                         [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, [252]],
                         {33:{2 : 252, 6 : 252}}),
                        (GpioConfigs.RTD.value,
                         [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, [254]],
                         {33:{2 : 254, 6 : 254}}),
                        (GpioConfigs.LED.value,
                         [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, [0]],
                         {32:{2 : 0, 6 : 0}}),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO._EdgePiGPIO__map_reg_address_value_dict')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_write_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_read_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')
def test_set_expander_default(mock_transfer,
                              mock_set_read_msg,
                              mock_set_write_msg,
                              mock_map_address_value_dict,
                              mock_i2c_device,
                              config,
                              mock_vals,
                              result,
                              mock_i2c):
    mock_i2c.return_value = None
    mock_transfer.return_value = mock_vals[4]
    mock_set_read_msg.return_value = mock_vals[1]
    mock_set_write_msg.return_value = mock_vals[2]
    mock_map_address_value_dict.side_effect = [{2 : 255, 6 : 255},{2 : 255, 6 : 255}]
    mock_i2c_device.return_value = mock_vals[0]
    gpio_ctrl = EdgePiGPIO(config)
    gpio_ctrl.set_expander_default()
    assert gpio_ctrl.dict_default_reg_dict == result



@pytest.mark.parametrize("config, pin_name, mock_value, result", [(GpioConfigs.DAC.value,
                                                                   'AO_EN1',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {32:{2:0, 6:0},
                                                                     33:{2:0, 6:0}}],
                                                                   [True, True, {2:128, 6:0}]
                                                                  ),
                                                                  (GpioConfigs.DAC.value,
                                                                   'AO_EN2',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {32:{2:128, 6:0},
                                                                     33:{2:0, 6:0}}],
                                                                   [True, True, {2:144, 6:0}]
                                                                  ),
                                                                  (GpioConfigs.DAC.value,
                                                                   'AO_EN6',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {32:{2:144, 6:0},
                                                                     33:{2:0, 6:0}}],
                                                                   [True, True, {2:148, 6:0}]
                                                                  ),
                                                                  (GpioConfigs.ADC.value,
                                                                   'GNDSW_IN1',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {33:{3:0, 7:0}}],
                                                                   [True, True, {3:2, 7:0}]
                                                                  ),
                                                                  (GpioConfigs.ADC.value,
                                                                   'GNDSW_IN2',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {33:{3:2, 7:0}}],
                                                                   [True, True, {3:6, 7:0}]
                                                                  )
                                                                 ])
@patch('edgepi.peripherals.i2c.I2CDevice')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_write_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_read_msg')
def test_set_expander_pin(mock_set_read_msg, mock_set_write_msg, mock_transfer, mock_i2c_device,
                          config, pin_name, mock_value, result, mock_i2c):
    mock_i2c.return_value = mock_value[0]
    mock_i2c_device.return_value = mock_value[1]
    mock_transfer.return_value = mock_value[2]
    mock_set_read_msg.return_value = mock_value[3]
    mock_set_write_msg.return_value = mock_value[4]
    gpio_ctrl = EdgePiGPIO(config)
    gpio_ctrl.dict_default_reg_dict = mock_value[5]
    gpio_ctrl.set_expander_pin(pin_name)
    assert gpio_ctrl.dict_pin[pin_name].is_high == result[1]
    assert gpio_ctrl.dict_default_reg_dict[gpio_ctrl.dict_pin[pin_name].address] == result[2]

@pytest.mark.parametrize("config, pin_name, mock_value, result", [(GpioConfigs.DAC.value,
                                                                   'AO_EN1',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {32:{2:148, 6:0},
                                                                     33:{2:0, 6:0}}],
                                                                   [False, False, {2:20, 6:0}]
                                                                  ),
                                                                  (GpioConfigs.DAC.value,
                                                                   'AO_EN2',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {32:{2:255, 6:0},
                                                                     33:{2:0, 6:0}}],
                                                                   [False, False, {2:239, 6:0}]
                                                                  ),
                                                                  (GpioConfigs.DAC.value,
                                                                   'AO_EN6',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {32:{2:132, 6:0},
                                                                     33:{2:0, 6:0}}],
                                                                   [False, False, {2:128, 6:0}]
                                                                  ),
                                                                  (GpioConfigs.ADC.value,
                                                                   'GNDSW_IN1',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {33:{3:6, 7:0}}],
                                                                   [False, False, {3:4, 7:0}]
                                                                  ),
                                                                  (GpioConfigs.ADC.value,
                                                                   'GNDSW_IN2',
                                                                   [0, 0,
                                                                    0,
                                                                    [0, 0],
                                                                    [0, 0],
                                                                    {33:{3:6, 7:0}}],
                                                                   [False, False, {3:2, 7:0}]
                                                                  )
                                                                 ])
@patch('edgepi.peripherals.i2c.I2CDevice')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_write_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_read_msg')
def test_clear_expander_pin(mock_set_read_msg, mock_set_write_msg, mock_transfer, mock_i2c_device,
                            config, pin_name, mock_value, result, mock_i2c):
    mock_i2c.return_value = mock_value[0]
    mock_i2c_device.return_value = mock_value[1]
    mock_transfer.return_value = mock_value[2]
    mock_set_read_msg.return_value = mock_value[3]
    mock_set_write_msg.return_value = mock_value[4]
    gpio_ctrl = EdgePiGPIO(config)
    gpio_ctrl.dict_default_reg_dict = mock_value[5]
    assert gpio_ctrl.clear_expander_pin(pin_name) == result[0]
    assert gpio_ctrl.dict_pin[pin_name].is_high == result[1]
    assert gpio_ctrl.dict_default_reg_dict[gpio_ctrl.dict_pin[pin_name].address] == result[2]

@pytest.mark.parametrize('mock_value, config, pin_name, result', [([0,0,True,False,False],
                                                                   GpioConfigs.DAC.value,
                                                                   'AO_EN1',
                                                                   True),
                                                                  ([0,0,True,False,True],
                                                                   GpioConfigs.DAC.value,
                                                                   'AO_EN1',
                                                                   False)])
@patch('edgepi.peripherals.i2c.I2CDevice')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.clear_expander_pin')
def test_toggle_expander_pin(mock_clear_expander_pin, mock_set_expander_pin, mock_i2c_device,
                             mock_value, config, pin_name, result, mock_i2c):
    mock_i2c.return_value = mock_value[0]
    mock_i2c_device.return_value = mock_value[1]
    mock_set_expander_pin.return_value = mock_value[2]
    mock_clear_expander_pin.return_value = mock_value[3]
    gpio_ctrl = EdgePiGPIO(config)
    gpio_ctrl.dict_pin[pin_name].is_high = mock_value[4]
    gpio_ctrl.toggle_expander_pin(pin_name)
    assert gpio_ctrl.dict_pin[pin_name].is_high == result
