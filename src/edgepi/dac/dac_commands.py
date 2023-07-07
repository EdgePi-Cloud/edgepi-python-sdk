""" Command class and methods for DAC devices """

import logging
from bitstring import Bits, pack
from edgepi.dac.dac_constants import (
    NUM_PINS,
    READ_WRITE_SIZE,
    DACChannel as CH,
    EdgePiDacCom as COMMAND,
    EdgePiDacCalibrationConstants as CALIB_CONSTS,
)


_logger = logging.getLogger(__name__)


class DACCommands:
    """Class for representing DAC device commands"""

    def __init__(self, dict_calib_param):
        _logger.info("Initializing DAC Methods")
        self.dict_calib_param = dict_calib_param

    def generate_write_and_update_command(self, ch: int, data: int) -> list:
        """Construct a write and update command"""
        self.check_range(ch, 0, NUM_PINS-1)
        self.check_range(data, 0, CALIB_CONSTS.RANGE.value)
        return self.combine_command(COMMAND.COM_WRITE_UPDATE.value, CH(ch).value, data)

    def __voltage_to_float_code(self, ch: int, expected: float, dac_gain: int = 1):
        """
        Convert a voltage to full precision binary code value
        code = ((expected_v - offset)/gain) * (Code_range/V_range))/DAC_GAIN
        """
        float_code =(((expected-self.dict_calib_param[ch].offset)/self.dict_calib_param[ch].gain)*\
                    (CALIB_CONSTS.RANGE.value/CALIB_CONSTS.V_RANGE.value))/dac_gain
        _logger.debug(f"Full code generated {float_code}")
        return float_code

    def voltage_to_code(self, ch: int, expected: float, dac_gain: int = 1) -> int:
        """
        Convert a voltage to binary code value

        Args:
            ch (int): the DAC channel to write voltage to (0-indexed)

            expected (float): the voltage input by the user

            dac_gain (int): dac gain state, x1 or x2, when x2 voltage range extened to 10V from 5V

        Returns:
            int: 16 bit binary code value for writing voltage value to DAC
        """
        # DAC channels are 0 indexed
        self.check_range(ch, 0, NUM_PINS-1)
        float_code = self.__voltage_to_float_code(ch, expected, dac_gain)
        _logger.debug(f"Int code generated {int(float_code)}")
        # DAC only accepts int values, round to nearest int
        return round(float_code)

    @staticmethod
    def extract_read_data(read_code: list) -> int:
        """
        Extracts bits corresponding to voltage code from a list containing
        the byte values of a DAC register read.

        Args:
            read_code (list): a list of unsigned int byte values from DAC read

        Returns:
            int: the unsigned int value of the 16 bits corresponding to voltage code

        Raises:
            ValueError: if read_code does not contain exactly 3 byte values
        """
        if len(read_code) != READ_WRITE_SIZE:
            raise ValueError("code must contain exactly 3 byte values")

        bits = pack("uint:8, uint:8, uint:8", read_code[0], read_code[1], read_code[2])

        # B23 to DB20 contain undefined data, and the last 16 bits contain the
        # DB19 to DB4 DAC register contents. B23 (MSB) is index 0 here.
        return bits[-16:].uint

    def __code_to_float_voltage(self, ch: int, code: int, dac_gain: int = 1) -> float:
        """
        Convert a voltage to float voltage
        ((Code*DAC_GAIN)*(V_Range/CodeRange))*Calib_Gain + Calib_Offset
        """
        voltage = ((code*dac_gain)*(CALIB_CONSTS.V_RANGE.value/CALIB_CONSTS.RANGE.value))*\
                  self.dict_calib_param[ch].gain + self.dict_calib_param[ch].offset
        return voltage

    def code_to_voltage(self, ch: int, code: int, dac_gain: int = 1) -> float:
        """
        Convert a 16 bit binary code value to voltage

        Args:
            ch (int): the DAC channel the code was obtained from (0-indexed)

            code (int): 16 bit unsigned int value of a DAC register read

            dac_gain (int): dac gain state, x1 or x2, when x2 voltage range extened to 10V from 5V

        Returns:
            float: voltage corresponding to 16 bit binary code
        """
        voltage = self.__code_to_float_voltage(ch, code, dac_gain)
        _logger.debug(f"code_to_voltage: code {hex(code)} = {voltage} V")
        return voltage

    @staticmethod
    # pylint: disable=inconsistent-return-statements
    def combine_command(op_code: int, ch: int, value: int) -> list:
        """
        Combine op_code, channel and value into a message frame to send out to DAC device

        Args:
            op_code (COMMAND.value): AD5675 DAC command

            ch (CH.value): AD5657 DAC channel address

            value: 16 bit data

        Returns:
            list: a list of bytes that form a DAC input shift register message frame,
                i.e. of the form [op_code_byte, ch_byte, value_byte]
        """
        DACCommands.check_for_int([op_code, ch, value])
        temp = (op_code << 20) + (ch << 16) + value
        combined_cmnd = [temp >> 16, (temp >> 8) & 0xFF, temp & 0xFF]
        _logger.debug(f"Combined Command is: {combined_cmnd}")
        return combined_cmnd

    @staticmethod
    def check_for_int(target_list: list) -> bool:
        """Checks if a list contains only integer values"""
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True

        raise ValueError(f"Non integer value passed{target_list}")

    @staticmethod
    def check_range(target, range_min, range_max) -> bool:
        """Validates target is in range between a min and max value"""
        if range_min <= target <= range_max:
            return True

        raise ValueError(f"Target {target} is out of range ")

    @staticmethod
    def generate_power_code(dac_state: list) -> int:
        """
        Converts a list containing the EdgePi DAC's power state for each channel
        to a binary code value.

        Args:
            dac_state (list): a list whose entries represent the power mode of each DAC
                channel, ordered sequentially from DAC 7 (index 0) to DAC 0 (index 7).

        Returns:
            int: a 16 bit binary code value for updating DAC channel power mode
        """
        data = Bits()
        for value in dac_state:
            data += Bits(uint=value, length=2)
        return data.uint
