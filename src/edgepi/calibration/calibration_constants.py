'''Calibration constants and dataclasses'''

from dataclasses import dataclass
from enum import Enum

class NumOfCh(Enum):
    '''
    Number of channels for each module
    '''
    DAC = 0x8
    ADC = 0x8
    RTD = 0x1
    TC = 0x1

@dataclass
class CalibParam:
    '''
    Calibration parameters Gains and offsets
    '''
    gain: float = None
    offset: float = None

@dataclass
class ReferenceV:
    '''
    Reference voltage of each module
    '''
    dac: float = None
    adc: float = None
    adc_gnd: float = None
