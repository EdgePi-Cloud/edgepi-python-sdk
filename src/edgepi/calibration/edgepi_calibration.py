'''
Module for importing calibration paratmeter
from the external eeprom
'''

import logging
from edgepi.peripherals.i2c import I2CDevice as i2c
from edgepi.calibration.eeprom_map import (
    DACParam,
    ADCParam,
    ModuleNames
)
from edgepi.calibration.access_eeprom import (
    selective_read,
    sequential_read,
    byte_write_register,
    page_write_register
)

class EdgePiCalibration(i2c):
    def __init__(self, module: ModuleNames):
        self.module = ModuleNames.module.value()
        