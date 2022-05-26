from edgepi.adc.adc_constants import EDGEPI_ADC_CHANNEL as CH
from edgepi.adc.adc_constants import EDGEPI_ADC_OP as opcode
import logging
_logger=logging.getLogger(__name__)

class ADCCommands():
    def __init__(self):
        _logger.info(f'Initializing ADC Methods')

    def read_register_command(self, address, num):
        ADCCommands.check_for_int([address, num])
        command = [opcode.OP_RREG.value + address, num-1]
        _logger.debug(f'Command to send is {command + [255]*num}')
        return command + [255]*num

    @staticmethod
    def check_for_int(target_list):
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True
        else:
            raise ValueError(f'Non integer value passed{target_list}')