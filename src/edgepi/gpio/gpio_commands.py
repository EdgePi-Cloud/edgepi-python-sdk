from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *

def getPeriphConfig(config: str = None):
    ''' Used to get proper config dataclass to configure neccessary peripheral configuration '''
    for perpheryConfig in GpioConfigs:
        if config == perpheryConfig.value.name:
            return perpheryConfig.value
    return None

def getPinConfigAddress(config:GpioExpanderConfig = None ):
    ''' 
    In: GPIO Expander Config data class
    Return: pin configuration(Direction) register address, pin output port (output level) register address 
    '''
    return GPIOAddresses.CONFIGURATION_PORT_0.value if config.port is 'A'else GPIOAddresses.CONFIGURATION_PORT_1.value, GPIOAddresses.OUTPUT_PORT_0.value if config.port is 'A'else GPIOAddresses.OUTPUT_PORT_1.value

def getDefaultValues(config:GpioExpanderConfig = None, pinList: list = None):
    ''' 
    In: GPIO Expander Config data class
    Return: pin configuration(Direction) register value, pin output port (output level) register value
    '''
    pinDirVal = []
    pinOutVal = []
    # TODO: check config and return specific Values 
    # if config.port is 'A' and config.dir is 'out':
    #     for pin in pinList:


def setPinStates(pinList:list = None):
    ''' 
    In:
        pinInfo: list of pin info dataclass
    Return: pin configuration(Direction) register value, pin output port (output level) register value
    '''
    for pin in pinList:
        pin.is_high = False
        pin.is_out = True
    return pinList