import pytest
from edgepi.gpio.gpio_commands import *
from edgepi.gpio.gpio_configs import *

@pytest.mark.parametrize('config, result', 
                       [('dac', GpioDACConfig),
                        ('adc', 'adc'),
                        ('rtd', 'rtd'),
                        ('din', 'din'),
                        ('dout', 'dout'),
                        ('ledArry', 'ledArry'),
                        ( None, None)])
def test_getPeriphConfig(config, result):
    assert getPeriphConfig(config) == result