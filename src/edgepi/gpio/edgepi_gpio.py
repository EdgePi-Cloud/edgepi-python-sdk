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
from edgepi.reg_helper.reg_helper import apply_opcodes, is_bit_set

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

    # TODO: not needed anymore?
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
        # TODO: this doesn't return result of the register read?
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

    def read_expander_pin_state(self, pin_name: str = None):
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
        reg_val = self.__read_port(dev_address, reg_addx)
        pin_val = is_bit_set(reg_val, pin_mask)
        _logger.debug(":read_expander_pin_state: pin '%s' = '%s'", pin_name,  pin_val)

        # get value at pin_index by masking the other bits
        return pin_val

    def get_pin_direction(self, pin_name: str = None):
        '''
        Get the current direction of a GPIO expander pin (low or high).

        Args:
            `pin_name` (str): name of the pin whose state to read

        Returns:
            `bool`: True if direction is input, False if direction is output
        '''
        dev_address = self.dict_pin[pin_name].address
        # dir_out_code and dir_in_code have the same addx and mask, doesn't matter which
        reg_addx = self.dict_pin[pin_name].dir_out_code.reg_address
        pin_mask = self.dict_pin[pin_name].dir_out_code.op_mask

        # read register at reg_addx
        reg_val = self.__read_port(dev_address, reg_addx)
        pin_val = is_bit_set(reg_val, pin_mask)
        _logger.debug(":get_pin_direction: pin '%s' = '%s'", pin_name,  pin_val)

        # get value at pin_index by masking the other bits
        return pin_val

    # TODO: merge with __read_register (note: they don't return the same value)
    def __read_port(self, dev_addx, port_addx) -> int:
        '''
        Read value of a port/register on a I2C device

        Args:
            `dev_addx` (int): I2C device address

            `port_addx` (int): port/register address to read value of

        Returns:
            `int`: 8-bit uint value of port/register
        '''
        read_msg = self.set_read_msg(port_addx, [0xFF])
        reg_val = self.transfer(dev_addx, read_msg)[0]
        _logger.debug(
            "__read_port: dev_addx='%s', port_addx='%s': value='%s'",
            dev_addx,
            hex(port_addx),
            hex(reg_val)
        )
        return reg_val

    def set_pin_direction_out(self, pin_name):
        '''
        Set the direction of a GPIO expander pin to output. Note this will
        set pin to low before setting to output for safety reasons.

        Args:
            `pin_name` (str): name of the pin whose direction to set
        '''
        dev_address = self.dict_pin[pin_name].address
        dir_out_code = self.dict_pin[pin_name].dir_out_code
        reg_addx = dir_out_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_port(dev_address, reg_addx)

        # set pin to low before setting to output (hazard)
        self.clear_expander_pin(pin_name)

        # set pin direction to out
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, dir_out_code)
        _logger.debug(":set_pin_direction_out: pin '%s' set to output", pin_name)

        self.dict_pin[pin_name].is_out = True

    def set_pin_direction_in(self, pin_name):
        '''
        Set the direction of a GPIO expander pin to high impedance input.

        Args:
            `pin_name` (str): name of the pin whose direction to set
        '''
        dev_address = self.dict_pin[pin_name].address
        dir_in_code = self.dict_pin[pin_name].dir_in_code
        reg_addx = dir_in_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_port(dev_address, reg_addx)

        # set pin to low before setting to output (hazard)
        self.clear_expander_pin(pin_name)

        # set pin direction to out
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, dir_in_code)
        _logger.debug(":set_pin_direction_in: pin '%s' set to output", pin_name)

        self.dict_pin[pin_name].is_out = False

    def set_expander_pin(self, pin_name: str = None):
        '''
        Function set gpio pin state to high

        Args:
            `pin_name` (str): name of the pin to set
        '''
        dev_address = self.dict_pin[pin_name].address
        set_code = self.dict_pin[pin_name].set_code
        reg_addx = set_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_port(dev_address, reg_addx)

        # set pin direction to output (also sets to low)
        self.set_pin_direction_out(pin_name)

        # set pin state to high
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, set_code)
        _logger.debug(":set_expander_pin: pin '%s' = set to high", pin_name)

        self.dict_pin[pin_name].is_high = True
        return self.dict_pin[pin_name].is_high

    def __apply_code_to_register(self, dev_addx, reg_addx, reg_val, opcode):
        """
        Applies an opcode obtained from I2CPinInfo object to a register.

        Args:
            dev_addx (int): I2C device address
            reg_addx (int): register/port address
            reg_val (int): current 8-bit value of register at reg_addx
            opcode (OpCode): opcode to apply to register at reg_addx
        """
        # apply opcode to get new register value
        reg_map = {reg_addx: reg_val}
        updated_reg_map = apply_opcodes(reg_map, [opcode])
        # write new register value to set pin new state
        self.__write_changed_values(updated_reg_map, dev_addx)
        _logger.debug(
            "__apply_code_to_register: dev_addx='%s', reg_addx='%s', reg_val='%s, opcode='%s'",
            dev_addx,
            hex(reg_addx),
            hex(reg_val),
            opcode
        )

    def clear_expander_pin(self, pin_name: str = None):
        '''
        Function clear gpio pin state to low
        In:
            pin_name (str): name of the pin to set
        '''
        dev_address = self.dict_pin[pin_name].address
        clear_code = self.dict_pin[pin_name].clear_code
        reg_addx = clear_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_port(dev_address, reg_addx)

        # set pin state to low
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, clear_code)
        _logger.debug(":set_expander_pin: pin '%s' = set to low", pin_name)

        self.dict_pin[pin_name].is_high = False

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
