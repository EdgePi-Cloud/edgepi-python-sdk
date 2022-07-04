from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *
from edgepi.reg_helper.reg_helper import apply_opcodes

def get_periph_config(config: str = None):
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

def get_pin_config_address(config:GpioExpanderConfig = None ):
    ''' 
    Depending on the config, return register addresses
    In: 
        config (GpioExpanderConfig) GPIO Expander Config data class
    Return:
        pin configuration(Direction) register address, pin output port (output level) register address 
    '''
    # return GPIOAddresses.CONFIGURATION_PORT_0.value if config.port is 'A'else GPIOAddresses.CONFIGURATION_PORT_1.value, GPIOAddresses.OUTPUT_PORT_0.value if config.port is 'A'else GPIOAddresses.OUTPUT_PORT_1.value
    return (GPIOAddresses.CONFIGURATION_PORT_0.value, GPIOAddresses.OUTPUT_PORT_0.value) if config.port is 'A' else (GPIOAddresses.CONFIGURATION_PORT_1.value, GPIOAddresses.OUTPUT_PORT_1.value)

def get_default_values(reg_dict: dict = None, pin_list: list = None):
    ''' 
    In:
        reg_dict (dict) - dictionary register address : register value
        pin_list (list) - list of I2cPinInfo dataclasses
    Return: 
        reg_dict (dict) - modified dictionary register address : {'value': register_vlaue, is_changed : true/false}
    '''
    # Generating list of OpCode, order = GpioXOutputClear, GpioXPinDir
    OpCodeList = [pin.clearCode for pin in pin_list] + [pin.dirCode for pin in pin_list]
    apply_opcodes(reg_dict, OpCodeList)
    return reg_dict

def check_multiple_dev(pin_list: list = None):
    ''' 
    Check if pins in the list belong to the same I2C dev or not
    In:
        pin_list (list) - list of I2cPinInfo dataclasses
    Return: 
        List of pin_list if there are more than one I2C device address exists
    '''
    dev_1 = [pin for pin in pin_list if pin.address == GpioExpanderAddress.EXP_ONE.value]
    dev_2 = [pin for pin in pin_list if pin.address == GpioExpanderAddress.EXP_TWO.value]
    return [dev_1, dev_2]

def set_pin_states(pin_list:list = None):
    ''' 
    In:
        pinInfo: list of pin info dataclass
    Return: pin configuration(Direction) register value, pin output port (output level) register value
    '''
    for pin in pin_list:
        pin.is_high = False
        pin.is_out = True
    return pin_list