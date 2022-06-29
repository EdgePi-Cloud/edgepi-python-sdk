from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *

def getPeriphConfig(config: str = None):
    ''' Used to get proper config dataclass to configure neccessary peripheral configuration '''
    for perpheryConfig in GpioConfigs:
        if config == perpheryConfig.value.name:
            return perpheryConfig.value
    return None

def getPinConfigAddress(config:GpioExpanderConfig = None ):
    return GPIOAddresses.CONFIGURATION_PORT_0.value if config.port is 'A'else GPIOAddresses.CONFIGURATION_PORT_1.value, GPIOAddresses.OUTPUT_PORT_0.value if config.port is 'A'else GPIOAddresses.OUTPUT_PORT_1.value

def getDefaultValues(config:GpioExpanderConfig = None):
    return GpioAPinDir.ALL_DIR_OUT.value.op_code if config.port is 'A'else GpioBPinDir.ALL_DIR_OUT.value.op_code, GpioAOutputClear.CLEAR_OUTPUT_ALL.value.op_code if config.port is 'A'else GpioBOutputClear.CLEAR_OUTPUT_ALL.value.op_code
