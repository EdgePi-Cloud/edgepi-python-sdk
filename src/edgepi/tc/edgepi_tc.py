"""
Module for interacting with the EdgePi Thermocouple via SPI.
"""


import logging
import time
from enum import Enum

from bitstring import Bits
from edgepi.peripherals.spi import SpiDevice
from edgepi.tc.tc_commands import code_to_temp, TempCode, tempcode_to_opcode, TempType
from edgepi.tc.tc_constants import (
    NUM_WRITE_REGS,
    AvgMode,
    CJHighMask,
    CJLowMask,
    CJMode,
    ConvMode,
    DecBits4,
    DecBits6,
    FaultMode,
    NoiseFilterMode,
    Masks,
    OpenCircuitMode,
    OpenMask,
    OvuvMask,
    TCAddresses,
    TCHighMask,
    TCLowMask,
    TCOps,
    TCType,
    VoltageMode,
)
from edgepi.tc.tc_faults import map_fault_status
from edgepi.reg_helper.reg_helper import OpCode, apply_opcodes
from edgepi.utilities.utilities import filter_dict
from edgepi.tc.tc_conv_time import calc_conv_time

_logger = logging.getLogger(__name__)

# pylint: disable=too-many-instance-attributes
class TCState:
    """
    A Class to store TC state
    """
    def __init__(self):
        # cmode = True = auto conv mode
        self.cmode = None
        # one_shot = True = single shot
        self.one_shot = None
        self.open_circuit_fault = None
        # cj = True = disabled
        self.cold_junction = None
        # fault = True = interrupt mode
        self.fault = None
        self.fault_clr = None
        # noise_rejection = true = 50Hz
        self.noise_rejection = None
        self.sampling_average = None
        self.tc_type = None

    def __tc_get_state_bool(self, cr_reg: int, mask:int):
        """
        Populate the state value using the cr_regs
        Args:
            cr_reg (int): value of one of configuration register either CR0 | CR1
            bitmask (int): bit mask
        Return:
            Bool
        """
        return (cr_reg & mask) == mask

    def __tc_get_state(self, cr_reg: int, mask: int):
        """
        Populate thes state value using the cr_regs
        Args:
            cr_reg (int): value of one of configuration register either CR0 | CR1
            bitmask (int): bit mask
        Return:
            int
        """
        reg_val = cr_reg&mask
        if mask == Masks.CR1_HIGH_MASK.value:
            state = TCType.get_tc_type(reg_val=reg_val)
        else:
            state = AvgMode.get_avg_mode(reg_val=reg_val)
        return state

    def tc_update_state(self, cr_regs: list):
        """
        Update configurations using configuration registers
        """
        # cmode = True = auto conv mode
        self.cmode = self.__tc_get_state_bool(cr_regs[0], ConvMode.AUTO.value.op_code)
        # one_shot = True = single shot
        self.one_shot = self.__tc_get_state_bool(cr_regs[0], TCOps.SINGLE_SHOT.value.op_code)
        self.open_circuit_fault = None
        # cj = True = disabled
        self.cold_junction = self.__tc_get_state_bool(cr_regs[0], CJMode.DISABLE.value.op_code)
        # fault = True = interrupt mode
        self.fault = self.__tc_get_state_bool(cr_regs[0], FaultMode.INTERRUPT.value.op_code)
        self.fault_clr = None
        # noise_rejection = true = 50Hz
        self.noise_rejection = self.__tc_get_state_bool(cr_regs[0],
                                                        NoiseFilterMode.HZ_50.value.op_code)
        # sampling_average = 0x00 =1sample,
        #                    0x10 = 2 samples,
        #                    0x20 = 4 samples,
        #                    0x30 = 8 samples,
        #                    0x40 = 16 samples
        self.sampling_average = self.__tc_get_state(cr_regs[1], Masks.CR1_LOW_MASK.value)
        #TC_TYPE = 0->7 = B->E->J->K->N->R->S->T
        self.tc_type = self.__tc_get_state(cr_regs[1], Masks.CR1_HIGH_MASK.value)

