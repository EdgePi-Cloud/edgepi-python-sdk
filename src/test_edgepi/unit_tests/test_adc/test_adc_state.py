"""Unit tests for ADCState class"""


from copy import deepcopy

import sys
from unittest import mock
import pytest
from edgepi.adc.adc_constants import (
    ADC1DataRate,
    ADCReg,
    ADCModes,
    ConvMode,
    CheckMode,
    FilterMode,
    StatusByte,
)
# pylint: disable=wrong-import-position, protected-access
sys.modules["periphery"] = mock.MagicMock()
from edgepi.adc.edgepi_adc import ADCState

ADC_REGS = {
    ADCReg.REG_ID.value: {"value": 0x0},
    ADCReg.REG_POWER.value: {"value": 0x0},
    ADCReg.REG_INTERFACE.value: {"value": 0x0},
    ADCReg.REG_MODE0.value: {"value": 0x0},
    ADCReg.REG_MODE1.value: {"value": 0x0},
    ADCReg.REG_MODE2.value: {"value": 0x0},
    ADCReg.REG_INPMUX.value: {"value": 0x0},
    ADCReg.REG_OFCAL0.value: {"value": 0x0},
    ADCReg.REG_OFCAL1.value: {"value": 0x0},
    ADCReg.REG_OFCAL2.value: {"value": 0x0},
    ADCReg.REG_FSCAL0.value: {"value": 0x0},
    ADCReg.REG_FSCAL1.value: {"value": 0x0},
    ADCReg.REG_FSCAL2.value: {"value": 0x0},
    ADCReg.REG_IDACMUX.value: {"value": 0x0},
    ADCReg.REG_IDACMAG.value: {"value": 0x0},
    ADCReg.REG_REFMUX.value: {"value": 0x0},
    ADCReg.REG_TDACP.value: {"value": 0x0},
    ADCReg.REG_TDACN.value: {"value": 0x0},
    ADCReg.REG_GPIOCON.value: {"value": 0x0},
    ADCReg.REG_GPIODIR.value: {"value": 0x0},
    ADCReg.REG_GPIODAT.value: {"value": 0x0},
    ADCReg.REG_ADC2CFG.value: {"value": 0x0},
    ADCReg.REG_ADC2MUX.value: {"value": 0x0},
    ADCReg.REG_ADC2OFC0.value: {"value": 0x0},
    ADCReg.REG_ADC2OFC1.value: {"value": 0x0},
    ADCReg.REG_ADC2FSC0.value: {"value": 0x0},
    ADCReg.REG_ADC2FSC1.value: {"value": 0x0},
}


def _apply_register_updates(reg_map: dict, updates: dict):
    for addx, value in updates.items():
        reg_map[addx]["value"] = value


