""" Constants for DAC device modules """


from enum import Enum


SW_RESET = 0x1234


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


class EdgePiDacChannel(Enum):
    """EdgePi DAC channel addresses"""

    DAC0 = 0x0
    DAC1 = 0x1
    DAC2 = 0x2
    DAC3 = 0x3
    DAC4 = 0x4
    DAC5 = 0x5
    DAC6 = 0x6
    DAC7 = 0x7


class EdgePiDacCalibrationConstants(Enum):
    """EdgePi DAC calibration constants"""

    VOLTAGE_REF = 2.047
    RANGE = 65535


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


class GainMode(Enum):
    """
    EdgePi DAC output amplifier gain modes

    Attributes:
        NO_AMP: amplifier gain = 1

        DOUBLE_AMP: amplifier gain = 2
    """

    NO_AMP = 0x0
    DOUBLE_AMP = 0x4
