'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''


import logging
from edgepi.gpio.gpio_configs import generate_expander_pin_info
from edgepi.gpio.gpio_constants import GpioDevPaths
from edgepi.peripherals.i2c import I2CDevice
from edgepi.reg_helper.reg_helper import OpCode, apply_opcodes, is_bit_set

_logger = logging.getLogger(__name__)

# pylint: disable=logging-too-many-args
class EdgePiGPIOExpander(I2CDevice):
    '''
    A class used to represent the GPIO Expander configuration for an I2C Device.
    This class will be imported to each module that requires GPIO manipulation.
    It is not intended for users.
    '''
    def __init__(self):
        super().__init__(GpioDevPaths.I2C_DEV_PATH.value)
        # get this device's expander pin names and opcodes for set, clear, direction ops
        self.expander_pin_dict = generate_expander_pin_info()

    def __read_register(self, reg_address: int, dev_address: int) -> int:
        '''
        function to read one register value from an I2C device
        Args:
            `reg_address`: register/port address to read data from
            `dev_address`: expander address to read
        Returns:
            `int`: 8-bit uint value of port/register
        '''
        msg_read = self.set_read_msg(reg_address, [0xFF])
        _logger.debug(f'Read Message: Register Address {msg_read[0].data}\
                      , Msg Place Holder {msg_read[1].data}')
        self.transfer(dev_address, msg_read)
        _logger.debug(f'Message Read: Register Address {msg_read[0].data},\
         Msg Place Holder {msg_read[1].data}')
        return msg_read[1].data[0]

    def __write_changed_values(self, reg_dict: dict, dev_address: int):
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

    def read_expander_pin(self, pin_name: str) -> bool:
        '''
        Get the current state of a GPIO expander pin (low or high).

        Args:
            `pin_name` (str): name of the pin whose state to read

        Returns:
            `bool`: True if state is high, False if state is low
        '''
        dev_address = self.expander_pin_dict[pin_name].address
        reg_addx = self.expander_pin_dict[pin_name].set_code.reg_address
        pin_mask = self.expander_pin_dict[pin_name].set_code.op_mask

        # read register at reg_addx
        reg_val = self.__read_register(reg_addx, dev_address)
        pin_state = is_bit_set(reg_val, pin_mask)
        _logger.debug(":read_expander_pin: pin '%s' = '%s'", pin_name,  pin_state)

        return pin_state

    def get_expander_pin_direction(self, pin_name: str) -> bool:
        '''
        Get the current direction of a GPIO expander pin (low or high).

        Args:
            `pin_name` (str): name of the pin whose state to read

        Returns:
            `bool`: True if direction is input, False if direction is output
        '''
        dev_address = self.expander_pin_dict[pin_name].address
        # dir_out_code and dir_in_code have the same addx and mask, doesn't matter which
        reg_addx = self.expander_pin_dict[pin_name].dir_out_code.reg_address
        pin_mask = self.expander_pin_dict[pin_name].dir_out_code.op_mask

        # read register at reg_addx
        reg_val = self.__read_register(reg_addx, dev_address)
        pin_state = is_bit_set(reg_val, pin_mask)
        _logger.debug(":get_expander_pin_direction: pin '%s' = '%s'", pin_name,  pin_state)

        return pin_state

    def set_expander_pin_direction_out(self, pin_name: str):
        '''
        Set the direction of a GPIO expander pin to output. Note this will
        set pin to low before setting to output for safety reasons.

        Args:
            `pin_name` (str): name of the pin whose direction to set
        '''
        dev_address = self.expander_pin_dict[pin_name].address
        dir_out_code = self.expander_pin_dict[pin_name].dir_out_code
        reg_addx = dir_out_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_register(reg_addx, dev_address)

        # set pin to low before setting to output (hazard)
        self.clear_expander_pin(pin_name)

        # set pin direction to out
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, dir_out_code)
        _logger.debug(":set_expander_pin_direction_out: pin '%s' set to output", pin_name)

        self.expander_pin_dict[pin_name].is_out = True

    def set_expander_pin_direction_in(self, pin_name: str):
        '''
        Set the direction of a GPIO expander pin to high impedance input.

        Args:
            `pin_name` (str): name of the pin whose direction to set
        '''
        dev_address = self.expander_pin_dict[pin_name].address
        dir_in_code = self.expander_pin_dict[pin_name].dir_in_code
        reg_addx = dir_in_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_register(reg_addx, dev_address)

        # set pin direction to input
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, dir_in_code)
        _logger.debug(":set_expander_pin_direction_in: pin '%s' set to output", pin_name)

        self.expander_pin_dict[pin_name].is_out = False

    def set_expander_pin(self, pin_name: str):
        '''
        Function set gpio pin state to high

        Args:
            `pin_name` (str): name of the pin to set
        '''
        dev_address = self.expander_pin_dict[pin_name].address
        set_code = self.expander_pin_dict[pin_name].set_code
        reg_addx = set_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_register(reg_addx, dev_address)

        # set pin direction to output (also sets to low)
        self.set_expander_pin_direction_out(pin_name)

        # set pin state to high
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, set_code)
        _logger.debug(":set_expander_pin: pin '%s' = set to high", pin_name)

        self.expander_pin_dict[pin_name].is_high = True

    def __apply_code_to_register(self, dev_addx: int, reg_addx: int, reg_val: int, opcode: OpCode):
        """
        Applies an opcode obtained from I2CPinInfo object to a register.

        Args:
            `dev_addx` (int): I2C device address
            `reg_addx` (int): register/port address
            `reg_val` (int): current 8-bit value of register at reg_addx
            `opcode` (OpCode): opcode to apply to register at reg_addx
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

    def clear_expander_pin(self, pin_name: str):
        '''
        Function clear gpio pin state to low
        In:
            `pin_name` (str): name of the pin to set
        '''
        dev_address = self.expander_pin_dict[pin_name].address
        clear_code = self.expander_pin_dict[pin_name].clear_code
        reg_addx = clear_code.reg_address

        # get register value of port this pin belongs to
        reg_val = self.__read_register(reg_addx, dev_address)

        # set pin state to low
        self.__apply_code_to_register(dev_address, reg_addx, reg_val, clear_code)
        _logger.debug(":set_expander_pin: pin '%s' = set to low", pin_name)

        self.expander_pin_dict[pin_name].is_high = False

    def toggle_expander_pin(self, pin_name: str):
        '''
        Function toggle gpio pin state to opposite logic

            High -> Low,
            Low -> High

        Args:
            `pin_name` (str): name of the pin to toggle
        '''
        dev_address = self.expander_pin_dict[pin_name].address
        # set and clear codes for a pin have same reg_addx and mask
        code = self.expander_pin_dict[pin_name].clear_code
        reg_addx = code.reg_address
        pin_mask = code.op_mask

        # get register value of port this pin belongs to
        reg_val = self.__read_register(reg_addx, dev_address)

        # if pin is set to low, set to high and vice-versa
        _logger.debug(":toggle_expander_pin: toggling pin '%s'", pin_name)
        if is_bit_set(reg_val, pin_mask):
            self.clear_expander_pin(pin_name)
        else:
            self.set_expander_pin(pin_name)
