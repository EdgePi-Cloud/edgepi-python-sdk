from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *

def getPeriphConfig(config: str = None):
    ''' Used to get proper config dataclass to configure neccessary peripheral configuration '''
    if config == 'dac':
        gpioConfig = GpioDACConfig
    elif config == 'adc':
        gpioConfig = 'adc'
    elif config == 'rtd':
        gpioConfig = 'rtd'
    elif config == 'ledArry':
        gpioConfig = 'ledArry'
    elif config == 'din':
        gpioConfig = 'din'
    elif config == 'dout':
        gpioConfig = 'dout'
    else:
        gpioConfig = None
    return gpioConfig