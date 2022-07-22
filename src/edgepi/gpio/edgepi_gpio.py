'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''

import logging
from edgepi.gpio.gpio_configs import generate_pin_info, GpioExpanderConfig
from edgepi.peripherals.i2c import I2CDevice
from edgepi.gpio.gpio_commands import (
    get_pin_config_address,
    break_pin_info_dict,
    get_default_values,
    check_multiple_dev,
    set_pin_states
    )
from edgepi.reg_helper.reg_helper import apply_opcodes, convert_dict_to_values

_logger = logging.getLogger(__name__)


class EdgePiGPIO(I2CDevice):
    '''
    A class used to represent the GPIO. This class will be imported to each module
    that requires GPIO manipulation. It is not intended for user.
    '''
    def __init__(self, config: GpioExpanderConfig = None):
        if config is None:
            raise ValueError(f'Missing Config {config}')
        self.config = config
        _logger.debug(f'{self.config.name} Configuration Selected: {self.config}')
        if self.config is not None and 'i2c' in self.config.dev_path:
            super().__init__(self.config.dev_path)
            self.pin_config_address, self.pin_out_address = get_pin_config_address(self.config)
            self.dict_pin = generate_pin_info(self.config)
            self.dict_default_reg_dict = None
        # TODO: add GPIO init, GPIO and I2C init

    def __generate_default_reg_dict(self, list_of_address):
        '''
        Function to generate a list of default register dictionary
        Return:
            list of register dictionary [{register address : register value}]
            list of pin list
        '''
        list_reg_dict={}
        for address in list_of_address:
            list_reg_dict[address]=self.__map_reg_address_value_dict(address)
        return list_reg_dict

    def set_expander_default(self):
        '''
        function to set the pins to default configuration
        Note: always toggle output state first before changing the pin direction
        Return:
            list_default_reg_dict:
                list of dictionary that includes default regsister address : value pair
        '''
        list_of_address = check_multiple_dev(generate_pin_info(self.config))
        self.dict_default_reg_dict = self.__generate_default_reg_dict(list_of_address)
        pin_info_dict_list = break_pin_info_dict(generate_pin_info(self.config))

        for pin_dict, default_reg_dict in\
            zip(pin_info_dict_list, list(self.dict_default_reg_dict.values())):

            pin_info_list = list(pin_dict.values())
            dev_address = pin_info_list[0].address
            default_reg_dict = get_default_values(default_reg_dict, pin_info_list)

            for reg_addx, entry in default_reg_dict.items():
                if entry['is_changed']:
                    msg_write = self.set_write_msg(reg_addx, [entry['value']])
                    self.transfer(dev_address, msg_write)

            for reg_address, value in default_reg_dict.items():
                list_read_msg = self.set_read_msg(reg_address, [value])
                default_reg_dict[reg_address] = self.transfer(dev_address, list_read_msg)
        set_pin_states(self.dict_pin)

    def __read_register(self, reg_address, dev_address):
        '''
        function to read one register value
        In:
            reg_address: register address to read data from
            dev_address: expander address to read
        Returns:
            A byte data
        '''
        msg_read = self.set_read_msg(reg_address, [0xFF])
        _logger.debug(f'Read Message: Register Address {msg_read[0].data}\
                      , Msg Place Holder {msg_read[1].data}')
        self.transfer(dev_address, msg_read)
        _logger.debug(f'Message Read: Register Address {msg_read[0].data},\
         Msg Place Holder {msg_read[1].data}')
        return msg_read[1].data[0]

    def __map_reg_address_value_dict(self, dev_address):
        '''
        Function to map address : value dictionary
        In:
            dev_address: expander address to read
        Returns:
            Dictionary containing address : value
        '''
        reg_map = {}
        reg_map[self.pin_out_address] =\
            self.__read_register(self.pin_out_address, dev_address)
        reg_map[self.pin_config_address] =\
            self.__read_register(self.pin_config_address, dev_address)
        return reg_map

    def __write_changed_values(self, reg_dict: dict = None, dev_address: int = None):
        '''
        Function to write changed values to the specified register
        In:
            reg_dict (dict): register address to value and is_changed flag
                             {register_address : {'value' : value(int), is_changed : bool}}
            dev_address: device address, 32 or 33
        Returns:
            void
        '''
        for reg_addx, entry in reg_dict.items():
            if entry['is_changed']:
                msg_write = self.set_write_msg(reg_addx, [entry['value']])
                self.transfer(dev_address, msg_write)

    def set_expander_pin(self, pin_name: str = None):
        '''
        Function set gpio pin state to high
        In:
            pin_name (str): name of the pin to set
        Returns:
            self.dict_pin[pin_name].is_high
        '''
        dev_address = self.dict_pin[pin_name].address
        list_opcode = [self.dict_pin[pin_name].set_code]
        dict_register = apply_opcodes(self.dict_default_reg_dict[dev_address], list_opcode)

        self.__write_changed_values(dict_register, dev_address)
        dict_register = convert_dict_to_values(dict_register)

        self.dict_pin[pin_name].is_high = True
        return self.dict_pin[pin_name].is_high

    def clear_expander_pin(self, pin_name: str = None):
        '''
        Function clear gpio pin state to low
        In:
            pin_name (str): name of the pin to set
        Returns:
            self.dict_pin[pin_name].is_high
        '''
        dev_address = self.dict_pin[pin_name].address
        list_opcode = [self.dict_pin[pin_name].clear_code]
        dict_register = apply_opcodes(self.dict_default_reg_dict[dev_address], list_opcode)

        self.__write_changed_values(dict_register, dev_address)
        dict_register = convert_dict_to_values(dict_register)

        self.dict_pin[pin_name].is_high = False
        return self.dict_pin[pin_name].is_high

    def toggle_expander_pin(self, pin_name: str = None):
        '''
        Function toggle gpio pin state to opposite logic
        High -> Low
        Low -> High
        In:
            pin_name (str): name of the pin to set
        Returns:
            void
        '''
        self.dict_pin[pin_name].is_high = self.clear_expander_pin(pin_name)\
                                          if self.dict_pin[pin_name].is_high\
                                          else self.set_expander_pin(pin_name)
