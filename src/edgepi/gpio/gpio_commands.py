from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *

def getPeriphConfig(config: str = None):
    ''' Used to get proper config dataclass to configure neccessary peripheral configuration '''
    for perpheryConfig in GpioConfigs:
        if config == perpheryConfig.value.name:
            return perpheryConfig.value
    return None