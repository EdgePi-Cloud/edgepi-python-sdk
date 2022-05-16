from edgepi.dac.dac_constants import EDGEPI_DAC_CHANNEL as CH
from edgepi.dac.dac_constants import EDGEPI_DAC_COM as COMMAND
from edgepi.dac.dac_constants import EDGEPI_DAC_CALIBRATION_CONSTANTS as CALIB_CONSTS
from edgepi.dac.dac_calibration import DACHwCalib_const, DACSwCalib_const

from typing import Union

import logging
_logger=logging.getLogger(__name__)

class DACCommands():
    def __init__(self):
        _logger.info(f'Initializing DAC Methods')
        self.DACHwCalib_const = DACHwCalib_const
        self.DACSwCalib_consts_list = [DACSwCalib_const]*8        

    def generate_write_and_update_command(self, ch, data):
        if self.check_range(ch, 0, len(CH)) and self.check_range(data, 0, CALIB_CONSTS.RANGE.value):
            return self.combine_command(COMMAND.COM_WRITE_UPDATE.value, CH(ch).value, data)
        return None
        
    #TODO: change the formula according to calibration if needed
    def voltage_to_code(self, ch, expected):
        code = (((expected + self.DACSwCalib_consts_list[ch].offset)  \
                / self.DACSwCalib_consts_list[ch].gain)              \
                + self.DACHwCalib_const.offset)                      \
                / ((CALIB_CONSTS.VOLTAGE_REF.value / CALIB_CONSTS.RANGE.value) + self.DACHwCalib_const.gain)
        _logger.debug(f'Code generated {int(code)}') 
        return int(code)

    @staticmethod
    def combine_command(op_code, ch, value) -> Union[float, Exception]:
        try:
            DACCommands.check_for_int([op_code, ch, value])
            temp = (op_code<<20) + (ch<<16) + value
            list = [temp>>16, (temp>>8)&0xFF, temp&0xFF]
            _logger.debug(f'Combined Command is: {list}')
            return list
        except Exception as e:
            _logger.error(f'Exception raised {e}')
            

    @staticmethod
    def check_for_int(target_list):
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True
        else:
            raise ValueError(f'Non integer value passed{target_list}')

    @staticmethod
    def check_range(target, min, max):
        if target <= max and target >= min:
            return True
        else:
            raise ValueError(f'Target out of range {target}')
