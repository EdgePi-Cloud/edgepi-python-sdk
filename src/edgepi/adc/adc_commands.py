""" Utility module for ADC commands """

import logging
from typing import Optional

from edgepi.adc.adc_constants import (
    ADCComs,
    ADCChannel as CH,
    ADCNum,
    ADCReg,
    ADCReadInfo,
    ADC_VOLTAGE_READ_LEN,

)
from edgepi.adc.adc_multiplexers import generate_mux_opcode

_logger = logging.getLogger(__name__)


# pylint: disable=logging-too-many-args
class ADCCommands:
    """Class representing ADC commands"""

    def __init__(self):
        _logger.info("Initializing ADC Methods")

    def read_register_command(self, address: int, num: int):
        """Trigger ADC register read"""
        self.check_for_int([address, num])
        command = [ADCComs.COM_RREG.value + address, num - 1]
        return command + [255] * num

    def write_register_command(self, address, values):
        """Trigger ADC register write"""
        self.check_for_int([address])
        all(self.check_range(value, 0, 255) for value in values)
        self.check_for_int(values)
        command = [ADCComs.COM_WREG.value + address, len(values) - 1]
        return command + values

    @staticmethod
    def unsafe_write_register_command(address: int, values: list[int]):
        """
        Trigger ADC register write - unsafe removes all arguments validation. 

        Please ensure that values contains only bytes, and that address is a 
        valid address.
        """
        command = [ADCComs.COM_WREG.value + address, len(values) - 1]
        return command + values

    @staticmethod
    def start_adc_command(adc_num: ADCReadInfo):
        """Command to start ADC conversions"""
        _logger.debug("Command to send is %s", ([adc_num.start_cmd]))
        return [adc_num.start_cmd]

    @staticmethod
    def read_adc_command(adc_num: ADCReadInfo, num_bytes: int):
        """
        Returns the command to read from the ADC, after waiting the required time for
        conversions to take effect
        """
        # Since this is full duplex SPI, we have to write something every time we expect
        # to read something as well, so we add the 6 0xff bytes so that periphery will read
        # the 6 results bytes we care about.
        return [adc_num.read_cmd] + [255] * num_bytes

    @staticmethod
    def stop_adc_command(adc_num: ADCReadInfo):
        """Command to stop ADC"""
        _logger.debug("Command to send is %s", ([adc_num.stop_cmd]))
        return [adc_num.stop_cmd]

    @staticmethod
    def reset_adc_command():
        """Command to reset ADC"""
        _logger.debug("Command to send is %s", ([ADCComs.COM_RESET.value]))
        return [ADCComs.COM_RESET.value]

    @staticmethod
    def read_command_tuple(
        mode2_register_value: Optional[int],
        conversion_delay: float,
        mux_p: CH,
        mux_n: CH,
    ) -> tuple[list, float, list]:
        """
        Returns a tuple containing two spi commands, separated by a delay. For use
        with spi_apply_adc_commands
        """
        inpmux_register_value = generate_mux_opcode(ADCReg.REG_INPMUX, mux_p, mux_n).op_code
        if mode2_register_value is not None:
            # update only data rate & input multiplexing (luckily they are right beside eachother)
            start_addr = ADCReg.REG_MODE2.value
            register_list = [mode2_register_value, inpmux_register_value]
        else:
            # Only write the register value 0x06 (INPMUX), which stores info
            # about how the multiplexer should read from the ADC channels (input pins).
            start_addr = ADCReg.REG_INPMUX.value
            register_list = [inpmux_register_value]

        write_reg_cmd = ADCCommands.unsafe_write_register_command(
            start_addr, register_list
        )

        # write config registers, start the adc's conversions, wait, then read registers
        return (
            write_reg_cmd + ADCCommands.start_adc_command(ADCNum.ADC_1.value),
            conversion_delay,
            ADCCommands.read_adc_command(ADCNum.ADC_1.value, ADC_VOLTAGE_READ_LEN),
        )

    @staticmethod
    def check_for_int(target_list):
        """Checks if a list contains only integer values"""
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True
        raise ValueError(f"Non integer value passed {target_list}")

    @staticmethod
    def check_range(target, lower, upper):
        """Validates target is in range between a min and max value"""
        if lower <= target <= upper:
            return True
        raise ValueError(f"Target out of range {target}")
