""" Utility module containing constants for gpio modules """


from enum import Enum, unique
from edgepi.reg_helper.reg_helper import OpCode, BitMask


class GpioExpanderAddress(Enum):
    """GPIO expander i2c device addresses"""

    EXP_ONE = 32
    EXP_TWO = 33


@unique
class GPIOAddresses(Enum):
    """GPIO expander port addresses"""

    # Read addresses
    INPUT_PORT_0 = 0x00
    INPUT_PORT_1 = 0x01
    OUTPUT_PORT_0 = 0x02    # Port B
    OUTPUT_PORT_1 = 0x03    # Port A
    POLARITY_INVERSION_PORT_0 = 0x04
    POLARITY_INVERSION_PORT_1 = 0x05
    CONFIGURATION_PORT_0 = 0x06 # Port B
    CONFIGURATION_PORT_1 = 0x07 # Port A


@unique
class GpioAOutputSet(Enum):
    """valid opcodes for setting a GPIO Expander's Port A (Output Port 1)"""

    SET_OUTPUT_1 = OpCode(0x01, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT0.value)
    SET_OUTPUT_2 = OpCode(0x02, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT1.value)
    SET_OUTPUT_3 = OpCode(0x04, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT2.value)
    SET_OUTPUT_4 = OpCode(0x08, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT3.value)
    SET_OUTPUT_5 = OpCode(0x10, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT4.value)
    SET_OUTPUT_6 = OpCode(0x20, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT5.value)
    SET_OUTPUT_7 = OpCode(0x40, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT6.value)
    SET_OUTPUT_8 = OpCode(0x80, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT7.value)
    SET_OUTPUT_ALL = OpCode(0xFF, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BYTE.value)


@unique
class GpioAOutputClear(Enum):
    """valid opcodes for clearing a GPIO Expander's A (Output Port 1)"""

    CLEAR_OUTPUT_1 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT0.value)
    CLEAR_OUTPUT_2 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT1.value)
    CLEAR_OUTPUT_3 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT2.value)
    CLEAR_OUTPUT_4 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT3.value)
    CLEAR_OUTPUT_5 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT4.value)
    CLEAR_OUTPUT_6 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT5.value)
    CLEAR_OUTPUT_7 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT6.value)
    CLEAR_OUTPUT_8 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT7.value)
    CLEAR_OUTPUT_ALL = OpCode(
        0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BYTE.value
    )


@unique
class GpioBOutputSet(Enum):
    """valid opcodes for setting a GPIO Expander's Port B (Output Port 0)"""

    SET_OUTPUT_1 = OpCode(0x01, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT0.value)
    SET_OUTPUT_2 = OpCode(0x02, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT1.value)
    SET_OUTPUT_3 = OpCode(0x04, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT2.value)
    SET_OUTPUT_4 = OpCode(0x08, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT3.value)
    SET_OUTPUT_5 = OpCode(0x10, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT4.value)
    SET_OUTPUT_6 = OpCode(0x20, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT5.value)
    SET_OUTPUT_7 = OpCode(0x40, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT6.value)
    SET_OUTPUT_8 = OpCode(0x80, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT7.value)
    SET_OUTPUT_ALL = OpCode(0xFF, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BYTE.value)


@unique
class GpioBOutputClear(Enum):
    """valid opcodes for clearing a GPIO Expander's Port B (Output Port 0)"""

    CLEAR_OUTPUT_1 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT0.value)
    CLEAR_OUTPUT_2 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT1.value)
    CLEAR_OUTPUT_3 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT2.value)
    CLEAR_OUTPUT_4 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT3.value)
    CLEAR_OUTPUT_5 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT4.value)
    CLEAR_OUTPUT_6 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT5.value)
    CLEAR_OUTPUT_7 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT6.value)
    CLEAR_OUTPUT_8 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BIT7.value)
    CLEAR_OUTPUT_ALL = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BYTE.value)

@unique
class GpioAPinDirOut(Enum):
    """
    Opcodes for setting a GPIO Expander's Port A pin direction to output (Configuration Port 1)
    """
    PIN1_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT0.value)
    PIN2_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT1.value)
    PIN3_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT2.value)
    PIN4_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT3.value)
    PIN5_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT4.value)
    PIN6_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT5.value)
    PIN7_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT6.value)
    PIN8_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT7.value)
    ALL_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BYTE.value)

