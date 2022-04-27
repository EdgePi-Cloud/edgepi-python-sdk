from operator import truediv
from pickle import EMPTY_LIST
from DAC_Constants import EDGEPI_DAC_ADDRESS as ADDRESS
from DAC_Constants import EDGEPI_DAC_COM as COMMAND
from DAC_Constants import EDGEPI_DAC_CALIBRATION_CONSTANTS as CALIB_CONSTS
from DAC_Constants import EDGEPI_DAC_AMP_CONSTANTS as AMP_CONSTS

import logging
logging.basicConfig(level=logging.INFO)
_logger=logging.getLogger(__name__)


class DAC_Methods():
    def __init__(self):
        _logger.info(f'Initializing DAC Methods')

    def write_and_update(self, ch, data):
        if self.check_range(ch, 0, len(ADDRESS)) and self.check_range(data, 0, 65535):
            return self.combine_command(COMMAND.COM_WRITE_UPDATE.value, ADDRESS(ch).value, data)
        # Todo: or throw error
        return None
        
#ToDo: change the formula according to calibration if needed
    def voltage_to_code(self, ch, expected):
        code = (expected + AMP_CONSTS(ch+8).value) / AMP_CONSTS(ch).value \
         + CALIB_CONSTS.DAC_OFFSET.value  \
         / ((CALIB_CONSTS.RANGE.value / CALIB_CONSTS.VOLTAGE_REF.value) + CALIB_CONSTS.DAC_GAIN) 
        return code

    @staticmethod
    def combine_command(op_code, ch, value):
        # Todo: why it requires class.staticmethod()? instead of just self.staticmethod?
        if DAC_Methods.check_for_int([op_code, ch, value]):
            temp = (op_code<<20) + (ch<<16) + value
            list = [temp>>16, (temp>>8)&0xFF, temp&0xFF]
            _logger.debug(f'Combined Command is: {list}')
        else:
            # Todo: throw an exception instead?
            list = None
        return list

    @staticmethod
    def check_for_int(target_list):
        if not target_list:
            return False
        for i in range(len(target_list)):
            if not isinstance(target_list[i], int):
                _logger.debug(f'Non-Integer number detected: {i}')
                return False
        return True
    @staticmethod
    def check_range(target, min, max):
        if target <= max and target >= min:
            return True
        else:
            return False