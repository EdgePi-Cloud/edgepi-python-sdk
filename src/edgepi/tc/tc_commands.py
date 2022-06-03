import logging
from edgepi.tc.tc_constants import *

_logger = logging.getLogger(__name__)

register_write_map = {
    TCOps.SINGLE_SHOT: TCAddresses.CR0_W,
    TCOps.CLEAR_FAULTS: TCAddresses.CR0_W,
    ConvMode.SINGLE: TCAddresses.CR0_W,
    ConvMode.AUTO: TCAddresses.CR0_W,
    CJMode.ENABLE: TCAddresses.CR0_W,
    CJMode.DISABLE: TCAddresses.CR0_W,
    FaultMode.COMPARATOR: TCAddresses.CR0_W,
    FaultMode.INTERRUPT: TCAddresses.CR0_W,
    NoiseFilterMode.Hz_50: TCAddresses.CR0_W,
    NoiseFilterMode.Hz_60: TCAddresses.CR0_W,
    AvgMode.AVG_1: TCAddresses.CR1_W,
    AvgMode.AVG_2: TCAddresses.CR1_W,
    AvgMode.AVG_4: TCAddresses.CR1_W,
    AvgMode.AVG_8: TCAddresses.CR1_W,
    AvgMode.AVG_16: TCAddresses.CR1_W,
    TCType.TYPE_B: TCAddresses.CR1_W,
    TCType.TYPE_E: TCAddresses.CR1_W,
    TCType.TYPE_J: TCAddresses.CR1_W,
    TCType.TYPE_K: TCAddresses.CR1_W,
    TCType.TYPE_N: TCAddresses.CR1_W,
    TCType.TYPE_R: TCAddresses.CR1_W,
    TCType.TYPE_S: TCAddresses.CR1_W,
    TCType.TYPE_T: TCAddresses.CR1_W,
}

class TCCommands():  
    def temp_to_code(self, temp:float):
        ''' converts a float temperature value to binary code for writing to register '''
        pass

    def code_to_temp(self, code_bytes:list):
        ''' converts register binary temperature code to float value'''
        # generate cold junction temperature and linearized TC temperatures
        try:
            cj_high_byte = code_bytes[1]
            cj_low_byte = code_bytes[2]
            lt_high_byte = code_bytes[3]
            lt_mid_byte = code_bytes[4]
            lt_low_byte = code_bytes[5]
        except IndexError:
            _logger.error(f'single sample failed to read registers')
            return None

        # combine code bytes and eliminate unneeded bits
        cj_code = ((cj_high_byte<<8) + cj_low_byte) >> 2
        # check if code is negative value and update value
        if cj_high_byte & 0x80:
            cj_code -= 2 << (14 - 1)

        # combine code bytes and eliminate unneeded bits
        lt_code = ((lt_high_byte<<16) + (lt_mid_byte<<8) + lt_low_byte) >> 5
        # check if code is negative value and update value
        if lt_high_byte & 0x80:
            lt_code -= 2 << (19 - 1)

        _logger.info(f'Cold Junction Temp: {cj_code*(2**-6)}')  # >> shift the 6 precision bits behind the decimal point
        _logger.info(f'LT TC Temp: {lt_code*(2**-7)}')          # >> shift the 7 precision bits behind the decimal point

        return cj_code, lt_code
    
    def find_register(self, setting):
        ''' 
        Returns address of the write register the setting maps to, or None.

        Args:
            setting (Enum): an enum representing a valid hex opcode
            register_map (dict): a dictionary mapping setting opcodes to registers

        Returns:
            TC_ADDRESS | None: address of the register that setting maps to, 
            or None if opcode is invalid.
        '''
        write_reg = register_write_map.get(setting)
        return write_reg

    
    def get_update_code(self, reg_addx, reg_value, updates: list):
        """ 
        Calls register update method for generating this register's setting update code.

        Args:
            reg_addx (TCAddresses): address of the register to be updated
            reg_value (literal): read value of the register to be updated
            updates (list): a list of setting updates to be applied to this register

        Returns:
            literal: value representing binary update instruction 
        """        
        if reg_addx == TCAddresses.CR0_W.value:
            code = self.generate_cr0_update(reg_value, updates)
        elif reg_addx == TCAddresses.CR1_W.value:
            code = self.generate_cr1_update(reg_value, updates)

        return code

    # TODO: update code generation needs to be more abstract, one method
    # should be able to handle all register configs
    def generate_cr0_update(self, reg_value, updates: list):
        ''' 
        Combines list of update commands into a single write command for cr0

        Args:
            reg_value (literal): the read value of the register
            updates (list): a list of valid hex update opcodes for cr0

        Returns:
            updated register value to be written back to register

        Raises:
            ValueError: if an invalid CR0 opcode is passed as argument in updates
        '''
        # TODO: validate user isn't trying to pass multiple commands for the same setting
        value = reg_value
        # perform each update on value
        for op_code in updates:
            # validate only cr0 ops allowed
            if self.find_register(op_code) != TCAddresses.CR0_W:
                raise ValueError('Invalid CR0 opcode.')
            # TODO: fix NoneType value here
            print(f'op_code = {op_code}')
            if 'f' in hex(op_code.value):
                value &= op_code.value
            else:
                value |= op_code.value

        return value
                
    def generate_cr1_update(self, reg_value, updates: list):
        if len(updates) > 2:
            raise ValueError('too many settings updates passed to CR1, only two settings are configurable at once')
        elif len(updates) > 1 and type(updates[0]) == type(updates[1]):
            # TODO: this misses the case where both voltage mode and tc_type updates are passed in
            raise ValueError('the same setting cannot receive two update commands at once')
        for opcode in updates:
            if type(opcode) == AvgMode:
                mask = 0x0F
            elif type(opcode) == TCType or type(opcode) == VoltageMode:
                mask = 0xF0
            else:
                raise ValueError(f'{opcode} is an invalid CR1 setting update code')
            
            # clear this byte, and rewrite it with new setting
            reg_value = reg_value & mask | opcode.value

        return reg_value
