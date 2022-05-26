from tabnanny import check
from edgepi.adc.adc_constants import EDGEPI_ADC_CHANNEL as CH
from edgepi.adc.adc_constants import EDGEPI_ADC_OP as opcode
import logging
_logger=logging.getLogger(__name__)

class ADCCommands():
    def __init__(self):
        _logger.info(f'Initializing ADC Methods')

    def read_register_command(self, address, num):
        self.check_for_int([address, num])
        command = [opcode.OP_RREG.value + address, num-1]
        _logger.debug(f'Command to send is {command + [255]*num}')
        return command + [255]*num

    def write_register_command(self, address, values):
        self.check_for_int([address])
        all(self.check_range(value, 0, 255) for value in values)
        self.check_for_int(values)
        command = [opcode.OP_WREG.value + address, len(values)-1]
        _logger.debug(f'Command to send is {command + values}')
        return command + values
    
    def start_adc1(self):
        _logger.debug(f'Command to send is {[opcode.OP_START1.value]}')
        return [opcode.OP_START1.value]

    def stop_adc1(self):
        _logger.debug(f'Command to send is {[opcode.OP_STOP1.value]}')
        return [opcode.OP_STOP1.value]
    
    def reset_adc(self):
        _logger.debug(f'Command to send is {[opcode.OP_RESET.value]}')
        return [opcode.OP_RESET.value]

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
