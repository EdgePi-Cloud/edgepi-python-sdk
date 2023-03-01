""" Utility module for ADC commands """


import logging

from edgepi.adc.adc_constants import ADCComs, ADCNum


_logger = logging.getLogger(__name__)


# pylint: disable=logging-too-many-args
class ADCCommands:
    """Class representing ADC commands"""

    def __init__(self):
        _logger.info("Initializing ADC Methods")

    def read_register_command(self, address: int, num: int):
        """Trigger ADC register read"""
        self.check_for_int([address, num])
        command = [ADCComs.COM_RREG.value + address, num - 1]
        return command + [255] * num

    def write_register_command(self, address, values):
        """Trigger ADC register write"""
        self.check_for_int([address])
        all(self.check_range(value, 0, 255) for value in values)
        self.check_for_int(values)
        command = [ADCComs.COM_WREG.value + address, len(values) - 1]
        return command + values

    def start_adc(self, adc_num: ADCNum):
        """Command to start ADC"""
        _logger.debug("Command to send is %s", ([adc_num.start_cmd]))
        return [adc_num.start_cmd]


    def stop_adc(self, adc_num: ADCNum):
        """Command to stop ADC"""
        _logger.debug("Command to send is %s", ([adc_num.stop_cmd]))
        return [adc_num.stop_cmd]


    def reset_adc(self):
        """Command to reset ADC"""
        _logger.debug("Command to send is %s", ([ADCComs.COM_RESET.value]))
        return [ADCComs.COM_RESET.value]

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
