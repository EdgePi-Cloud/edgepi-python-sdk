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
class PWMCh(Enum):
    """PWM Channel Enum"""
    PWM_1 = PWMChSysfs(chip=0, channel=0)
    PWM_2 = PWMChSysfs(chip=0, channel=1)

@unique
class Polarity(Enum):
    """PWM polarity Enum"""
    NORMAL = "Normal"
    INVERSED = "Inversed"
