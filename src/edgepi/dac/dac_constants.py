""" Constants for DAC device modules """


from enum import Enum


DAC_PRECISION = 3  # decimal place precision for voltage conversions
SW_RESET = 0x1234  # software reset command data bits
NULL_BITS = 0x0
READ_WRITE_SIZE = 3  # size of DAC read/write in bytes
UPPER_LIMIT = 5.000 # upper limit for voltage writes to DAC


class EdgePiDacCom(Enum):
    """Commands for EdgePi DAC"""

    COM_NOP = 0x0
    COM_WRITE_INPUT = 0x1  # LDAC pin is held low, so not used
    COM_UPDATE_DAC = 0x2
    COM_WRITE_UPDATE = 0x3
    COM_POWER_DOWN_OP = 0x4
    COM_HW_LDAC_MASK = 0x5  # LDAC pin is held low, so not used
    COM_SW_RESET = 0x6  # resets to POR, address bits set to 0x0 and data bits set to 0x1234
    COM_GAIN = 0x7
    COM_DCEN = 0x8  # Daisy chain setup enable
    COM_READBACK = 0x9  # used for daisy chain operation
    COM_UPDATE_ALL_CH = (
        0x0A  # update all channels of the input register simultaneously with the input data
    )
    # update all channel of teh input register and DAC register simultaneously with the input data
    COM_UPDATE_ALL_DAC = 0x0B


class DACChannel(Enum):
    """EdgePi DAC channel addresses"""

    AOUT1 = 0x0
    AOUT2 = 0x1
    AOUT3 = 0x2
    AOUT4 = 0x3
    AOUT5 = 0x4
    AOUT6 = 0x5
    AOUT7 = 0x6
    AOUT8 = 0x7


NUM_PINS = len(DACChannel)


class EdgePiDacCalibrationConstants(Enum):
    """EdgePi DAC calibration constants"""

    V_RANGE = 5.0000
    RANGE = 65535
    DAC_GAIN_FACTOR = 2


class PowerMode(Enum):
    """
    EdgePi DAC power modes

    Attributes:
        NORMAL: normal power consumption of 1.1 mA typically

        POWER_DOWN_GROUND: low power consumption, 1 μA typically. DAC output stage
            connected internally to GND through 1 kΩ resistor.

        POWER_DOWN_3_STATE: low power consumption, 1 μA typically. DAC output stage
            left open circuited (three-state).
    """

    NORMAL = 0x0
    POWER_DOWN_GROUND = 0x1
    POWER_DOWN_3_STATE = 0x3


class AOPins(Enum):
    """Analog/Digital out gpio pin names"""

    AO_EN1 = "AO_EN1"
    AO_EN2 = "AO_EN2"
    AO_EN3 = "AO_EN3"
    AO_EN4 = "AO_EN4"
    AO_EN5 = "AO_EN5"
    AO_EN6 = "AO_EN6"
    AO_EN7 = "AO_EN7"
    AO_EN8 = "AO_EN8"

class DOPins(Enum):
    """Analog/Digital out gpio pin names"""

    DOUT1 = 'DOUT1'
    DOUT2 = 'DOUT2'
    DOUT3 = 'DOUT3'
    DOUT4 = 'DOUT4'
    DOUT5 = 'DOUT5'
    DOUT6 = 'DOUT6'
    DOUT7 = 'DOUT7'
    DOUT8 = 'DOUT8'

class GainPin(Enum):
    """DAC gain enable/disable pin"""
    DAC_GAIN = "DAC_GAIN"
