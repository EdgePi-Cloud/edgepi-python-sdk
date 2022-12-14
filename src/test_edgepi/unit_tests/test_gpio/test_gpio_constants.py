"""unit tests for gpio_constants module"""


import pytest
from edgepi.reg_helper.reg_helper import _apply_opcode
from edgepi.gpio.gpio_constants import (
    GpioAOutputClear,
    GpioAOutputSet,
    GpioAPinDirIn,
    GpioAPinDirOut,
)


@pytest.mark.parametrize(
    "reg_value, opcode, updated_reg_value",
    [
        (0b00000000, GpioAOutputSet.SET_OUTPUT_1.value, 0b00000001),  # Set Bit1
        (0b00000001, GpioAOutputSet.SET_OUTPUT_2.value, 0b00000011),  # Set Bit2
        (0b00000011, GpioAOutputSet.SET_OUTPUT_3.value, 0b00000111),  # Set Bit3
        (0b00000111, GpioAOutputSet.SET_OUTPUT_4.value, 0b00001111),  # Set Bit4
        (0b00001111, GpioAOutputSet.SET_OUTPUT_5.value, 0b00011111),  # Set Bit5
        (0b00011111, GpioAOutputSet.SET_OUTPUT_6.value, 0b00111111),  # Set Bit6
        (0b00111111, GpioAOutputSet.SET_OUTPUT_7.value, 0b01111111),  # Set Bit7
        (0b01111111, GpioAOutputSet.SET_OUTPUT_8.value, 0b11111111),  # Set Bit8
        (0b00000000, GpioAOutputSet.SET_OUTPUT_ALL.value, 0b11111111),  # Set ALL
    ],
)
def test_output_set(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value


@pytest.mark.parametrize(
    "reg_value, opcode, updated_reg_value",
    [
        (0b11111111, GpioAOutputClear.CLEAR_OUTPUT_8.value, 0b01111111),  # Claer Bit8
        (0b01111111, GpioAOutputClear.CLEAR_OUTPUT_7.value, 0b00111111),  # Claer Bit7
        (0b00111111, GpioAOutputClear.CLEAR_OUTPUT_6.value, 0b00011111),  # Claer Bit6
        (0b00011111, GpioAOutputClear.CLEAR_OUTPUT_5.value, 0b00001111),  # Claer Bit5
        (0b00001111, GpioAOutputClear.CLEAR_OUTPUT_4.value, 0b00000111),  # Claer Bit4
        (0b00000111, GpioAOutputClear.CLEAR_OUTPUT_3.value, 0b00000011),  # Claer Bit3
        (0b00000011, GpioAOutputClear.CLEAR_OUTPUT_2.value, 0b00000001),  # Claer Bit2
        (0b00000001, GpioAOutputClear.CLEAR_OUTPUT_1.value, 0b00000000),  # Claer Bit1
        (0b11111111, GpioAOutputClear.CLEAR_OUTPUT_ALL.value, 0b00000000),  # Claer ALL
    ],
)
def test_output_clear(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value


@pytest.mark.parametrize(
    "reg_value, opcode, updated_reg_value",
    [
        (0b11111111, GpioAPinDirOut.PIN8_DIR_OUT.value, 0b01111111),  # Output Dir Bit8
        (0b01111111, GpioAPinDirOut.PIN7_DIR_OUT.value, 0b00111111),  # Output Dir Bit7
        (0b00111111, GpioAPinDirOut.PIN6_DIR_OUT.value, 0b00011111),  # Output Dir Bit6
        (0b00011111, GpioAPinDirOut.PIN5_DIR_OUT.value, 0b00001111),  # Output Dir Bit5
        (0b00001111, GpioAPinDirOut.PIN4_DIR_OUT.value, 0b00000111),  # Output Dir Bit4
        (0b00000111, GpioAPinDirOut.PIN3_DIR_OUT.value, 0b00000011),  # Output Dir Bit3
        (0b00000011, GpioAPinDirOut.PIN2_DIR_OUT.value, 0b00000001),  # Output Dir Bit2
        (0b00000001, GpioAPinDirOut.PIN1_DIR_OUT.value, 0b00000000),  # Output Dir Bit1
        (0b11111111, GpioAPinDirOut.ALL_DIR_OUT.value, 0b00000000),  # Output Dir ALL
    ],
)
def test_pin_dir_out(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value


@pytest.mark.parametrize(
    "reg_value, opcode, updated_reg_value",
    [
        (0b00000000, GpioAPinDirIn.PIN1_DIR_IN.value, 0b00000001),  # Input Dir Bit8
        (0b00000001, GpioAPinDirIn.PIN2_DIR_IN.value, 0b00000011),  # Input Dir Bit7
        (0b00000011, GpioAPinDirIn.PIN3_DIR_IN.value, 0b00000111),  # Input Dir Bit6
        (0b00000111, GpioAPinDirIn.PIN4_DIR_IN.value, 0b00001111),  # Input Dir Bit5
        (0b00001111, GpioAPinDirIn.PIN5_DIR_IN.value, 0b00011111),  # Input Dir Bit4
        (0b00011111, GpioAPinDirIn.PIN6_DIR_IN.value, 0b00111111),  # Input Dir Bit3
        (0b00111111, GpioAPinDirIn.PIN7_DIR_IN.value, 0b01111111),  # Input Dir Bit2
        (0b01111111, GpioAPinDirIn.PIN8_DIR_IN.value, 0b11111111),  # Input Dir Bit1
        (0b00000000, GpioAPinDirIn.ALL_DIR_IN.value, 0b11111111),  # Input Dir ALL
    ],
)
def test_pin_dir_in(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value