@pytest.mark.parametrize(
    "mode, updates, expected",
    [
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b01000000}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b11000000}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b11100000}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b11110000}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b11111000}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b11111100}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b11111110}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b11111111}, ConvMode.PULSE.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b00000000}, ConvMode.CONTINUOUS.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b10000000}, ConvMode.CONTINUOUS.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b10100000}, ConvMode.CONTINUOUS.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b10110000}, ConvMode.CONTINUOUS.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b10111000}, ConvMode.CONTINUOUS.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b10111100}, ConvMode.CONTINUOUS.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b10111110}, ConvMode.CONTINUOUS.value.op_code),
        (ADCModes.CONV, {ADCReg.REG_MODE0.value: 0b10111111}, ConvMode.CONTINUOUS.value.op_code),
        (
            ADCModes.CHECK,
            {ADCReg.REG_INTERFACE.value: 0b00000000},
            CheckMode.CHECK_BYTE_OFF.value.op_code,
        ),
        (
            ADCModes.CHECK,
            {ADCReg.REG_INTERFACE.value: 0b00000001},
            CheckMode.CHECK_BYTE_CHK.value.op_code,
        ),
        (
            ADCModes.CHECK,
            {ADCReg.REG_INTERFACE.value: 0b00000010},
            CheckMode.CHECK_BYTE_CRC.value.op_code,
        ),
        (
            ADCModes.CHECK,
            {ADCReg.REG_INTERFACE.value: 0b11111100},
            CheckMode.CHECK_BYTE_OFF.value.op_code,
        ),
        (
            ADCModes.CHECK,
            {ADCReg.REG_INTERFACE.value: 0b11111101},
            CheckMode.CHECK_BYTE_CHK.value.op_code,
        ),
        (
            ADCModes.CHECK,
            {ADCReg.REG_INTERFACE.value: 0b11111110},
            CheckMode.CHECK_BYTE_CRC.value.op_code,
        ),
        (
            ADCModes.STATUS,
            {ADCReg.REG_INTERFACE.value: 0b00000000},
            StatusByte.STATUS_BYTE_OFF.value.op_code,
        ),
        (
            ADCModes.STATUS,
            {ADCReg.REG_INTERFACE.value: 0b00000100},
            StatusByte.STATUS_BYTE_ON.value.op_code,
        ),
        (
            ADCModes.STATUS,
            {ADCReg.REG_INTERFACE.value: 0b11111011},
            StatusByte.STATUS_BYTE_OFF.value.op_code,
        ),
        (
            ADCModes.STATUS,
            {ADCReg.REG_INTERFACE.value: 0b11111111},
            StatusByte.STATUS_BYTE_ON.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000000},
            ADC1DataRate.SPS_2P5.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000001},
            ADC1DataRate.SPS_5.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000010},
            ADC1DataRate.SPS_10.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000011},
            ADC1DataRate.SPS_16P6.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000100},
            ADC1DataRate.SPS_20.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000101},
            ADC1DataRate.SPS_50.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000110},
            ADC1DataRate.SPS_60.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00000111},
            ADC1DataRate.SPS_100.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001000},
            ADC1DataRate.SPS_400.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001001},
            ADC1DataRate.SPS_1200.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001010},
            ADC1DataRate.SPS_2400.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001011},
            ADC1DataRate.SPS_4800.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001100},
            ADC1DataRate.SPS_7200.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001101},
            ADC1DataRate.SPS_14400.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001110},
            ADC1DataRate.SPS_19200.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b00001111},
            ADC1DataRate.SPS_38400.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110000},
            ADC1DataRate.SPS_2P5.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110001},
            ADC1DataRate.SPS_5.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110010},
            ADC1DataRate.SPS_10.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110011},
            ADC1DataRate.SPS_16P6.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110100},
            ADC1DataRate.SPS_20.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110101},
            ADC1DataRate.SPS_50.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110110},
            ADC1DataRate.SPS_60.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11110111},
            ADC1DataRate.SPS_100.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111000},
            ADC1DataRate.SPS_400.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111001},
            ADC1DataRate.SPS_1200.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111010},
            ADC1DataRate.SPS_2400.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111011},
            ADC1DataRate.SPS_4800.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111100},
            ADC1DataRate.SPS_7200.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111101},
            ADC1DataRate.SPS_14400.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111110},
            ADC1DataRate.SPS_19200.value.op_code,
        ),
        (
            ADCModes.DATA_RATE_1,
            {ADCReg.REG_MODE2.value: 0b11111111},
            ADC1DataRate.SPS_38400.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b00000000},
            FilterMode.SINC1.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b00011111},
            FilterMode.SINC1.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b00100000},
            FilterMode.SINC2.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b00111111},
            FilterMode.SINC2.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b01000000},
            FilterMode.SINC3.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b01011111},
            FilterMode.SINC3.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b01100000},
            FilterMode.SINC4.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b01111111},
            FilterMode.SINC4.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b10000000},
            FilterMode.FIR.value.op_code,
        ),
        (
            ADCModes.FILTER,
            {ADCReg.REG_MODE1.value: 0b10011111},
            FilterMode.FIR.value.op_code,
        ),
    ],
)
def test_get_state(mode, updates, expected):
    reg_map = deepcopy(ADC_REGS)
    _apply_register_updates(reg_map, updates)
    state = ADCState(reg_map)
    assert state.get_state(mode) == expected
