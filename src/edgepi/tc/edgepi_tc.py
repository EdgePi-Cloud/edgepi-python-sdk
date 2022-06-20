'''
Provides a class for interacting with the EdgePi Thermocouple via SPI. 
'''

import logging
import time

from bitstring import Bits
from edgepi.peripherals.spi import SpiDevice
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import code_to_temp
from edgepi.tc.tc_faults import map_fault_status
from edgepi.reg_helper.reg_helper import apply_opcodes
from edgepi.utilities.utilities import filter_dict

_logger = logging.getLogger(__name__)

class EdgePiTC(SpiDevice):
    ''' 
    A class used to represent the EdgePi Thermocouple as an SPI device.
    ''' 
    def __init__(self):
        super().__init__(bus_num=6, dev_ID=2)

    def read_temperatures(self):
        ''' Use to read cold junction and linearized thermocouple temperature measurements '''
        temp_bytes = self.__read_registers(TCAddresses.CJTH_R.value, 5)
        return code_to_temp(temp_bytes)

    def single_sample(self):
        '''
        Conduct a single sampling event. Returns measured temperature in degrees Celsius.

        Returns:
            a tuple containing temperatures for cold junction and linearized thermocouple temperature
        '''
        reg_value = self.__read_register(TCAddresses.CR0_R.value)
        command = reg_value[1] | TCOps.SINGLE_SHOT.value.op_code
        self.__write_to_register(TCAddresses.CR0_W.value, command)
        # there is a time delay between register write and update
        time.sleep(0.5)

        # read cold junction and linearized TC temperatures
        temp_codes = self.read_temperatures()

        _logger.debug(f'single sample codes: {temp_codes}')

        return temp_codes

    def read_faults(self) -> list:
        # read in values from fault status register and fault mask register
        faults = self.__read_register(TCAddresses.SR_R.value)
        fault_bits = Bits(uint=faults[1], length=8)
        masks = self.__read_register(TCAddresses.MASK_R.value)
        fault_masks = Bits(uint=masks[1], length=8)

        fault_msgs = map_fault_status(fault_bits, fault_masks)
        _logger.info(f'read_faults:\n{fault_msgs}')

        return fault_msgs

    def __read_register(self, reg_addx):
        ''' Reads the value of a single register.

            Args:
                reg_addx (TCAddress.Enum.value): the register's address
            
            Returns:
                a list containing two entries: new_data[0] = register address, new_data[1] = register value
        '''
        data = [reg_addx] + [0xFF]
        _logger.debug(f'__read_register: addx = {reg_addx} => data before xfer = {data}')
        new_data = self.transfer(data)
        _logger.debug(f'__read_register: addx = {reg_addx} => data after xfer = {new_data}')
        return new_data

    def __read_registers(self, start_addx:int=0, regs_to_read:int=16):
        ''' read a variable number of registers sequentially
           
            Args:
                start_addx (TCAddress.Enum.value): address of the register to begin the read at.
                regs_to_read (int): number of registers to read, including starting register.
            
            Returns:
                a list containing register values starting from start_addx. Note, first entry 
                is the start address: register values begin from the second entry.
        '''
        data = [start_addx] + [0xFF]*regs_to_read
        _logger.debug(f'__read_registers: shifting in data => {data}')
        new_data = self.transfer(data)
        _logger.debug(f'__read_registers: shifted out data => {new_data}')
        return new_data

    def __write_to_register(self, reg_addx, value):
        ''' write a value to a register.
            
            Args:
                reg_addx (TCAddress.Enum.value): address of the register to write the value to.
                
                value (int): a values to be written to the register.
        '''
        data = [reg_addx] + [value]
        _logger.debug(f'__write_to_registers: shifting in data => {data}')
        new_data = self.transfer(data)
        _logger.debug(f'__write_to_registers: shifted out data => {new_data}')

    def __read_registers_to_map(self):
        ''' Builds a map of write register address to corresponding read register value. Note, each register has 
            a read and write address, but only the read address contains the register's value. Write addresses are only 
            for writing.
            
            Returns:
                a dictionary containing (write_register_address: register_value) entries for each writeable register
        '''
        reg_map = {}
        num_regs = 16
        read_regs_offset = 0x80
        start_addx = TCAddresses.CR0_W.value
        # read values from __read_registers, but log values to corresponding write registers 
        reg_values = self.__read_registers(start_addx-read_regs_offset)
        for addx_offset in range(num_regs):
            reg_map[start_addx+addx_offset] = reg_values[addx_offset+1] # reg_values[0] is start_addx
        _logger.debug(f'__read_registers_to_map => {reg_map}')
        return reg_map

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
        A collective thermocouple settings update method. Use this method when you wish to configure multiple thermocouple settings
        at once.

        Args:
            all (Enum): enum representing a valid hex opcode. Valid opcodes are available in this SDK's tc_constants module.
        '''
        # TODO: update docstring with individual fields for args
        args_list = filter_dict(locals(), 'self')
        _logger.debug(f'set_config args list: \n\n {args_list}\n\n')

        # read value of every write register into dict, starting from CR0_W. Tuples are (write register addx : register_value) pairs.
        reg_values = self.__read_registers_to_map()
        _logger.debug(f'set_config: register values before updates => {reg_values}')

        # updated register values
        apply_opcodes(reg_values, args_list)
        _logger.debug(f'set_config: register values after updates => {reg_values}')

        # only update registers whose values have been changed
        for reg_addx, entry in reg_values.items():
            if entry['is_changed']:
                updated_value = entry['value']
                self.__write_to_register(reg_addx, updated_value)
                _logger.info(f'register value at address ({hex(reg_addx)}) has been updated to ({hex(updated_value)})')      
