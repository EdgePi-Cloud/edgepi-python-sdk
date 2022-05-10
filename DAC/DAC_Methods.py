from DAC.DAC_Constants import EDGEPI_DAC_CHANNEL as CH
from DAC.DAC_Constants import EDGEPI_DAC_COM as COMMAND
from DAC.DAC_Constants import EDGEPI_DAC_CALIBRATION_CONSTANTS as CALIB_CONSTS

import logging
_logger=logging.getLogger(__name__)


class DAC_Methods():
    def __init__(self):
        _logger.info(f'Initializing DAC Methods')
        self.__amplifier_gain = [2.5] * 8
        self.__amplifier_offset = [0] * 8
        self.__dac_gain = 0
        self.__dac_offset = 0
        

    def generate_write_and_update_command(self, ch, data):
        if self.check_range(ch, 0, len(CH)) and self.check_range(data, 0, 65535):
            return self.combine_command(COMMAND.COM_WRITE_UPDATE.value, CH(ch).value, data)
        # Todo: or throw error
        return None
        
    #ToDo: change the formula according to calibration if needed
    def voltage_to_code(self, ch, expected):
        code = (((expected + self.__amplifier_offset[ch])  \
                / self.__amplifier_gain[ch])              \
                + self.__dac_offset)                      \
                / ((CALIB_CONSTS.VOLTAGE_REF.value / CALIB_CONSTS.RANGE.value) + self.__dac_gain) 
        return int(code)

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
        return target <= max and target >= min
