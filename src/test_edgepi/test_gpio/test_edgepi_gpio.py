import pytest
from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from edgepi.gpio.gpio_configs import *
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

@pytest.mark.parametrize("mock_expect,config, result",
                        [(['/dev/i2c-10'],'dac',[GpioConfigs.DAC.value,6,2,[]]),
                         (['/dev/i2c-10'],'adc',[GpioConfigs.ADC.value,7,3,[]]),
                         (['/dev/i2c-10'],'rtd',[GpioConfigs.RTD.value,7,3,[]]),
                         (['/dev/i2c-10'],'led',[GpioConfigs.LED.value,7,3,[]]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
def test_edgepi_gpio_init(mock_I2CDevice, mock_expect, config, result):
    mock_I2CDevice.fd = mock_expect[0]
    gpioCtrl = EdgePiGPIO(config)
    assert gpioCtrl.config == result[0]
    assert gpioCtrl.pinConfigAddress == result[1]
    assert gpioCtrl.pinOutAddress == result[2]
    assert gpioCtrl.listRegDict == result[3]

# generate_write_message with default values and state
# trnsfer_message
# return pin state
# def test_edgepi_gpio_set_default():

@pytest.mark.parametrize("config, dev_address, out",
                        [('dac',32, 255),
                         ('adc',33, 255),
                         ('rtd',33, 255),
                         ('led',32, 255),
                        ])
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')                                  
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')                        
def test_edgepi_gpio_read_register(mock,config, dev_address, out):
    mock.return_value = out
    gpioCtrl = EdgePiGPIO(config)
    out_data = gpioCtrl._read_register(gpioCtrl.pinConfigAddress, dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, dev_address, out",
                        [('dac', 32, {2 : 255, 6 : 255}),
                         ('adc', 32, {3 : 255, 7 : 255}),
                         ('rtd', 33, {3 : 255, 7 : 255}),
                         ('led', 33, {3 : 255, 7 : 255}),
                        ])               
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.read_register')                          
def test_edgepi_gpio_reg_addressToValue_dict(mock, config, dev_address, out):
    mock.return_value = 255
    gpioCtrl = EdgePiGPIO(config)
    out_data = gpioCtrl.reg_addressToValue_dict(dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, result",
                        [('dac', [{2 : 255, 6 : 255}, {2 : 255, 6 : 255}]),
                         ('adc', [None, {2 : 255, 6 : 255}]),
                        ])    
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.reg_addressToValue_dict')  
def test_generate_default_reg_dict(Mock,config, result):
    Mock.return_value = {2 : 255, 6 : 255}
    gpioCtrl = EdgePiGPIO(config)
    dict, _ = gpioCtrl.generate_default_reg_dict()
    assert dict[0] == result[0]
    assert dict[1] ==  result[1]


@pytest.mark.parametrize("config, mock_vals, result",
                        [('dac', [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 0], [{2 : 0, 6 : 0}, {2 : 0, 6 : 0}]),
                         ('adc', [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 252], [None, {2 : 252, 6 : 252}]),
                         ('rtd', [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 254], [None, {2 : 254, 6 : 254}]),
                         ('led', [0, [0, 0], [0, 0], {2 : 255, 6 : 255}, 0], [{2 : 0, 6 : 0}, None,]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO._reg_addressToValue_dict')  
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.setWriteMsg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.setReadMsg')
@patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO.transfer')
def test_set_expander_default(mock_transfer, mock_setReadMsg, mock_setWriteMsg, mock_reg_addressToValue_dict, mock_I2CDevice, config, mock_vals, result):
    mock_transfer.return_value = mock_vals[4]
    mock_setReadMsg.return_value = mock_vals[1]
    mock_setWriteMsg.return_value = mock_vals[2]
    mock_reg_addressToValue_dict.return_value = mock_vals[3]
    mock_I2CDevice.return_value = mock_vals[0]
    gpioCtrl = EdgePiGPIO(config)
    listDict = gpioCtrl.set_expander_default()
    assert listDict[0] == result[0]
    assert listDict[1] == result[1]
