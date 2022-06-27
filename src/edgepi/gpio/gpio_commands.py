from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *

def getPeriphConfig(config: str = None):
    ''' Used to get proper config dataclass to configure neccessary peripheral configuration '''
    if config == 'dac':
        gpioConfig = GpioDACConfig
    elif config == 'adc':
        gpioConfig = GpioADCConfig
    elif config == 'rtd':
        gpioConfig = GpioRTDConfig
    elif config == 'led':
        gpioConfig = GpioLEDConfig
    elif config == 'din':
        gpioConfig = None
    elif config == 'dout':
        gpioConfig = None
    else:
        gpioConfig = None
    return gpioConfig