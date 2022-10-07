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

# pylint: disable=logging-too-many-args
class EdgePiGPIO(I2CDevice):
    '''
    A class used to represent the GPIO Expander configuration for an I2C Device.
    This class will be imported to each module that requires GPIO manipulation.
    It is not intended for users.
    '''
    def __init__(self, config: GpioExpanderConfig = None):
        if config is None:
            raise ValueError(f'Missing Config {config}')
        self.config = config
        _logger.debug(f'{self.config.name} Configuration Selected: {self.config}')
        if self.config is not None and 'i2c' in self.config.dev_path:
            super().__init__(self.config.dev_path)
            # get expander configuration port and output port addxs for this device
            self.pin_config_address, self.pin_out_address = get_pin_config_address(self.config)
            # get this device's expander pin names and opcodes for set, clear, direction ops
            self.dict_pin = generate_pin_info(self.config)
            # this is initialized by `set_expander_default` call
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
        _logger.info('Setting GPIO to default state')
        list_of_address = check_multiple_dev(generate_pin_info(self.config))
        self.dict_default_reg_dict = self.__generate_default_reg_dict(list_of_address)
        pin_info_dict_list = break_pin_info_dict(generate_pin_info(self.config))

        for pin_dict, default_reg_dict in\
            zip(pin_info_dict_list, list(self.dict_default_reg_dict.values())):

            pin_info_list = list(pin_dict.values())
            dev_address = pin_info_list[0].address
            default_reg_dict = get_default_values(default_reg_dict, pin_info_list)

            self.__write_changed_values(default_reg_dict, dev_address)

            for reg_address, value in default_reg_dict.items():
                list_read_msg = self.set_read_msg(reg_address, [value['value']])
                default_reg_dict[reg_address] = self.transfer(dev_address, list_read_msg)[0]
                _logger.debug(f'Updated Default Register Dictionary Contest {default_reg_dict}')
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
                _logger.debug(f'Write Message Content {msg_write[0]}')
                self.transfer(dev_address, msg_write)

    def read_expander_pin(self, pin_name: str = None):
        '''
        Get the current state of a GPIO expander pin (low or high).

        Args:
            `pin_name` (str): name of the pin whose state to read

        Returns:
            `bool`: True if state is high, False if state is low
        '''
        dev_address = self.dict_pin[pin_name].address
        reg_addx = self.dict_pin[pin_name].set_code.reg_address
        pin_mask = self.dict_pin[pin_name].set_code.op_mask

        # read register at reg_addx
        read_msg = self.set_read_msg(reg_addx, [0xFF])
        reg_val = self.transfer(dev_address, read_msg)[0]
        # pylint: disable=logging-too-many-args
        _logger.debug(
            "GPIO reading device '%s' starting at register '%s': value bytes='%s'",
            hex(dev_address),
            hex(reg_addx),
            bin(reg_val)
        )
        # print(f"Reading device '{dev_address}' starting at register '{hex(reg_addx)}': value bytes='{bin(reg_val)}'")

        # get value at pin_index by masking the other bits
        return reg_val & (~pin_mask)


    def get_pin_direction(self, pin_name: str = None):
        '''
        Get the current direction of a GPIO expander pin (low or high).

        Args:
            `pin_name` (str): name of the pin whose state to read

        Returns:
            `bool`: True if direction is input, False if direction is output
        '''
        dev_address = self.dict_pin[pin_name].address
        reg_addx = self.dict_pin[pin_name].dir_code.reg_address
        pin_mask = self.dict_pin[pin_name].dir_code.op_mask

        # TODO: refactor this to private method
        # read register at reg_addx
        read_msg = self.set_read_msg(reg_addx, [0xFF])
        reg_val = self.transfer(dev_address, read_msg)[0]
        _logger.debug(
            "GPIO reading device '%s' starting at register '%s': value bytes='%s'",
            hex(dev_address),
            hex(reg_addx),
            bin(reg_val)
        )
        # print(f"Reading device '{dev_address}' starting at register '{hex(reg_addx)}': value bytes='{bin(reg_val)}'")

        # get value at pin_index by masking the other bits
        return reg_val & (~pin_mask)


    def set_pin_direction(self, pin_name, direction):
        '''
        Set the direction of a GPIO expander pin (low or high).

        Args:
            `pin_name` (str): name of the pin whose state to read

        Returns:
            `bool`: True if direction is input, False if direction is output
        '''
        raise NotImplementedError

    def set_expander_pin(self, pin_name: str = None):
        '''
        Function set gpio pin state to high
        In:
            pin_name (str): name of the pin to set
        Returns:
            self.dict_pin[pin_name].is_high
        '''
        dev_address = self.dict_pin[pin_name].address
        reg_addx = self.dict_pin[pin_name].set_code.reg_address

        # get register value of port this pin belongs to
        # TODO: use private method
        read_msg = self.set_read_msg(reg_addx, [0xFF])
        reg_val = self.transfer(dev_address, read_msg)[0]

        # apply opcode to set this pin high
        # TODO: private method
        reg_map = {reg_addx: {"value": reg_val}}
        updated_reg_map = apply_opcodes(reg_map, [self.dict_pin[pin_name].set_code])
        updated_reg_val = updated_reg_map[reg_addx]["value"]
        _logger.debug("Updating port '%s' value from '%s' to '%s'", reg_addx, hex(reg_val), hex(updated_reg_val))

        # set pin direction to output
        self.set_pin_direction(pin_name, "output")

        # set pin state to high
        # TODO: refactor private method `__write_changed_values`
        write_msg = self.set_write_msg(reg_addx, [updated_reg_val])
        _logger.debug(f'GPIO Write Message Content {bin(write_msg[0])}')
        self.transfer(dev_address, write_msg)

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
