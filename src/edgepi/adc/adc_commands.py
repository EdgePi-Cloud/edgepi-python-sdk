""" Utility module for ADC commands """

import logging
from edgepi.adc.adc_constants import EdgePiADCOp as opcode

_logger = logging.getLogger(__name__)

# pylint: disable=logging-too-many-args
class ADCCommands:
    """Class representing ADC commands"""

    def __init__(self):
        _logger.info("Initializing ADC Methods")

    def read_register_command(self, address, num):
        """Trigger ADC register read"""
        self.check_for_int([address, num])
        command = [opcode.OP_RREG.value + address, num - 1]
        _logger.debug("Command to send is %s", (command + [255] * num))
        return command + [255] * num

    def write_register_command(self, address, values):
        """Trigger ADC register write"""
        self.check_for_int([address])
        all(self.check_range(value, 0, 255) for value in values)
        self.check_for_int(values)
        command = [opcode.OP_WREG.value + address, len(values) - 1]
        _logger.debug("Command to send is %s", (command + values))
        return command + values

    def start_adc1(self):
        """Command to start ADC"""
        _logger.debug("Command to send is %s", ([opcode.OP_START1.value]))
        return [opcode.OP_START1.value]

    def stop_adc1(self):
        """Command to stop ADC"""
        _logger.debug("Command to send is %s", ([opcode.OP_STOP1.value]))
        return [opcode.OP_STOP1.value]

    def reset_adc(self):
        """Command to reset ADC"""
        _logger.debug("Command to send is %s", ([opcode.OP_RESET.value]))
        return [opcode.OP_RESET.value]

    @staticmethod
    def check_for_int(target_list):
        """Checks if a list contains only integer values"""
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True
        raise ValueError(f"Non integer value passed {target_list}")

    @staticmethod
    def check_range(target, lower, upper):
        """Validates target is in range between a min and max value"""
        if lower <= target <= upper:
            return True
        raise ValueError(f"Target out of range {target}")
