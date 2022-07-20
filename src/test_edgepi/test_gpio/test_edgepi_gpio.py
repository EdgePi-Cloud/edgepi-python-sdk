import pytest
from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from edgepi.gpio.gpio_configs import *
from edgepi.gpio.gpio_commands import check_multiple_dev
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

@pytest.mark.parametrize("mock_expect,config, result",
                        [(['/dev/i2c-10'],GpioConfigs.DAC.value,[GpioConfigs.DAC.value,6,2]),
                         (['/dev/i2c-10'],GpioConfigs.ADC.value,[GpioConfigs.ADC.value,7,3]),
                         (['/dev/i2c-10'],GpioConfigs.RTD.value,[GpioConfigs.RTD.value,7,3]),
                         (['/dev/i2c-10'],GpioConfigs.LED.value,[GpioConfigs.LED.value,7,3]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
def test_edgepi_gpio_init(mock_I2CDevice, mock_expect, config, result):
    mock_I2CDevice.fd = mock_expect[0]
    gpioCtrl = EdgePiGPIO(config)
    assert gpioCtrl.config == result[0]
    assert gpioCtrl.pin_config_address == result[1]
    assert gpioCtrl.pin_out_address == result[2]

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
def test_edgepi_gpio_read_register(mock, mock_msg, config, dev_address, out):
    mock_msg.data = [255]
    mock_msg.return_value = (mock_msg ,mock_msg)
    mock.return_value = out
    gpioCtrl = EdgePiGPIO(config)
    out_data = gpioCtrl._EdgePiGPIO__read_register(gpioCtrl.pin_config_address, dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, dev_address, out",
                        [(GpioConfigs.DAC.value, 32, {2 : 255, 6 : 255}),
                         (GpioConfigs.ADC.value, 32, {3 : 255, 7 : 255}),
                         (GpioConfigs.RTD.value, 33, {3 : 255, 7 : 255}),
                         (GpioConfigs.LED.value, 33, {3 : 255, 7 : 255}),
                        ])               
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO._EdgePiGPIO__read_register')                          
def test_edgepi_gpio_reg_addressToValue_dict(mock, config, dev_address, out):
    mock.return_value = 255
    gpioCtrl = EdgePiGPIO(config)
    out_data = gpioCtrl._EdgePiGPIO__map_reg_address_value_dict(dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, result",
                        [(GpioConfigs.DAC.value, [{2 : 255, 6 : 255}, {2 : 255, 6 : 255}]),
                         (GpioConfigs.ADC.value, [{2 : 255, 6 : 255}]),
                        ])    
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO._EdgePiGPIO__map_reg_address_value_dict')  
def test_generate_default_reg_dict(Mock,config, result):
    Mock.side_effect = [{2 : 255, 6 : 255}, {2 : 255, 6 : 255}]
    gpioCtrl = EdgePiGPIO(config)
    dict= gpioCtrl._EdgePiGPIO__generate_default_reg_dict(check_multiple_dev(generate_pin_info(config)))
    assert dict == result


@pytest.mark.parametrize("config, mock_vals, result",
                        [(GpioConfigs.DAC.value, [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 0], [{2 : 0, 6 : 0}, {2 : 0, 6 : 0}]),
                         (GpioConfigs.ADC.value, [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 252], [{2 : 252, 6 : 252}]),
                         (GpioConfigs.RTD.value, [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 254], [{2 : 254, 6 : 254}]),
                         (GpioConfigs.LED.value, [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 0], [{2 : 0, 6 : 0}]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO._EdgePiGPIO__map_reg_address_value_dict')  
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_write_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_read_msg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')
def test_set_expander_default(mock_transfer, mock_set_read_msg, mock_set_write_msg, mock_reg_addressToValue_dict, mock_I2CDevice, config, mock_vals, result):
    mock_transfer.return_value = mock_vals[4]
    mock_set_read_msg.return_value = mock_vals[1]
    mock_set_write_msg.return_value = mock_vals[2]
    mock_reg_addressToValue_dict.side_effect = [{2 : 255, 6 : 255},{2 : 255, 6 : 255}]
    mock_I2CDevice.return_value = mock_vals[0]
    gpioCtrl = EdgePiGPIO(config)
    listDict = gpioCtrl.set_expander_default()
    assert listDict == result
