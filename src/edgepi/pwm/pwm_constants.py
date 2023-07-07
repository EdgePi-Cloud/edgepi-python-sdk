"""PWM Constants"""

from enum import Enum, unique
from dataclasses import dataclass

@dataclass(frozen=True)
class PWMChSysfs:
    """
    PWM System file numbers
    Attributes:
        chip (int): PWM chip number
        channel (int): PWM channel number
    """
    chip: int = None
    channel: int =None

@unique
class PWMPins(Enum):
    """GPIO Pin Names"""

    PWM1 = 'PWM1'
    PWM2 = 'PWM2'

@unique
class PWMCh(Enum):
    """PWM Channel Enum"""
    PWM_1 = PWMChSysfs(chip=0, channel=1)
    PWM_2 = PWMChSysfs(chip=0, channel=0)

@unique
class Polarity(Enum):
    """PWM polarity Enum"""
    NORMAL = 1
    INVERSED = -1

PWM_MAX_FREQ = 10000.0
PWM_MIN_FREQ = 1000.0
PWM_MAX_DUTY_CYCLE = 1.0
PWM_MIN_DUTY_CYCLE = 0.0
