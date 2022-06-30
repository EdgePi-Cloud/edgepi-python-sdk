import pytest
from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from edgepi.gpio.gpio_configs import *
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

@pytest.mark.parametrize("mock_expect,config, result",
                        [(['/dev/i2c-10'],'dac',[GpioConfigs.DAC.value]),
                         (['/dev/i2c-10'],'adc',[GpioConfigs.ADC.value]),
                         (['/dev/i2c-10'],'rtd',[GpioConfigs.RTD.value]),
                         (['/dev/i2c-10'],'led',[GpioConfigs.LED.value]),
                        ])
@patch('edgepi.peripherals.i2c.I2CDevice')
def test_edgepi_gpio_init(i2c_mock, mock_expect, config, result):
    i2c_mock.fd = mock_expect[0]
    gpioCtrl = EdgePiGPIO(config)
    assert gpioCtrl.config == result[0]

# generate_write_message with default values and state
# trnsfer_message
# return pin state
# def test_edgepi_gpio_set_default():

@pytest.mark.parametrize("config, dev_address, out",
                        [('dac',32, [255]),
                         ('adc',33, [255]),
                         ('rtd',33, [255]),
                         ('led',32, [255]),
                        ])                                         
def test_edgepi_gpio_read_register(config, dev_address, out):
    gpioCtrl = EdgePiGPIO(config)
    out_data = gpioCtrl._EdgePiGPIO__read_register(gpioCtrl.pinConfigAddress, dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, dev_address, out",
                        [('dac', 32, {2 : 255, 6 : 255}),
                         ('adc', 32, {3 : 255, 7 : 255}),
                         ('rtd', 33, {3 : 255, 7 : 255}),
                         ('led', 33, {3 : 255, 7 : 255}),
                        ])               
@patch.object(EdgePiGPIO, '_EdgePiGPIO__read_register')                          
def test_edgepi_gpio_reg_addressToValue_dict(mock, config, dev_address, out):
    mock.return_value = 255
    gpioCtrl = EdgePiGPIO(config)
    out_data = gpioCtrl._EdgePiGPIO__reg_addressToValue_dict(dev_address)
    assert out_data == out

@pytest.mark.parametrize("config, result",
                        [('dac', [2, {2 : [255], 6 : [255]}]),
                         ('adc', [1, {2 : [255], 6 : [255]}]),
                        ])    
@patch.object(EdgePiGPIO, '_EdgePiGPIO__reg_addressToValue_dict')
def test_generate_default_reg_dict(Mock,config, result):
    Mock.return_value = {2 : [255], 6 : [255]}
    gpioCtrl = EdgePiGPIO(config)
    dict, _ = gpioCtrl.generate_default_reg_dict()
    assert len(dict) == result[0]
    assert dict[0] ==  result[1]