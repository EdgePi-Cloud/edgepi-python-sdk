'''
Module for importing calibration paratmeter
from the external eeprom
'''

# import logging
from edgepi.peripherals.i2c import I2CDevice as i2c
from edgepi.calibration.eeprom_map import (
    # DACParam,
    # ADCParam,
    ModuleNames
)
# from edgepi.calibration.access_eeprom import (
#     selective_read,
#     sequential_read,
#     byte_write_register,
#     page_write_register
# )

class EdgePiCalibration(i2c):
    '''
    EdgePi Calibration Class handling the following functionality
    1. load calibration parameter
    2. store new calibration parameter
    3. calibration process for each module
        - Load measurement values
           - Edge Pi measurements
           - Equipment measurements
        - Calculation: use leat mean square method
    '''
    __dev_path = 'add/i2c/dev/path'
    # TODO: define i2c device id
    __eeprom_ID = 0xFF

    def __init__(self, module: ModuleNames):
        super().__init__(self.__dev_path)
        self.module = module.value()
#TODO: Import
#TODO: Export
#TODO:  Least Square method
