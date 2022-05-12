from DAC.DAC_Constants import EDGEPI_DAC_CHANNEL as CH
from DAC.DAC_Constants import EDGEPI_DAC_COM as COMMAND
from DAC.DAC_Constants import EDGEPI_DAC_CALIBRATION_CONSTANTS as CALIB_CONSTS
from DAC.DAC_Calibration import dac_hw_calib_const, dac_sw_calib_const

from typing import Union

import logging
_logger=logging.getLogger(__name__)

class DAC_Commands():
    def __init__(self):
        _logger.info(f'Initializing DAC Methods')
        self.dac_hw_calib_const = dac_hw_calib_const
        self.dac_sw_calib_consts_list = [dac_sw_calib_const]*8        

    def generate_write_and_update_command(self, ch, data):
        if self.check_range(ch, 0, len(CH)) and self.check_range(data, 0, CALIB_CONSTS.RANGE.value):
            return self.combine_command(COMMAND.COM_WRITE_UPDATE.value, CH(ch).value, data)
        # Todo: or throw error
        return None
        
    #ToDo: change the formula according to calibration if needed
    def voltage_to_code(self, ch, expected):
        code = (((expected + self.dac_sw_calib_consts_list[ch].offset)  \
                / self.dac_sw_calib_consts_list[ch].gain)              \
                + self.dac_hw_calib_const.offset)                      \
                / ((CALIB_CONSTS.VOLTAGE_REF.value / CALIB_CONSTS.RANGE.value) + self.dac_hw_calib_const.gain) 
        return int(code)

    @staticmethod
    def combine_command(op_code, ch, value) -> Union[float, Exception]:
        try:
            DAC_Commands.check_for_int([op_code, ch, value])
            temp = (op_code<<20) + (ch<<16) + value
            list = [temp>>16, (temp>>8)&0xFF, temp&0xFF]
            _logger.debug(f'Combined Command is: {list}')
            return list
        except Exception as e:
            return e

    @staticmethod
    def check_for_int(target_list):
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True
        else:
            raise ValueError('Non integer value passed')

    @staticmethod
    def check_range(target, min, max):
        if target <= max and target >= min:
            return True
        else:
            raise ValueError('Value out of range')
