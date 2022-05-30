from array import array
from tc.tc_constants import *

register_write_map = {
    TC_OPS.SINGLE_SHOT: TC_ADDRESSES.CR0_W,
    TC_OPS.CLEAR_FAULTS: TC_ADDRESSES.CR0_W,
    CONV_MODE.SINGLE: TC_ADDRESSES.CR0_W,
    CONV_MODE.AUTO: TC_ADDRESSES.CR0_W,
    CJ_MODE.ENABLE: TC_ADDRESSES.CR0_W,
    CJ_MODE.DISABLE: TC_ADDRESSES.CR0_W,
    FAULT_MODE.COMPARATOR: TC_ADDRESSES.CR0_W,
    FAULT_MODE.INTERRUPT: TC_ADDRESSES.CR0_W,
    NOISE_FILTER_MODE.Hz_50: TC_ADDRESSES.CR0_W,
    NOISE_FILTER_MODE.Hz_60: TC_ADDRESSES.CR0_W,
    AVG_MODE.AVG_1: TC_ADDRESSES.CR1_W,
    AVG_MODE.AVG_2: TC_ADDRESSES.CR1_W,
    AVG_MODE.AVG_4: TC_ADDRESSES.CR1_W,
    AVG_MODE.AVG_8: TC_ADDRESSES.CR1_W,
    AVG_MODE.AVG_16: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_B: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_E: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_J: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_K: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_N: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_R: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_S: TC_ADDRESSES.CR1_W,
    TC_TYPE.TYPE_T: TC_ADDRESSES.CR1_W,
}

class TCCommands():
    def read_register(self):
        ''' read the value of any MAX31856 register '''
        pass

    def write_to_register(self, reg_addx):
        ''' write to any MAX31856 register '''
        pass

    def temp_to_code(self, temp:float):
        ''' converts a float temperature value to binary code for writing to register '''
        pass

    def code_to_temp(self, code):
        ''' converty register binary temperature code to float value'''
        pass
    
    def find_register(self, setting):
        ''' 
        Returns address of the register the setting maps to, or None.

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
            reg_addx (TC_ADDRESSES): address of the register to be updated
            reg_value (literal): read value of the register to be updated
            updates (list): a list of setting updates to be applied to this register

        Returns:
            literal: value representing binary update instruction 
        """        
        if reg_addx == TC_ADDRESSES.CR0_W:
            code = self.generate_cr0_update(reg_value, updates)
        elif reg_addx == TC_ADDRESSES.CR1_W:
            code = self.generate_cr1_update(reg_value, updates)

        return code

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
        value = reg_value
        # perform each update on value
        for op_code in updates:
            # validate only cr0 ops allowed
            if self.find_register(op_code) != TC_ADDRESSES.CR0_W:
                raise ValueError('Invalid CR0 opcode.')
            if 'f' in hex(op_code.value):
                value &= op_code.value
            else:
                value |= op_code.value

        return value
                
    def generate_cr1_update(self, reg_value, updates: list):
        pass
