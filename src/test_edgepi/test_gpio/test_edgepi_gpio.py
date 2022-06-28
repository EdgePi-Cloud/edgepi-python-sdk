import pytest
from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from edgepi.gpio.gpio_configs import *
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

@pytest.fixture(name='gpio')
def fixture_test_edgepi_tc(mocker):
    mocker.patch('edgepi.peripherals.i2c.I2C')
    mocker.patch('edgepi.peripherals.gpio.GPIO')

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