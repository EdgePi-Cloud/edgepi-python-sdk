""" Command class and methods for DAC devices """

import logging
from typing import Union
from bitstring import Bits, pack
from edgepi.dac.dac_constants import (
    READ_WRITE_SIZE,
    DAC_PRECISION,
    EdgePiDacChannel as CH,
    EdgePiDacCom as COMMAND,
    EdgePiDacCalibrationConstants as CALIB_CONSTS,
)


_logger = logging.getLogger(__name__)


class DACCommands:
    """Class for representing DAC device commands"""

    def __init__(self, dach_w_calib_const, dacs_w_calib_const):
        _logger.info("Initializing DAC Methods")
        self.dach_w_calib_const = dach_w_calib_const
        self.dacs_w_calib_consts_list = dacs_w_calib_const

    def generate_write_and_update_command(self, ch, data):
        """Construct a write and update command"""
        if self.check_range(ch, 0, len(CH)) and self.check_range(data, 0, CALIB_CONSTS.RANGE.value):
            return self.combine_command(COMMAND.COM_WRITE_UPDATE.value, CH(ch).value, data)

    @staticmethod
    def validate_voltage_precision(voltage: float) -> bool:
        """
        Verifies the voltage value meets DAC precision constraints. DAC is currently
        accurate to the mV.

        Args:
            voltage (float): voltage value

        Returns:
            bool: True if voltage value has at most DAC_PRECISION decimal places
        """
        return len(str(float(voltage)).split(".")[1]) <= DAC_PRECISION

    # TODO: change the formula according to calibration if needed
    def voltage_to_code(self, ch: int, expected: float):
        """
        Convert a voltage to binary code value

        Args:
            ch (int): the DAC channel to write voltage to (0-indexed)

            expected (float): the voltage input by the user

        Returns:
            16 bit binary code value for writing voltage value to DAC
        """
        # DAC channels are 0 indexed
        self.check_range(ch, 0, len(CH) - 1)
        code = (
            (
                (expected + self.dacs_w_calib_consts_list[ch].offset)
                / self.dacs_w_calib_consts_list[ch].gain
            )
            + self.dach_w_calib_const.offset
        ) / (
            (CALIB_CONSTS.VOLTAGE_REF.value / CALIB_CONSTS.RANGE.value)
            + self.dach_w_calib_const.gain
        )
        _logger.debug(f"Code generated {int(code)}")
        return int(code)

    @staticmethod
    def extract_read_data(read_code: list):
        """
        Extracts bits corresponding to voltage code from a list containing
        the byte values of a DAC register read.

        Args:
            read_code (list): a list of unsigned int byte values from DAC read

        Returns:
            the unsigned int value of the 16 bits corresponding to voltage code

        Raises:
            ValueError: if read_code does not contain exactly 3 byte values
        """
        if len(read_code) != READ_WRITE_SIZE:
            raise ValueError("code must contain exactly 3 byte values")

        bits = pack("uint:8, uint:8, uint:8", read_code[0], read_code[1], read_code[2])

        # B23 to DB20 contain undefined data, and the last 16 bits contain the
        # DB19 to DB4 DAC register contents. B23 (MSB) is index 0 here.
        return bits[-16:].uint

    def code_to_voltage(self, ch: int, code: int) -> float:
        """
        Convert a 16 bit binary code value to voltage

        Args:
            ch (int): the DAC channel the code was obtained from (0-indexed)

            code (int): 16 bit unsigned int value of a DAC register read

        Returns:
            voltage corresponding to 16 bit binary code
        """
        # DAC gain/offset errors
        dac_gain_err = (
            CALIB_CONSTS.VOLTAGE_REF.value / CALIB_CONSTS.RANGE.value
        ) + self.dach_w_calib_const.gain
        dac_offset_err = self.dach_w_calib_const.offset
        # amplifier gain/offset for this channel
        amp_gain = self.dacs_w_calib_consts_list[ch].gain
        amp_offset = self.dacs_w_calib_consts_list[ch].offset
        voltage = (((code * dac_gain_err) - dac_offset_err) * amp_gain) - amp_offset
        _logger.debug(f"code_to_voltage: code {hex(code)} = {voltage} V")
        return round(voltage, DAC_PRECISION)

    @staticmethod
    # pylint: disable=inconsistent-return-statements
    def combine_command(op_code, ch, value) -> Union[float, Exception]:
        """
        Combine op_code, channel and value into a message frame to send out to DAC device

        Args:
            op_code (COMMAND.value): AD5675 DAC command

            ch (CH.value): AD5657 DAC channel address

            value: 16 bit data

        Returns:
            a list of bytes that form a DAC input shift register message frame, i.e.
            of the form [op_code_byte, ch_byte, value_byte]
        """
        try:
            DACCommands.check_for_int([op_code, ch, value])
            temp = (op_code << 20) + (ch << 16) + value
            combined_cmnd = [temp >> 16, (temp >> 8) & 0xFF, temp & 0xFF]
            _logger.debug(f"Combined Command is: {combined_cmnd}")
            return combined_cmnd
        # pylint: disable=broad-except
        except Exception as err:
            _logger.error(f"Exception raised {err}")

    @staticmethod
    def check_for_int(target_list):
        """Checks if a list contains only integer values"""
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True

        raise ValueError(f"Non integer value passed{target_list}")

    @staticmethod
    def check_range(target, range_min, range_max):
        """Validates target is in range between a min and max value"""
        if range_min <= target <= range_max:
            return True

        raise ValueError(f"Target {target} is out of range ")

    @staticmethod
    def generate_power_code(dac_state: list):
        """
        Converts a list containing the EdgePi DAC's power state for each channel
        to a binary code value.

        Args:
            dac_state (list): a list whose entries represent the power mode of each DAC
                channel, ordered sequentially from DAC 7 (index 0) to DAC 0 (index 7).

        Returns:
            a 16 bit binary code value for updating DAC channel power mode
        """
        data = Bits()
        for value in dac_state:
            data += Bits(uint=value, length=2)
        return data.uint
