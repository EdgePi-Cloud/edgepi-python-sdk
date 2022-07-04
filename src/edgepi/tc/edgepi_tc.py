'''
Provides a class for interacting with the EdgePi Thermocouple via SPI. 
'''

import logging
import time

from bitstring import Bits
from edgepi.peripherals.spi import SpiDevice
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import code_to_temp, TempCode, tempcode_to_opcode, TempType
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
        # TODO: replace with time delay calculation
        time.sleep(0.5)

        # read cold junction and linearized TC temperatures
        temp_codes = self.read_temperatures()

        _logger.debug(f'single sample codes: {temp_codes}')

        return temp_codes

    def read_faults(self, filter_at_fault=True) -> list:
        ''' Read information about thermocouple fault status.

            Args:
                filter_at_fault (bool): set to True to return only Faults that are currently asserting

            Returns:
                a dictionary mapping each thermocouple fault type to a Fault object holding 
                information about its current status. See :obj:`tc.tc_faults.Fault` for details about the Fault class.
        '''
        # read in values from fault status register and fault mask register
        faults = self.__read_register(TCAddresses.SR_R.value)
        fault_bits = Bits(uint=faults[1], length=8)
        masks = self.__read_register(TCAddresses.MASK_R.value)
        fault_masks = Bits(uint=masks[1], length=8)

        fault_msgs = map_fault_status(fault_bits, fault_masks)
        _logger.info(f'read_faults:\n{fault_msgs}')

        # filter out normal status Fault objects
        if filter_at_fault:
            fault_msgs = { fault_type:fault for (fault_type,fault) in fault_msgs.items() if fault.at_fault == True }

        return fault_msgs

    def overwrite_cold_junction_temp(self, cj_temp:int, cj_temp_decimals:DecBits6):
        ''' Write temperature values to the cold-junction sensor. Cold-junction sensing
            must be disabled (using set_config method) in order for values to be written
            to the cold-junction sensor.

            Args:
                cj_temp (int): the integer value of the temperature to be written to the cold-junction sensor

                cj_temp_decimals (DecBits6): the decimal value of the temperature to be written to the cold-junction sensor
        '''
        self.set_config(cj_temp=cj_temp, cj_temp_decimals=cj_temp_decimals)

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

    def __write_to_register(self, reg_addx:int, value:int):
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

    def __update_registers_from_dict(self, reg_values:dict):
        ''' Applies updated register values contained in a dictionary of register values

            Args:
                reg_values (dict): a dictionary containing { register_address: entry } pairs, where
                                    entry is a dictionary holding 'value' and 'is_changed' keys.
        '''
        for reg_addx, entry in reg_values.items():
            if entry['is_changed']:
                updated_value = entry['value']
                self.__write_to_register(reg_addx, updated_value)
                _logger.info(f'register value at address ({hex(reg_addx)}) has been updated to ({hex(updated_value)})')

    def set_config(
        self,
        conversion_mode: ConvMode = None,  
        oc_fault_mode: OpenCircuitMode = None,
        cold_junction_mode: CJMode = None, 
        fault_mode: FaultMode = None,
        noise_filter_mode: NoiseFilterMode = None,
        average_mode: AvgMode = None,
        tc_type: TCType = None,
        voltage_mode: VoltageMode = None,
        cj_high_mask: CJHighMask = None,
        cj_low_mask: CJLowMask = None,
        tc_high_mask: TCHighMask = None,
        tc_low_mask: TCLowMask = None,
        ovuv_mask: OvuvMask = None,
        open_mask: OpenMask = None,
        cj_high_threshold: int = None,
        cj_low_threshold: int = None,
        lt_high_threshold: int = None,
        lt_high_threshold_decimals: DecBits4 = None,
        lt_low_threshold: int = None,
        lt_low_threshold_decimals: DecBits4 = None,
        cj_offset: int = None,
        cj_offset_decimals: DecBits4 = None,
        cj_temp: int = None,
        cj_temp_decimals: DecBits6 = None
        ):
        '''
        A collective thermocouple settings update method. Use this method to configure thermocouple settings. This method
        allows you to configure settings either individually, or collectively (more than one at a time).

        Args:
            all (Enum): enum representing a valid hex opcode. Valid opcodes are available in this SDK's tc_constants module.

                conversion_mode (ConvMode): enable manual or automatic sampling

                oc_fault_mode (OpenCircuitMode): set open circuit fault detection mode

                cold_junction_mode (CJMode): enable or disable cold junction sensor

                fault_mode (FaultMode): set fault reading mode

                noise_filter_mode (NoiseFilterMode): set which noise frequency to reject

                average_mode (AvgMode): number of samples to average per temperature measurement

                tc_type (TCType): set thermocouple type

                voltage_mode (VoltageMode): set input voltage range

                cj_high_mask (CJHighMask): choose whether to mask CJHIGH fault from asserting through the FAULT pin
                
                cj_low_mask (CJLowMask): choose whether to mask CJLOW fault from asserting through the FAULT pin
                
                tc_high_mask (TCHighMask): choose whether to mask TCHIGH fault from asserting through the FAULT pin
                
                tc_low_mask (TCLowMask): choose whether to mask TCLOW fault from asserting through the FAULT pin
                
                ovuv_mask (OvuvMask): choose whether to mask OVUV fault from asserting through the FAULT pin
                
                open_mask (OpenMask): choose whether to mask OPEN fault from asserting through the FAULT pin

                cj_high_threshold (int): set cold junction temperature upper threshold. If cold junction temperature rises
                above this limit, the FAULT output will assert

                cj_low_threshold (int): set cold junction temperature lower threshold. If cold junction temperature falls
                below this limit, the FAULT output will assert

                lt_high_threshold (int): set thermocouple hot junction temperature upper threshold. If thermocouple hot junction 
                temperature rises above this limit, the FAULT output will assert

                lt_high_threshold_decimals (DecBits4): set thermocouple hot junction temperature upper threshold decimal value.

                lt_low_threshold (int): set thermocouple hot junction temperature lower threshold. If thermocouple hot junction 
                temperature falls below this limit, the FAULT output will assert

                lt_low_threshold_decimals (DecBits4): set thermocouple hot junction temperature lower threshold decimal value.

                cj_offset (int): set cold junction temperature offset.

                cj_offset_decimals (DecBits4): set cold junction temperature offset decimal value.

                cj_temp (int): write values to cold-junction sensor. Only use when cold-junction is disabled.

                cj_temp_decimals (DecBits6): set decimal value for cj_temp
        '''
        # filter out self from args
        args_dict = filter_dict(locals(), 'self', None)
        _logger.debug(f'set_config: args dict:\n\n {args_dict}\n\n')

        # extract non-temperature setting opcodes from Enums
        ops_list = [entry.value for entry in args_dict.values() if issubclass(entry.__class__, Enum) and type(entry.value) is OpCode]

        # process temperature setting
        tempcodes = []
        tempcodes.append(TempCode(cj_high_threshold, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION))
        tempcodes.append(TempCode(cj_low_threshold, DecBits4.P0, 7, 0, 0, TCAddresses.CJLF_W.value, TempType.COLD_JUNCTION))
        tempcodes.append(TempCode(lt_high_threshold, lt_high_threshold_decimals, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE))
        tempcodes.append(TempCode(lt_low_threshold, lt_low_threshold_decimals, 11, 4, 0, TCAddresses.LTLFTH_W.value, TempType.THERMOCOUPLE))
        tempcodes.append(TempCode(cj_offset, cj_offset_decimals, 3, 4, 0, TCAddresses.CJTO_W.value, TempType.COLD_JUNCTION_OFFSET))
        tempcodes.append(TempCode(cj_temp, cj_temp_decimals, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION))

        for tempcode in tempcodes:
            ops_list += tempcode_to_opcode(tempcode)
        _logger.debug(f'set_config: ops_list:\n\n{ops_list}\n\n')
        
        # read value of every write register into dict, starting from CR0_W. Tuples are (write register addx : register_value) pairs.
        reg_values = self.__read_registers_to_map()
        _logger.debug(f'set_config: register values before updates:\n\n{reg_values}\n\n')

        # updated register values
        apply_opcodes(reg_values, ops_list)
        _logger.debug(f'set_config: register values after updates:\n\n{reg_values}\n\n')

        # only update registers whose values have been changed
        self.__update_registers_from_dict(reg_values)
