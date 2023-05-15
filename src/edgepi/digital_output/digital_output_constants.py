""" Digital Output Constants """


from enum import Enum, unique

@unique
class DoutPins(Enum):
    """GPIO Pin Names"""

    DOUT1 = 'DOUT1'
    DOUT2 = 'DOUT2'
    DOUT3 = 'DOUT3'
    DOUT4 = 'DOUT4'
    DOUT5 = 'DOUT5'
    DOUT6 = 'DOUT6'
    DOUT7 = 'DOUT7'
    DOUT8 = 'DOUT8'

@unique
class AoutPins(Enum):
    """GPIO Pin Names"""

    AO_EN1 = 'AO_EN1'
    AO_EN2 = 'AO_EN2'
    AO_EN3 = 'AO_EN3'
    AO_EN4 = 'AO_EN4'
    AO_EN5 = 'AO_EN5'
    AO_EN6 = 'AO_EN6'
    AO_EN7 = 'AO_EN7'
    AO_EN8 = 'AO_EN8'