@unique
class GpioAPinDirIn(Enum):
    """
    Opcodes for setting a GPIO Expander's Port A pin direction to input (Configuration Port 1)
    """
    PIN1_DIR_IN = OpCode(0x01, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT0.value)
    PIN2_DIR_IN = OpCode(0x02, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT1.value)
    PIN3_DIR_IN = OpCode(0x04, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT2.value)
    PIN4_DIR_IN = OpCode(0x08, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT3.value)
    PIN5_DIR_IN = OpCode(0x10, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT4.value)
    PIN6_DIR_IN = OpCode(0x20, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT5.value)
    PIN7_DIR_IN = OpCode(0x40, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT6.value)
    PIN8_DIR_IN = OpCode(0x80, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT7.value)
    ALL_DIR_IN = OpCode(0xFF, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BYTE.value)


@unique
class GpioBPinDirOut(Enum):
    """
    Opcodes for setting a GPIO Expander's Port B pin direction to output (Configuration Port 0)
    """
    PIN1_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT0.value)
    PIN2_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT1.value)
    PIN3_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT2.value)
    PIN4_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT3.value)
    PIN5_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT4.value)
    PIN6_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT5.value)
    PIN7_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT6.value)
    PIN8_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT7.value)
    ALL_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BYTE.value)

@unique
class GpioBPinDirIn(Enum):
    """
    Opcodes for setting a GPIO Expander's Port B pin direction to input (Configuration Port 0)
    """
    PIN1_DIR_IN = OpCode(0x01, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT0.value)
    PIN2_DIR_IN = OpCode(0x02, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT1.value)
    PIN3_DIR_IN = OpCode(0x04, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT2.value)
    PIN4_DIR_IN = OpCode(0x08, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT3.value)
    PIN5_DIR_IN = OpCode(0x10, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT4.value)
    PIN6_DIR_IN = OpCode(0x20, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT5.value)
    PIN7_DIR_IN = OpCode(0x40, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT6.value)
    PIN8_DIR_IN = OpCode(0x80, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT7.value)
    ALL_DIR_IN = OpCode(0xFF, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BYTE.value)

@unique
class GpioDevPaths(Enum):
    """
    GPIO device paths
    """
    I2C_DEV_PATH = '/dev/i2c-10'
    GPIO_CIHP_DEV_PATH = '/dev/gpiochip0'

@unique
class GpioPins(Enum):
    """GPIO Pin Names"""
    LED_OVR1 = 'LED_OVR1'
    LED_OVR2 = 'LED_OVR2'
    LED_OVR3 = 'LED_OVR3'
    LED_OVR4 = 'LED_OVR4'
    LED_OVR5 = 'LED_OVR5'
    LED_OVR6 = 'LED_OVR6'
    LED_OVR7 = 'LED_OVR7'
    LED_OVR8 = 'LED_OVR8'
    AO_EN1 = 'AO_EN1'
    AO_EN2 = 'AO_EN2'
    AO_EN3 = 'AO_EN3'
    AO_EN4 = 'AO_EN4'
    AO_EN5 = 'AO_EN5'
    AO_EN6 = 'AO_EN6'
    AO_EN7 = 'AO_EN7'
    AO_EN8 = 'AO_EN8'
    DAC_GAIN = 'DAC_GAIN'
    GNDSW_IN1 = 'GNDSW_IN1'
    GNDSW_IN2 = 'GNDSW_IN2'
    RTD_EN = 'RTD_EN'
    RELAY = 'RELAY'
    DOUT1 = 'DOUT1'
    DOUT2 = 'DOUT2'
    DOUT3 = 'DOUT3'
    DOUT4 = 'DOUT4'
    DOUT5 = 'DOUT5'
    DOUT6 = 'DOUT6'
    DOUT7 = 'DOUT7'
    DOUT8 = 'DOUT8'
    DIN1 = 'DIN1'
    DIN2 = 'DIN2'
    DIN3 = 'DIN3'
    DIN4 = 'DIN4'
    DIN5 = 'DIN5'
    DIN6 = 'DIN6'
    DIN7 = 'DIN7'
    DIN8 = 'DIN8'
    BUZZER = 'BUZZER'
    AUDIO = 'AUDIO'
