""" Digital Output Constants """


from enum import Enum, unique

@unique
class DoutPins(Enum):
    """Digital Output Gpio Pin Names"""

    DOUT1 = 'DOUT1'
    DOUT2 = 'DOUT2'
    DOUT3 = 'DOUT3'
    DOUT4 = 'DOUT4'
    DOUT5 = 'DOUT5'
    DOUT6 = 'DOUT6'
    DOUT7 = 'DOUT7'
    DOUT8 = 'DOUT8'

@unique
class DoutTriState(Enum):
    """Digital Output Tri-state Enum"""

    HI_Z = -1
    LOW = 0
    HIGH = 1
