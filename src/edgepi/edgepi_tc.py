'''
Provides a class for interacting with the EdgePi Thermocouple via SPI. 
'''

import logging
from peripherals.spi import SpiDevice
from edgepi.tc import tc_constants as tc
from edgepi.tc.tc_commands import TCCommands

_logger = logging.getLogger(__name__)

class EdgePiTC(SpiDevice):
    ''' 
    A class used to represent the EdgePi Thermocouple as an SPI device.
    '''
    tc_coms = TCCommands()

    def __init__(self):
        super().__init__(bus_num=6, dev_ID=0)

    # TODO: use enum instead of int
    def set_averaging_mode(self, num_samples:tc.AVG_MODE):
        '''
        Sets number of measurements made per sampling event.   
        Parameters: and interger from the set {1, 2, 4, 8, 16}. Default = 1. 
        '''
        pass

    def single_sample(self, file_path:str=None):
        '''
        Conduct a single sampling event. Returns measured temperature in degrees Celsius.
        Parameters: a string representing a file path to log results to (optional).
        '''
        pass

    def auto_sample(self, file_path:str=None):
        '''
        Conduct sampling events continuously. Returns measured temperature in degrees Celsius.
        Parameters: a string representing a file path to log results to (optional).
        '''
        pass

    def set_type(self, tc_type:tc.TC_TYPE):
        '''
        Set thermocouple type. 
        Parameters: a string from the set {B,E,J,K,N,R,S,T}.
        '''
        pass

    def set_config(
        self,
        conversion_mode: tc.CONV_MODE = None,  
        oc_fault_mode: tc.FAULT_MODE = None, 
        cold_junction_mode: tc.CJ_MODE = None, 
        fault_mode: tc.FAULT_MODE = None,
        noise_filter_mode: tc.NOISE_FILTER_MODE = None,
        average_mode: tc.AVG_MODE = None,
        tc_type: tc.TC_TYPE = None,
        voltage_mode: tc.VOLT_MODE = None,
        fault_mask: tc.FAULT_MASKS = None,
        cj_high_threshold: int = None,
        cj_low_threshold: int = None,
        lt_high_threshold: int = None,
        lt_high_threshold_decimals: tc.DEC_BITS = None,
        lt_low_threshold: int = None,
        lt_low_threshold_decimals: tc.DEC_BITS = None,
        cj_offset: int = None,
        cj_offset_decimals: tc.DEC_BITS = None,
        ):
        '''
        A collective thermocouple settings update method.

        Args:
            all (Enum): enum representing a valid hex opcode. See tc_constants.py for valid opcodes.
        '''
        args_list = [conversion_mode, oc_fault_mode, cold_junction_mode, fault_mode, noise_filter_mode,
                    average_mode, tc_type, voltage_mode, fault_mask, cj_high_threshold, cj_low_threshold,
                    lt_high_threshold, lt_high_threshold_decimals, lt_low_threshold, lt_low_threshold_decimals,
                    cj_offset, cj_offset_decimals]
        _logger.info(f'set_config args list: {args_list}')

        # map each command to its register and build dictionary of (register_address : [command_list]) tuples. 
        # this also validates the command is a valid opcode.
        add_reg_map = {}
        for setting in args_list:
            if setting is not None:
                reg = self.tc_coms.find_register(setting)
                # invalid opcodes return None
                if reg is None:
                    continue
                if reg in add_reg_map:
                    add_reg_map[reg].append(setting)
                else:
                    add_reg_map[reg] = [setting]
        _logger.info(f'set_config add_reg_map: {add_reg_map}')
        
        # for each register, combine all settings updates into one command
        for addx, op_array in add_reg_map.items():   
            # read register value 
            reg_value = self.tc_coms.read_register(addx)
            # generate update code for register 
            update_code = self.tc_coms.get_update_code(addx, reg_value, op_array)
            # write to register, spi_transfer data
