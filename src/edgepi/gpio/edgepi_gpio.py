'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''

import logging
import time

from edgepi.peripherals.gpio import GpioDevice
from edgepi.peripherals.i2c import I2CDevice
from edgepi.gpio.gpio_configs import GpioConfigs
from edgepi.gpio.gpio_commands import *

from edgepi.reg_helper.reg_helper import apply_opcodes

_logger = logging.getLogger(__name__)

class EdgePiGPIO(I2CDevice):
    ''' 
    A class used to represent the GPIO. This class will be imported to each module
    that requires GPIO manipulation. It is not intended for user.
    '''
    
    def __init__(self, config: GpioExpanderConfig = None):
        if config is None:
            raise ValueError(f'Missing Config Name')
        self.config = config
        _logger.debug(f'{self.config.name} Configuration Selected: {self.config}')
        if self.config is not None and 'i2c' in self.config.dev_path:
            super().__init__(self.config.dev_path)
            _logger.info(f'GPIO expander up and running')
            self.pin_config_address, self.pin_out_address = get_pin_config_address(self.config)
        # TODO: add GPIO init, GPIO and I2C init

    def __generate_default_reg_dict(self, list_of_address):
        ''' 
        Function to generate a list of default register dictionary
        Return:
            list of register dictionary [{register address : register value}]
            list of pin list
        '''
        listRegDict=[]
        for address in list_of_address:
            listRegDict.append(self.__map_reg_address_value_dict(address))
        return listRegDict

    def set_expander_default(self):
        ''' 
        function to set the pins to default configuration
        Note: always toggle output state first before changing the pin direction
        Return:
            list_default_reg_dict: list of dictionary that includes default regsister address : value pair
        '''

        list_default_reg_dict = self.__generate_default_reg_dict(check_multiple_dev(generate_pin_info(self.config)))
        pin_info_dict_list = break_pin_info_dict(generate_pin_info(self.config))
        for pin_dict, default_reg_dict in zip(pin_info_dict_list, list_default_reg_dict):
            pin_info_list = list(pin_dict.values())
            dev_address = pin_info_list[0].address
            default_reg_dict = get_default_values(default_reg_dict, pin_info_list)
            
            for reg_addx, entry in default_reg_dict.items():
                if entry['is_changed']:
                    msg_write = self.set_write_msg(reg_addx, [entry['value']])
                    self.transfer(dev_address, msg_write)

            for reg_address, value in default_reg_dict.items():
                default_reg_dict[reg_address] = self.transfer(dev_address, self.set_read_msg(reg_address, [value]))
        return list_default_reg_dict
    
    def __read_register(self, reg_address, dev_address):
        ''' 
        function to read one register value
        In:
            reg_address: register address to read data from
            dev_address: expander address to read 
        Returns:
            A byte data
        '''
        _logger.debug(f'Reading a register value')
        msg_read = self.set_read_msg(reg_address, [0xFF])
        _logger.debug(f'Read Message: Register Address {msg_read[0].data}, Msg Place Holder {msg_read[1].data}')
        self.transfer(dev_address, msg_read)
        _logger.debug(f'Message Read: Register Address {msg_read[0].data}, Msg Place Holder {msg_read[1].data}')
        return msg_read[1].data[0]

    def __map_reg_address_value_dict(self, dev_address):
        ''' 
        Function to map address : value dictionary
        In:
            dev_address: expander address to read 
        Returns:
            Dictionary containing address : value
        '''
        _logger.info(f'Mapping a register addree : register value')
        reg_map = {}
        reg_map[self.pin_out_address] = self.__read_register(self.pin_out_address, dev_address)
        reg_map[self.pin_config_address] = self.__read_register(self.pin_config_address, dev_address)
        return reg_map