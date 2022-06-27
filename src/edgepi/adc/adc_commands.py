import logging
from edgepi.adc.adc_constants import EDGEPI_ADC_OP as opcode
_logger=logging.getLogger(__name__)

class ADCCommands():
    def __init__(self):
        _logger.info('Initializing ADC Methods')

    def read_register_command(self, address, num):
        self.check_for_int([address, num])
        command = [opcode.OP_RREG.value + address, num-1]
        _logger.debug('Command to send is %s', (command + [255]*num))
        return command + [255]*num

    def write_register_command(self, address, values):
        self.check_for_int([address])
        all(self.check_range(value, 0, 255) for value in values)
        self.check_for_int(values)
        command = [opcode.OP_WREG.value + address, len(values)-1]
        _logger.debug('Command to send is %s', (command + values))
        return command + values

    def start_adc1(self):
        _logger.debug('Command to send is %s', ([opcode.OP_START1.value]))
        return [opcode.OP_START1.value]

    def stop_adc1(self):
        _logger.debug('Command to send is %s', ([opcode.OP_STOP1.value]))
        return [opcode.OP_STOP1.value]

    def reset_adc(self):
        _logger.debug('Command to send is %s', ([opcode.OP_RESET.value]))
        return [opcode.OP_RESET.value]

    @staticmethod
    def check_for_int(target_list):
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True
        raise ValueError('Non integer value passed %s', target_list)

    @staticmethod
    def check_range(target, lower, upper):
        if target >= lower and target <= upper:
            return True
        raise ValueError('Target out of range %s', target)
