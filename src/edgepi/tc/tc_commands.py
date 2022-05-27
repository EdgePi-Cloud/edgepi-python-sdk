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

    def write_to_register(self):
        ''' write to any MAX31856 register '''
        pass

    def temp_to_code(self, temp:float):
        ''' converts a float temperature value to binary code for writing to register '''
        pass

    def code_to_temp(self, code):
        ''' converty register binary temperature code to float value'''
        pass
    
    @staticmethod
    def find_register(setting, register_map: dict = register_write_map):
        ''' 
        Returns address of the register the setting maps to, or None.

        Parameters:
            setting (enum): an enum representing a valid hex opcode
            register_map (dict): a dictionary mapping setting opcodes to registers

        Returns:
            enum whose value is the address of the register that setting maps to, or None if opcode is invalid

        Raises:
            AttributeError
                If a container other than a dictionary is passed in as register_map
        '''
        write_reg = register_map.get(setting)
        return write_reg

    @staticmethod
    def update_settings(reg_addx, updates):
        ''' calls appropriate register update method for handling this register's setting update '''
        pass
