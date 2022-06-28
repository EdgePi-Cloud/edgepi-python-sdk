import pytest
from edgepi.gpio.gpio_commands import *
from edgepi.gpio.gpio_configs import *

@pytest.mark.parametrize('config, result', 
                       [('dac', GpioConfigs.DAC.value),
                        ('adc', GpioConfigs.ADC.value),
                        ('rtd', GpioConfigs.RTD.value),
                        ('din', None),
                        ('dout', None),
                        ('led', GpioConfigs.LED.value),
                        ( None, None)])
def test_getPeriphConfig(config, result):
    assert getPeriphConfig(config) == result