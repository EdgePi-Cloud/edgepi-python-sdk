'''
Provides group of helper functions for GPIO module
'''

from edgepi.gpio.gpio_constants import GPIOAddresses
from edgepi.gpio.gpio_configs import GpioConfigs, GpioExpanderConfig
from edgepi.reg_helper.reg_helper import apply_opcodes

def get_periph_config(config: str = None):
    '''
        Used to get proper config dataclass to configure neccessary peripheral configuration
        In
            config (str): name of comfiuration
        Return
            config (GpioExpanderConfig): gpio expander dataclass
            None if config doesnt exists in the Enum
    '''
    for perphery_config in GpioConfigs:
        if config == perphery_config.value.name:
            return perphery_config.value
    return None

def get_pin_config_address(config:GpioExpanderConfig = None ):
    '''
    Depending on the config, return GPIO expander port register addresses
    In:
        config (GpioExpanderConfig) GPIO Expander Config data class
    Return:
        pin configuration(Direction) register address
        pin output port (output level) register address
    '''
    return (GPIOAddresses.CONFIGURATION_PORT_0.value, GPIOAddresses.OUTPUT_PORT_0.value)\
        if config.port == 'B' else\
            (GPIOAddresses.CONFIGURATION_PORT_1.value, GPIOAddresses.OUTPUT_PORT_1.value)

def get_default_values(reg_dict: dict = None, pin_list: list = None):
    '''
    In:
        reg_dict (dict) - dictionary register address : register value
        pin_list (list) - list of I2cPinInfo dataclasses
    Return:
        reg_dict (dict) - modified dictionary
                          {register address : {'value': register_vlaue, is_changed : true/false}}
    '''
    # Generating list of OpCode, order = GpioXOutputClear, GpioXPinDir
    list_opcode = [pin.clear_code for pin in pin_list] + [pin.dir_out_code for pin in pin_list]
    apply_opcodes(reg_dict, list_opcode)
    return reg_dict

def check_multiple_dev(pin_dict: dict = None):
    '''
    Check if pins in the dictionary belong to the same I2C dev or not
    In:
        pin_dict (dict) - dictionary of I2cPinInfo dataclasses
    Return:
        list_of_address (list) - list of device addresses

    '''
    addresses = [value.address for value in pin_dict.values()]
    list_of_address = list(set(addresses))
    return list_of_address

def break_pin_info_dict(pin_dict: dict = None):
    '''
    break pin_info_dict into two separate dictionaries if there are more than 2 devices used
    In:
        pin_dict (dict) - dictionary of I2cPinInfo dataclasses
    Return:
        list of dictionary: if there are two device used, there are two dictionaries in the list
    '''
    address_list = check_multiple_dev(pin_dict)
    if len(address_list) == 2:
        secondary_dict = {}
        for key, value in pin_dict.items():
            if value.address == address_list[1]:
                secondary_dict[key] = value
        for key in secondary_dict:
            pin_dict.pop(key)
        return [pin_dict, secondary_dict]
    return [pin_dict]

def set_pin_states(pin_dict:dict = None):
    '''
    In:
        pinInfo: list of pin info dataclass
    Return:
        pin configuration(Direction) register value, pin output port (output level) register value
    '''
    for key in pin_dict:
        pin_dict[key].is_high = False
        pin_dict[key].is_out = True
    return pin_dict
