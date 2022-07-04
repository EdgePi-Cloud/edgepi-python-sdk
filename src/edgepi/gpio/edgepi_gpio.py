'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''

import logging
import time

from edgepi.peripherals.gpio import GpioDevice
from edgepi.peripherals.i2c import I2CDevice
from edgepi.gpio.gpio_commands import *

from edgepi.reg_helper.reg_helper import apply_opcodes

_logger = logging.getLogger(__name__)

class EdgePiGPIO(I2CDevice):
    ''' 
    A class used to represent the GPIO. This class will be imported to each module
    that requires GPIO manipulation. It is not intended for user.
    '''
    
    def __init__(self, config_name: str = None):
        if config_name is None:
            raise ValueError(f'Missing Config Name')
        self.config = get_periph_config(config_name)
        _logger.debug(f'{self.config.name} Configuration Selected: {self.config}')
        if self.config is not None and 'i2c' in self.config.dev_path:
            super().__init__(self.config.dev_path)
            _logger.info(f'GPIO expander up and running')
            self.pin_list = generate_pin_info(self.config.name)
            self.pin_config_address, self.pin_out_address = get_pin_config_address(self.config)
        # TODO: add GPIO init, GPIO and I2C init

    def __generate_default_reg_dict(self, pin_lists):
        ''' 
        Function to generate a list of default register dictionary
        Return:
            list of register dictionary [{register address : register value}]
            list of pin list
        '''
        listRegDict=[]
        for pin_list in pin_lists:
            if pin_list:
                listRegDict.append(self.__reg_addressToValue_dict(pin_list[0].address))
            else:
                listRegDict.append(None)
        return listRegDict

    def set_expander_default(self):
        ''' 
        function to set the pins to default configuration
        Note: always toggle output state first before changing the pin direction
        Return:
            list_default_reg_dict: list of dictionary that includes default regsister address : value pair
        '''
        pin_lists = check_multiple_dev(self.pin_list)
        list_default_reg_dict = self.__generate_default_reg_dict(pin_lists)
        for pin_list, default_reg_dict in zip(pin_lists, list_default_reg_dict):
            if not pin_list:
                continue
            dev_address = pin_list[0].address
            default_reg_dict = get_default_values(default_reg_dict, pin_list)
            
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

    def __reg_addressToValue_dict(self, dev_address):
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