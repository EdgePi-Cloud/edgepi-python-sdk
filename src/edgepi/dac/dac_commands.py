""" Command class and methods for DAC devices """

import logging
from typing import Union
from edgepi.dac.dac_constants import EdgePiDacChannel as CH
from edgepi.dac.dac_constants import EdgePiDacCom as COMMAND
from edgepi.dac.dac_constants import EdgePiDacCalibrationConstants as CALIB_CONSTS


_logger = logging.getLogger(__name__)


class DACCommands:
    """Class for representing DAC device commands"""

    def __init__(self, dach_w_calib_const, dacs_w_calib_const):
        _logger.info("Initializing DAC Methods")
        self.dach_w_calib_const = dach_w_calib_const
        self.dacs_w_calib_consts_list = dacs_w_calib_const

    def generate_write_and_update_command(self, ch, data):
        """Construct a write and update command"""
        if self.check_range(ch, 0, len(CH)) and self.check_range(
            data, 0, CALIB_CONSTS.RANGE.value
        ):
            return self.combine_command(
                COMMAND.COM_WRITE_UPDATE.value, CH(ch).value, data
            )
        return None

    # TODO: change the formula according to calibration if needed
    def voltage_to_code(self, ch, expected):
        """Convert a voltage to binary code value"""
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
    # pylint: disable=inconsistent-return-statements
    def combine_command(op_code, ch, value) -> Union[float, Exception]:
        """combine op_code, channel and value into a message frame to send out to DAC device"""
        try:
            DACCommands.check_for_int([op_code, ch, value])
            temp = (op_code << 20) + (ch << 16) + value
            combined_cmnd = [temp >> 16, (temp >> 8) & 0xFF, temp & 0xFF]
            _logger.debug(f"Combined Command is: {combined_cmnd}")
            return combined_cmnd
        # pylint: disable=broad-except
        except Exception as e:
            _logger.error(f"Exception raised {e}")

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

        raise ValueError(f"Target out of range {target}")
