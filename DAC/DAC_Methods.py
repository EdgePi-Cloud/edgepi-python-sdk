from operator import truediv
from pickle import EMPTY_LIST
from DAC_Constants import EDGEPI_DAC_ADDRESS as ADDRESS
from DAC_Constants import EDGEPI_DAC_COM as COMMAND

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

    #@staticmethod
    def combine_command(self, op_code, ch, value):
        if self.check_for_int([op_code, ch, value]):
            temp = (op_code<<20) + (ch<<16) + value
            list = [temp>>16, (temp>>8)&0xFF, temp&0xFF]
            _logger.debug(f'Combined Command is: {list}')
        else:
            # Todo: throw an exception instead?
            list = None
        return list

    #@staticmethod
    def check_for_int(self, target_list):
        if not target_list:
            return False
        for i in range(len(target_list)):
            if not isinstance(target_list[i], int):
                _logger.debug(f'Non-Integer number detected: {i}')
                return False
        return True
    #@staticmethod
    def check_range(self, target, min, max):
        if target <= max and target >= min:
            return True
        else:
            return False