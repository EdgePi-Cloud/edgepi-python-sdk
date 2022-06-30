from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *
from edgepi.reg_helper.reg_helper import apply_opcodes

def getPeriphConfig(config: str = None):
    ''' Used to get proper config dataclass to configure neccessary peripheral configuration 
        In
            config (str): name of comfiuration
        Return
            config (GpioExpanderConfig): gpio expander dataclass
            None if config doesnt exists in the Enum
    '''
    for perpheryConfig in GpioConfigs:
        if config == perpheryConfig.value.name:
            return perpheryConfig.value
    return None

def getPinConfigAddress(config:GpioExpanderConfig = None ):
    ''' 
    Depending on the config, return register addresses
    In: 
        config (GpioExpanderConfig) GPIO Expander Config data class
    Return:
        pin configuration(Direction) register address, pin output port (output level) register address 
    '''
    return GPIOAddresses.CONFIGURATION_PORT_0.value if config.port is 'A'else GPIOAddresses.CONFIGURATION_PORT_1.value, GPIOAddresses.OUTPUT_PORT_0.value if config.port is 'A'else GPIOAddresses.OUTPUT_PORT_1.value

def getDefaultValues(reg_dict: dict = None, pinList: list = None):
    ''' 
    In:
        reg_dict (dict) - dictionary register address : register value
        pin_list (list) - list of I2cPinInfo dataclasses
    Return: 
        reg_dict (dict) - modified dictionary register address : {'value': register_vlaue, is_changed : true/false}
    '''
    # Generating list of OpCode, order = GpioXOutputClear, GpioXPinDir
    OpCodeList = [pin.clearCode for pin in pinList] + [pin.dirCode for pin in pinList]
    apply_opcodes(reg_dict, OpCodeList)
    return reg_dict

def checkMultipleDev(pinList: list = None):
    ''' 
    Check if pins in the list belong to the same I2C dev or not
    In:
        pin_list (list) - list of I2cPinInfo dataclasses
    Return: 
        List of pin_list if there are more than one I2C device address exists
    '''
    dev_1 = [pin for pin in pinList if pin.address == 32]
    dev_2 = [pin for pin in pinList if pin.address == 33]
    return [dev_1, dev_2]

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