class EdgePiTC(SpiDevice):
    """
    A class used to represent the EdgePi Thermocouple as an SPI device.
    """

    # default MAX31856 register values for writeable registers
    default_reg_values = {
        TCAddresses.CR0_W.value: 0x00,
        TCAddresses.CR1_W.value: 0x03,
        TCAddresses.MASK_W.value: 0xFF,
        TCAddresses.CJHF_W.value: 0x7F,
        TCAddresses.CJLF_W.value: 0xC0,
        TCAddresses.LTHFTH_W.value: 0x7F,
        TCAddresses.LTHFTL_W.value: 0xFF,
        TCAddresses.LTLFTH_W.value: 0x80,
        TCAddresses.LTLFTL_W.value: 0x00,
        TCAddresses.CJTO_W.value: 0x00,
        TCAddresses.CJTH_W.value: 0x00,
        TCAddresses.CJTL_W.value: 0x00,
    }

    def __init__(self):
        super().__init__(bus_num=6, dev_id=2)
        self.tc_state = TCState()

    def read_temperatures(self):
        """Use to read cold junction and linearized thermocouple temperature measurements"""
        temp_bytes = self.__read_registers(TCAddresses.CJTH_R.value, 5)
        return code_to_temp(temp_bytes)

    def single_sample(self, safe_delay: bool = True):
        """Conduct a single sampling event. Returns measured temperature in degrees Celsius.

        Args:
            safe_delay (bool): manual sampling requires a time delay between triggering
                            the sampling and the measured values being available for reading.
                            Set to True to enable the maximum time delay, or False to enable
                            a shorter time delay. Note, using the shorter time delay offers
                            a higher chance of reading temperature values before the new
                            measurement is available.
        Returns:
            a tuple containing temperatures for cold junction
            and linearized thermocouple temperature
        """
        cr0_value = self.__read_register(TCAddresses.CR0_R.value)
        cr1_value = self.__read_register(TCAddresses.CR1_R.value)
        command = cr0_value[1] | TCOps.SINGLE_SHOT.value.op_code
        self.__write_to_register(TCAddresses.CR0_W.value, command)

        # compute time delay between register write and update
        conv_time = calc_conv_time(cr0_value[1], cr1_value[1], safe_delay)
        time.sleep(conv_time / 1000)

        # read cold junction and linearized TC temperatures
        temp_codes = self.read_temperatures()

        _logger.debug(f"single sample codes: {temp_codes}")

        return temp_codes

    def read_faults(self, filter_at_fault=True) -> list:
        """Read information about thermocouple fault status.

        Args:
            filter_at_fault (bool): set to True to return only Faults that are currently asserting

        Returns:
            a dictionary mapping each thermocouple fault type to a Fault object holding
            information about its current status.
            See :obj:`tc.tc_faults.Fault` for details about the Fault class.
        """
        # read in values from fault status register and fault mask register
        faults = self.__read_register(TCAddresses.SR_R.value)
        fault_bits = Bits(uint=faults[1], length=8)
        masks = self.__read_register(TCAddresses.MASK_R.value)
        fault_masks = Bits(uint=masks[1], length=8)

        fault_msgs = map_fault_status(fault_bits, fault_masks)
        _logger.info(f"read_faults:\n{fault_msgs}")

        # filter out normal status Fault objects
        if filter_at_fault:
            fault_msgs = {
                fault_type: fault
                for (fault_type, fault) in fault_msgs.items()
                if fault.at_fault is True
            }

        return fault_msgs

    def clear_faults(self):
        """
        When thermocouple is in Interrupt Fault Mode, clears all bits in Fault Status Register,
        and deasserts FAULT pin output. Note that the FAULT output and the fault bit may
        reassert immediately if the fault persists. If thermocouple is in Comparator Fault Mode,
        this will have no effect on the thermocouple.
        """
        cr0 = self.__read_register(TCAddresses.CR0_R.value)
        command = cr0[1] | TCOps.CLEAR_FAULTS.value.op_code
        self.__write_to_register(TCAddresses.CR0_W.value, command)

    def overwrite_cold_junction_temp(self, cj_temp: int, cj_temp_decimals: DecBits6):
        """
        Write temperature values to the cold-junction sensor.
        Cold-junction sensing must be disabled (using set_config method)
        in order for values to be written to the cold-junction sensor.

        Args:
            cj_temp (int): the integer value of the temperature
                            to be written to the cold-junction sensor

            cj_temp_decimals (DecBits6): the decimal value of the temperature
                                        to be written to the cold-junction sensor

        Raises:
            ColdJunctionOverwriteError: if value is written to cold-junction temperature
                                    registers while cold-junction sensing is not disabled.
        """
        self.set_config(cj_temp=cj_temp, cj_temp_decimals=cj_temp_decimals)

    def reset_registers(self):
        """
        Resets register values to factory default values. Please refer to MAX31856
        datasheet or this module's documentation for these values. Note this will
        not reset the CJTH and CJTL registers, as these require cold-junction
        sensing to be disabled in order to update the values.
        """
        for addx, value in self.default_reg_values.items():
            self.__write_to_register(addx, value)

    def __read_register(self, reg_addx):
        """Reads the value of a single register.

        Args:
            reg_addx (TCAddress.Enum.value): the register's address

        Returns:
            a list containing two entries:
            new_data[0] = register address, new_data[1] = register value
        """
        data = [reg_addx] + [0xFF]
        with self.spi_open():
            new_data = self.transfer(data)
        _logger.debug(f"__read_register: addx = {reg_addx} => data after xfer = {new_data}")
        return new_data

    def __read_registers(self, start_addx: int = 0, regs_to_read: int = 16):
        """read a variable number of registers sequentially

        Args:
            start_addx (TCAddress.Enum.value): address of the register to begin the read at.
            regs_to_read (int): number of registers to read, including starting register.

        Returns:
            a list containing register values starting from start_addx. Note, first entry
            is the start address: register values begin from the second entry.
        """
        data = [start_addx] + [0xFF] * regs_to_read
        with self.spi_open():
            new_data = self.transfer(data)
        _logger.debug(f"__read_registers: shifted out data => {new_data}")
        return new_data

    def __write_to_register(self, reg_addx: int, value: int):
        """write a value to a register.

        Args:
            reg_addx (TCAddress.Enum.value): address of the register to write the value to.

            value (int): a values to be written to the register.
        """
        data = [reg_addx] + [value]
        _logger.debug(f"__write_to_registers: shifting in data => {data}")
        with self.spi_open():
            self.transfer(data)

    def __read_registers_to_map(self):
        """
        Builds a map of write register address to corresponding read register value.
        Note, each register has a read and write address, but only the read address
        contains the register's value. Write addresses are only for writing.

        Returns:
            a dictionary containing (write_reg_address: register_value) entries
            for each writeable register.
        """
        reg_map = {}
        num_regs = NUM_WRITE_REGS
        read_regs_offset = 0x80
        start_addx = TCAddresses.CR0_W.value
        # read values from __read_registers, but log values to corresponding write registers
        reg_values = self.__read_registers(start_addx - read_regs_offset)
        for addx_offset in range(num_regs):
            reg_map[start_addx + addx_offset] = reg_values[
                addx_offset + 1
            ]  # reg_values[0] is start_addx
        _logger.debug(f"__read_registers_to_map => {reg_map}")
        return reg_map

    def __update_registers_from_dict(self, reg_values: dict):
        """Applies updated register values contained in a dictionary of register values

        Args:
            reg_values (dict): a dictionary containing { register_address: entry } pairs, where
                                entry is a dictionary holding 'value' and 'is_changed' keys.
        """
        for reg_addx, entry in reg_values.items():
            if entry["is_changed"]:
                updated_value = entry["value"]
                self.__write_to_register(reg_addx, updated_value)
                _logger.debug(
                    f"register value at address ({hex(reg_addx)})"
                    f" has been updated to ({hex(updated_value)})")

    def __get_tc_type(self):
        """Returns the currently configured thermocouple type"""
        cr1 = Bits(uint=self.__read_register(TCAddresses.CR1_R.value)[1], length=8)
        tc_bits = cr1[-4:].uint
        for tc in TCType:
            if not isinstance(tc.value, int) and tc.value.op_code == tc_bits:
                return tc
        return None

    def __get_cj_status(self):
        "Returns the current cold-junction sensing status (on/off)"
        cr0 = Bits(uint=self.__read_register(TCAddresses.CR0_R.value)[1], length=8)
        return cr0[4]

    def __process_temperature_settings(
        self,
        cj_high_threshold: int,
        cj_low_threshold: int,
        lt_high_threshold: int,
        lt_high_threshold_decimals: DecBits4,
        lt_low_threshold: int,
        lt_low_threshold_decimals: DecBits4,
        cj_offset: int,
        cj_offset_decimals: DecBits4,
        cj_temp: int,
        cj_temp_decimals: DecBits6,
        tc_type: TCType,
        ops_list: list,
    ):
        """generates OpCodes for temperature settings and appends to external OpCodes list"""
        tempcodes = [
            TempCode(
                cj_high_threshold,
                DecBits4.P0,
                7,
                0,
                0,
                TCAddresses.CJHF_W.value,
                TempType.COLD_JUNCTION,
            ),
            TempCode(
                cj_low_threshold,
                DecBits4.P0,
                7,
                0,
                0,
                TCAddresses.CJLF_W.value,
                TempType.COLD_JUNCTION,
            ),
            TempCode(
                lt_high_threshold,
                lt_high_threshold_decimals,
                11,
                4,
                0,
                TCAddresses.LTHFTH_W.value,
                TempType.THERMOCOUPLE,
            ),
            TempCode(
                lt_low_threshold,
                lt_low_threshold_decimals,
                11,
                4,
                0,
                TCAddresses.LTLFTH_W.value,
                TempType.THERMOCOUPLE,
            ),
            TempCode(
                cj_offset,
                cj_offset_decimals,
                3,
                4,
                0,
                TCAddresses.CJTO_W.value,
                TempType.COLD_JUNCTION_OFFSET,
            ),
            TempCode(
                cj_temp, cj_temp_decimals, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION
            ),
        ]

        # in case the user updates thermocouple type as well
        tc_type = tc_type if tc_type is not None else self.__get_tc_type()
        cj_status = self.__get_cj_status()

        for tempcode in tempcodes:
            ops_list += tempcode_to_opcode(tempcode, tc_type, cj_status)
        _logger.debug(f"set_config: ops_list:\n\n{ops_list}\n\n")

    def set_config(
        self,
        conversion_mode: ConvMode = None,
        open_circuit_mode: OpenCircuitMode = None,
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
        cj_temp_decimals: DecBits6 = None,
    ):
        """
        A collective thermocouple settings update method.
        Use this method to configure thermocouple settings.
        This method allows you to configure settings either individually,
        or collectively (more than one at a time).

        Args:
            conversion_mode (ConvMode): enable manual or automatic sampling

            oc_fault_mode (OpenCircuitMode): set open circuit fault detection mode

            cold_junction_mode (CJMode): enable or disable cold junction sensor

            fault_mode (FaultMode): set fault reading mode

            noise_filter_mode (NoiseFilterMode): set which noise frequency to reject

            average_mode (AvgMode): number of samples to average per temperature measurement

            tc_type (TCType): set thermocouple type

            voltage_mode (VoltageMode): set input voltage range

            cj_high_mask (CJHighMask): mask CJHIGH fault from asserting through the FAULT pin

            cj_low_mask (CJLowMask): mask CJLOW fault from asserting through the FAULT pin

            tc_high_mask (TCHighMask): mask TCHIGH fault from asserting through the FAULT pin

            tc_low_mask (TCLowMask): mask TCLOW fault from asserting through the FAULT pin

            ovuv_mask (OvuvMask): mask OVUV fault from asserting through the FAULT pin

            open_mask (OpenMask): mask OPEN fault from asserting through the FAULT pin

            cj_high_threshold (int): set cold junction temperature upper threshold.
                If cold junction temperature rises above this limit, the FAULT output will assert

            cj_low_threshold (int): set cold junction temperature lower threshold.
                If cold junction temperature falls below this limit, the FAULT output will assert

            lt_high_threshold (int): set thermocouple hot junction temperature upper threshold.
                If thermocouple hot junction temperature rises above this limit,
                the FAULT output will assert

                lt_high_threshold_decimals (DecBits4): set thermocouple hot junction temperature
                                                        upper threshold decimal value.

            lt_low_threshold (int): set thermocouple hot junction temperature lower threshold.
                If thermocouple hot junction temperature falls below this limit,
                the FAULT output will assert

                lt_low_threshold_decimals (DecBits4): set thermocouple hot junction temperature
                                                    lower threshold decimal value.

            cj_offset (int): set cold junction temperature offset.

                cj_offset_decimals (DecBits4): set cold junction temperature offset decimal value.

                cj_temp (int): write values to cold-junction sensor.
                                Only use when cold-junction is disabled.

                cj_temp_decimals (DecBits6): set decimal value for cj_temp
        """
        # pylint: disable=unused-argument

        # filter out self from args
        args_dict = filter_dict(locals(), "self", None)
        _logger.debug(f"set_config: args dict:\n {args_dict}")

        # extract non-temperature setting opcodes from Enums
        ops_list = [
            entry.value
            for entry in args_dict.values()
            if issubclass(entry.__class__, Enum) and isinstance(entry.value, OpCode)
        ]

        self.__process_temperature_settings(
            cj_high_threshold,
            cj_low_threshold,
            lt_high_threshold,
            lt_high_threshold_decimals,
            lt_low_threshold,
            lt_low_threshold_decimals,
            cj_offset,
            cj_offset_decimals,
            cj_temp,
            cj_temp_decimals,
            tc_type,
            ops_list,
        )

        # read value of every write register into dict, starting from CR0_W.
        # Tuples are (write register addx : register_value) pairs.
        reg_values = self.__read_registers_to_map()
        _logger.debug(f"set_config: register values before updates:\n{reg_values}")

        # updated register values
        apply_opcodes(reg_values, ops_list)
        _logger.debug(f"set_config: register values after updates:\n\n{reg_values}")

        # only update registers whose values have been changed
        self.__update_registers_from_dict(reg_values)

        # Update configuration state
        self.get_state()

    def get_state(self):
        """
        Read config registers and update state object
        Args:
            N/A
        Retuern:
            N/A
        """
        cr_regs = self.__read_registers(TCAddresses.CR0_R.value, 2)
        self.tc_state.tc_update_state(cr_regs[1:])
