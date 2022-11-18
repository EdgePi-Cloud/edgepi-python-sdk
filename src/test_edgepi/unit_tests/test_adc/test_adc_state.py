"Unit testing ADCState class"

from unittest import mock
from copy import deepcopy
import sys
import pytest

sys.modules['periphery'] = mock.MagicMock()

# pylint: disable=wrong-import-position
# mocked periphery module needs to be placed above
from edgepi.adc.edgepi_adc import ADCState
from edgepi.adc.adc_query_lang import ADCProperties
from edgepi.adc.adc_constants import (
    ADC1DataRate,
    ADC2DataRate,
    ADCChannel,
    ADCReg,
    CheckMode,
    ConvMode,
    FilterMode,
    StatusByte,
)

# mock default register values
ADC_REGS = {
    ADCReg.REG_ID.value: 0x0,
    ADCReg.REG_POWER.value: 0x0,
    ADCReg.REG_INTERFACE.value: 0x0,
    ADCReg.REG_MODE0.value: 0x0,
    ADCReg.REG_MODE1.value: 0x0,
    ADCReg.REG_MODE2.value: 0x0,
    ADCReg.REG_INPMUX.value: 0x0,
    ADCReg.REG_OFCAL0.value: 0x0,
    ADCReg.REG_OFCAL1.value: 0x0,
    ADCReg.REG_OFCAL2.value: 0x0,
    ADCReg.REG_FSCAL0.value: 0x0,
    ADCReg.REG_FSCAL1.value: 0x0,
    ADCReg.REG_FSCAL2.value: 0x0,
    ADCReg.REG_IDACMUX.value: 0x0,
    ADCReg.REG_IDACMAG.value: 0x0,
    ADCReg.REG_REFMUX.value: 0x0,
    ADCReg.REG_TDACP.value: 0x0,
    ADCReg.REG_TDACN.value: 0x0,
    ADCReg.REG_GPIOCON.value: 0x0,
    ADCReg.REG_GPIODIR.value: 0x0,
    ADCReg.REG_GPIODAT.value: 0x0,
    ADCReg.REG_ADC2CFG.value: 0x0,
    ADCReg.REG_ADC2MUX.value: 0x0,
    ADCReg.REG_ADC2OFC0.value: 0x0,
    ADCReg.REG_ADC2OFC1.value: 0x0,
    ADCReg.REG_ADC2FSC0.value: 0x0,
    ADCReg.REG_ADC2FSC1.value: 0x0,
}


def _apply_register_updates(reg_map: dict, updates: dict):
    for addx, value in updates.items():
        reg_map[addx] = value


@pytest.mark.parametrize(
    "updates, state_property, expected",
    [
        # CHECK_MODE
        (
            {ADCReg.REG_INTERFACE.value: 0x2},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CRC.value.op_code],
        ),
        (
            {ADCReg.REG_INTERFACE.value: 0x1},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CHK.value.op_code],
        ),
        (
            {ADCReg.REG_INTERFACE.value: 0x0},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_OFF.value.op_code],
        ),
        # CONV_MODE
        (
            {ADCReg.REG_MODE0.value: 0x40},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.PULSE.value.op_code],
        ),
        (
            {ADCReg.REG_MODE0.value: 0x00},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.CONTINUOUS.value.op_code],
        ),
        # STATUS_MODE
        (
            {ADCReg.REG_INTERFACE.value: 0x0},
            "state.status_byte",
            ADCProperties.STATUS_MODE.value.values[StatusByte.STATUS_BYTE_OFF.value.op_code],
        ),
        (
            {ADCReg.REG_INTERFACE.value: 0x4},
            "state.status_byte",
            ADCProperties.STATUS_MODE.value.values[StatusByte.STATUS_BYTE_ON.value.op_code],
        ),
        # ADC1_MUXP
        (
            {ADCReg.REG_INPMUX.value: 0x00},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x10},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x20},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x30},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x40},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x50},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x60},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x70},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x80},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN8.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x90},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN9.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0xA0},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0xF0},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC1_MUXN
        (
            {ADCReg.REG_INPMUX.value: 0x00},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x1},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x2},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x3},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x4},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x5},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x6},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x7},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x8},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN8.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0x9},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN9.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0xA},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {ADCReg.REG_INPMUX.value: 0xF},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # ADC2_MUXP
        (
            {ADCReg.REG_ADC2MUX.value: 0x00},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x10},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x20},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x30},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x40},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x50},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x60},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x70},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x80},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN8.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x90},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN9.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0xA0},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0xF0},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC2_MUXN
        (
            {ADCReg.REG_ADC2MUX.value: 0x00},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x1},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x2},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x3},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x4},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x5},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x6},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x7},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x8},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN8.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0x9},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN9.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0xA},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {ADCReg.REG_ADC2MUX.value: 0xF},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # FILTER_MODE
        (
            {ADCReg.REG_MODE1.value: 0x0},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC1.value.op_code],
        ),
        (
            {ADCReg.REG_MODE1.value: 0b00100000},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC2.value.op_code],
        ),
        (
            {ADCReg.REG_MODE1.value: 0b01000000},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC3.value.op_code],
        ),
        (
            {ADCReg.REG_MODE1.value: 0b01100000},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC4.value.op_code],
        ),
        (
            {ADCReg.REG_MODE1.value: 0b10000000},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.FIR.value.op_code],
        ),
        # RTD on
        (
            {
                ADCReg.REG_INPMUX.value: 0x56,
                ADCReg.REG_IDACMUX.value: 0x98,
                ADCReg.REG_IDACMAG.value: 0x44,
                ADCReg.REG_REFMUX.value: 0b00011100,
            },
            "state.rtd_on",
            True
        ),
        # RTD off
        (
            {
                ADCReg.REG_INPMUX.value: 0xFA,
                ADCReg.REG_IDACMUX.value: 0xBB,
                ADCReg.REG_IDACMAG.value: 0x00,
                ADCReg.REG_REFMUX.value: 0x00,
            },
            "state.rtd_on",
            False
        ),
        # RTD improperly configured
        (
            {
                ADCReg.REG_INPMUX.value: 0x56,
                ADCReg.REG_IDACMUX.value: 0x98,
                ADCReg.REG_IDACMAG.value: 0x48,
                ADCReg.REG_REFMUX.value: 0b00011100,
            },
            "state.rtd_on",
            False
        ),
        # ADC1 Data Rate
        (
            {ADCReg.REG_MODE2.value: 0x00},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2P5.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x01},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_5.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x02},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_10.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x03},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_16P6.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x04},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_20.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x05},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_50.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x06},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_60.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x07},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_100.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x08},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_400.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x09},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_1200.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x0A},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2400.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x0B},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_4800.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x0C},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_7200.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x0D},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_14400.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x0E},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_19200.value.op_code],
        ),
        (
            {ADCReg.REG_MODE2.value: 0x0F},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_38400.value.op_code],
        ),
        # ADC2 Data Rate
        (
            {ADCReg.REG_ADC2CFG.value: 0x00},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_10.value.op_code],
        ),
        (
            {ADCReg.REG_ADC2CFG.value: 0x40},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_100.value.op_code],
        ),
        (
            {ADCReg.REG_ADC2CFG.value: 0x80},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_400.value.op_code],
        ),
        (
            {ADCReg.REG_ADC2CFG.value: 0xC0},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_800.value.op_code],
        ),
    ],
)
def test_adc_state_init(updates, state_property, expected):
    reg_map = deepcopy(ADC_REGS)
    _apply_register_updates(reg_map, updates)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = ADCState(reg_map)
    assert eval(state_property) == expected
