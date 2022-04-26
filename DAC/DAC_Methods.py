from DAC_Constants import EDGEPI_DAC_ADDRESS as ADDRESS
from DAC_Constants import EDGEPI_DAC_COM as COMMAND

import logging
logging.basicConfig(level=logging.INFO)
_logger=logging.getLogger(__name__)


class DAC_Methods():
    def __init__(self):
        _logger.info(f'Initializing DAC Methods')

    def combine_command(self, op_code, ch, value):
        temp = (op_code<<20) + (ch<<16) + value
        list = [temp>>16, (temp>>8)&0xFF, temp&0xFF]
        _logger.debug(f'Combined Command is: {list}')
        return list