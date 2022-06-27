import pytest
from edgepi.gpio.gpio_commands import *
from edgepi.gpio.gpio_configs import *

@pytest.mark.parametrize('config, result', 
                       [('dac', GpioDACConfig),
                        ('adc', GpioADCConfig),
                        ('rtd', GpioRTDConfig),
                        ('din', None),
                        ('dout', None),
                        ('led', GpioLEDConfig),
                        ( None, None)])
def test_getPeriphConfig(config, result):
    assert getPeriphConfig(config) == result