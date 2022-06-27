from enum import Enum, unique
from edgepi.reg_helper.reg_helper import OpCode
from edgepi.gpio.gpio_configs import *

@unique
class GpioExpanderAddress(Enum):
    EXP_ONE = 32
    EXP_TWO = 33

@unique
class GPIOAddresses(Enum):
    # Read addresses
    INPUT_PORT_0  = 0x00 
    INPUT_PORT_1  = 0x01
    OUTPUT_PORT_0 = 0x02 
    OUTPUT_PORT_1 = 0x03 
    POLARITY_INVERSION_PORT_0 = 0x04 
    POLARITY_INVERSION_PORT_1 = 0x05 
    CONFIGURATION_PORT_0 = 0x06 
    CONFIGURATION_PORT_1 = 0x07 

class BitMask(Enum):
    BIT0 = 0xFE
    BIT1 = 0xFD
    BIT2 = 0xFB
    BIT3 = 0xF7
    BIT4 = 0xEF
    BIT5 = 0xDF
    BIT6 = 0xBF
    BIT7 = 0x7F
    BYTE = 0x00



@unique
class GpioAOutputSet(Enum):
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
class GpioAOutputClear(Enum):
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
class GpioBOutputSet(Enum):
    SET_OUTPUT_1 = OpCode(0x01, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT0.value)
    SET_OUTPUT_2 = OpCode(0x02, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT1.value)
    SET_OUTPUT_3 = OpCode(0x04, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT2.value)
    SET_OUTPUT_4 = OpCode(0x08, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT3.value)
    SET_OUTPUT_5 = OpCode(0x10, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT4.value)
    SET_OUTPUT_6 = OpCode(0x20, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT5.value)
    SET_OUTPUT_7 = OpCode(0x40, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT6.value)
    SET_OUTPUT_8 = OpCode(0x80, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT7.value)
    SET_OUTPUT_ALL = OpCode(0xFF, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BYTE.value)

@unique
class GpioBOutputClear(Enum):
    CLEAR_OUTPUT_1 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT0.value)
    CLEAR_OUTPUT_2 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT1.value)
    CLEAR_OUTPUT_3 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT2.value)
    CLEAR_OUTPUT_4 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT3.value)
    CLEAR_OUTPUT_5 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT4.value)
    CLEAR_OUTPUT_6 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT5.value)
    CLEAR_OUTPUT_7 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT6.value)
    CLEAR_OUTPUT_8 = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_1.value, BitMask.BIT7.value)
    CLEAR_OUTPUT_ALL = OpCode(0x00, GPIOAddresses.OUTPUT_PORT_0.value, BitMask.BYTE.value)

@unique
class GpioAPinDir(Enum):
    PIN1_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT0.value)    
    PIN2_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT1.value)
    PIN3_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT2.value)
    PIN4_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT3.value)
    PIN5_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT4.value)
    PIN6_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT5.value)
    PIN7_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT6.value)
    PIN8_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BIT7.value)
    ALL_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BYTE.value)

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
class GpioBPinDir(Enum):
    PIN1_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT0.value)    
    PIN2_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT1.value)
    PIN3_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT2.value)
    PIN4_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT3.value)
    PIN5_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT4.value)
    PIN6_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT5.value)
    PIN7_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT6.value)
    PIN8_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT7.value)
    ALL_DIR_OUT = OpCode(0x00, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BYTE.value)


    PIN1_DIR_IN = OpCode(0x01, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT0.value)
    PIN2_DIR_IN = OpCode(0x02, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT1.value)
    PIN3_DIR_IN = OpCode(0x04, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT2.value)
    PIN4_DIR_IN = OpCode(0x08, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT3.value)
    PIN5_DIR_IN = OpCode(0x10, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT4.value)
    PIN6_DIR_IN = OpCode(0x20, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT5.value)
    PIN7_DIR_IN = OpCode(0x40, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT6.value)
    PIN8_DIR_IN = OpCode(0x80, GPIOAddresses.CONFIGURATION_PORT_1.value, BitMask.BIT7.value)
    ALL_DIR_IN = OpCode(0xFF, GPIOAddresses.CONFIGURATION_PORT_0.value, BitMask.BYTE.value)

