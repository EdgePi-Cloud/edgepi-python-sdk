'''
Provides a class for interacting with the EdgePi Thermocouple via SPI. 
'''

import logging
import time

from edgepi.peripherals.spi import SpiDevice
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TCCommands

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EdgePiTC(SpiDevice):
    ''' 
    A class used to represent the EdgePi Thermocouple as an SPI device.
    '''
    tc_coms = TCCommands()

    def __init__(self):
        super().__init__(bus_num=6, dev_ID=2)

    # TODO: use enum instead of int
    def set_averaging_mode(self, num_samples:AvgMode):
        '''
        Sets number of measurements made per sampling event.   
        Parameters: and interger from the set {1, 2, 4, 8, 16}. Default = 1. 
        '''
        self.set_config(average_mode=num_samples)

    def __read_temps(self):
        temp_bytes = self.read_registers(TCAddresses.CJTH_R.value, 5)
        return self.tc_coms.code_to_temp(temp_bytes)

    def single_sample(self):
        '''
        Conduct a single sampling event. Returns measured temperature in degrees Celsius.
        Parameters: a string representing a file path to log results to (optional). Note,
        thermocouple Conversion Mode must be set to Normally Off to enable single sampling.

        Returns:
            tuple containing temperature codes for cold junction and linearized thermocouple temperature
        '''
        # TODO: disable auto mode on call, or let user decide?
        reg_value = self.read_register(TCAddresses.CR0_R.value)
        command = reg_value[1] | TCOps.SINGLE_SHOT.value
        self.write_to_registers(TCAddresses.CR0_W.value, [command])
        # there is a time delay between register write and update
        time.sleep(0.5)

        # read cold junction and linearized TC temperatures
        temp_codes = self.__read_temps()

        _logger.info(f'single sample codes: {temp_codes}')

        return temp_codes

    # TODO: document how to use auto mode for users
    def auto_sample_mode(self):
        '''
        Conduct sampling events continuously. Returns measured temperature in degrees Celsius..
        '''
        self.set_config(conversion_mode=ConvMode.AUTO)

    def set_type(self, tc_type:TCType):
        '''
        Set thermocouple type. 
        Args: 
            tc_type (TCType): a string from the set {B,E,J,K,N,R,S,T}.
        '''
        self.set_config(tc_type=tc_type)

    def set_average_mode(self, avg_mode:AvgMode):
        self.set_config(average_mode=avg_mode)

    def read_register(self, reg_addx):
        ''' Reads the value of a single register.

            Args:
                reg_addx (int|TCAddress.Enum.value): the register's address
            
            Returns:
                a list new_data containing two entries: new_data[0] = register address, new_data[1] = register value
        '''
        data = [reg_addx] + [0xFF]
        _logger.info(f'read_register: addx = {reg_addx} => data before xfer = {data}')
        new_data = super().transfer(data)
        _logger.info(f'read_register: addx = {reg_addx} => data after xfer = {new_data}')
        return new_data

    def read_registers(self, start_addx:int=0, regs_to_read:int=16):
        ''' read a variable number of registers sequentially
           
            Args:
                start_addx (int): address of the register to begin the read at.
                regs_to_read (int): number of registers to read, including starting register.
            
            Returns:
                a list containing register values starting from start_addx. Note, first entry 
                is the start address: register values begin from the second entry.
        '''
        data = [start_addx] + [0xFF]*regs_to_read
        _logger.info(f'read_registers: shifting in data => {data}')
        new_data = super().transfer(data)
        _logger.info(f'read_registers: shifted out data => {new_data}')
        return new_data

    # TODO: change to 'private' methods
    def write_to_registers(self, start_addx, values):
        ''' write to a variable number of registers sequentially.
            
            Args:
                start_addx (int): address of the register to begin the write at.
                
                values (list): a list of values to be written to registers. CAUTION: register writes occur
                sequentially from start register and include as many registers as there are entries in the list.
                All registers in this range will be overwritten: it is recommended to read the register values first,
                in case a register write includes bad values. 
        '''
        data = [start_addx] + values
        _logger.info(f'write_to_registers: shifting in data => {data}')
        new_data = super().transfer(data)
        _logger.info(f'write_to_registers: shifted out data => {new_data}')

    def __map_updates_to_address(self, args_list:list) -> list:
        ''' Maps a list of register update codes to their corresponding registers
            
            Args:
                args_list (list): a list of valid register opcodes
            
            Returns:
                a dictionary containing {register_address : [update_codes_list]} tuples
        '''
        reg_updates_map = {}
        for setting in args_list:
            if setting is not None:
                reg_addx = self.tc_coms.find_register(setting)
                # invalid setting opcodes return None
                if reg_addx is None:
                    continue
                if reg_addx in reg_updates_map:
                    reg_updates_map[reg_addx].append(setting)
                else:
                    reg_updates_map[reg_addx] = [setting]
        _logger.info(f'__map_updates_to_address: reg_updates_map => {reg_updates_map}')
        return reg_updates_map

    def __read_registers_to_map(self):
        ''' Builds a map of write register address to corresponding read register value. Note, each register has 
            a read and write address, but only the read address contains the register's value. Write addresses are only 
            for writing.
            
            Returns:
                a dictionary containing (write_register_address: read_register_value) entries for each writeable register
        '''
        reg_map = {}
        num_regs = 16
        read_regs_offset = 0x80
        start_addx = TCAddresses.CR0_W.value
        # read values from read_registers, but log values to corresponding write registers 
        reg_values = self.read_registers(start_addx-read_regs_offset)
        for addx_offset in range(num_regs):
            reg_map[start_addx+addx_offset] = reg_values[addx_offset+1] # reg_values[0] is start_addx
        _logger.info(f'__read_registers_to_map => {reg_map}')
        return reg_map

    # TODO: make issue for temp setting
    def set_config(
        self,
        conversion_mode: ConvMode = None,  
        oc_fault_mode: FaultMode = None, 
        cold_junction_mode: CJMode = None, 
        fault_mode: FaultMode = None,
        noise_filter_mode: NoiseFilterMode = None,
        average_mode: AvgMode = None,
        tc_type: TCType = None,
        voltage_mode: VoltageMode = None,
        fault_mask: FaultMasks = None,
        cj_high_threshold: int = None,
        cj_low_threshold: int = None,
        lt_high_threshold: int = None,
        lt_high_threshold_decimals: DecBits = None,
        lt_low_threshold: int = None,
        lt_low_threshold_decimals: DecBits = None,
        cj_offset: int = None,
        cj_offset_decimals: DecBits = None,
        ):
        '''
        A collective thermocouple settings update method.

        Args:
            all (Enum): enum representing a valid hex opcode. See tc_constants.py for valid opcodes.

        Returns:
            a list whose entries represent the value to be written to each write register, starting from CR0_W
        '''
        args_list = [conversion_mode, oc_fault_mode, cold_junction_mode, fault_mode, noise_filter_mode,
                    average_mode, tc_type, voltage_mode, fault_mask, cj_high_threshold, cj_low_threshold,
                    lt_high_threshold, lt_high_threshold_decimals, lt_low_threshold, lt_low_threshold_decimals,
                    cj_offset, cj_offset_decimals]
        _logger.info(f'set_config args list: {args_list}')

        # map each command to its register and build dictionary of (register_address : [command_list]) tuples. 
        # this also validates the command is a valid opcode.
        reg_updates_map = self.__map_updates_to_address(args_list)

        # read value of every write register into dict, starting from CR0_W. Tuples are (write register addx : register_value) pairs.
        reg_values = self.__read_registers_to_map()

        # for each register the user entered updates for, combine all settings updates into one command, 
        # and modify corresponding register value in list. If no updates, keep the read-in register value.
        for addx, op_array in reg_updates_map.items():
            reg_value = reg_values.get(addx.value)
            # generate update code for register
            update_code = self.tc_coms.get_update_code(addx.value, reg_value, op_array)
            # modify register value entry to be written back
            reg_values[addx.value] = update_code

        update_bytes = [TCAddresses.CR0_W.value] + list(reg_values.values())
        _logger.info(f'set-config: writing update bytes -> {update_bytes}')

        # TODO: validate registers not updated by user have not been modified and all entries are valid opcodes
        # write multi-byte update transfer starting from CR0_W
        self.transfer(update_bytes)

        return update_bytes

if __name__ == '__main__':
    tc_dev = EdgePiTC()
    # tc_dev.set_config(conversion_mode=ConvMode.AUTO, tc_type=TCType.TYPE_N)
    # values = [0,3,255,127,192,127,255,128,0,0,0,0]
    print('cr1 value before transfer')
    tc_dev.read_registers()
    # tc_dev.set_average_mode(AvgMode.AVG_4)
    print('cr1 value after transfer')
    tc_dev.read_registers()
    tc_dev.single_sample()
    # tc_dev.auto_sample()
