"Unit testing ADCState class"

import sys
import pytest
from unittest import mock
from copy import deepcopy


from edgepi.adc.edgepi_adc import ADCState
from edgepi.adc.adc_query_lang import ADCModes
from edgepi.adc.adc_constants import ADCReg, CheckMode, ConvMode, StatusByte

# to allow development on windows
sys.modules["periphery"] = mock.MagicMock()


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
            ADCModes.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CRC.value.op_code],
        ),
        (
            {ADCReg.REG_INTERFACE.value: 0x1},
            "state.checksum_mode",
            ADCModes.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CHK.value.op_code],
        ),
        (
            {ADCReg.REG_INTERFACE.value: 0x0},
            "state.checksum_mode",
            ADCModes.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_OFF.value.op_code],
        ),
        # CONV_MODE
        (
            {ADCReg.REG_MODE0.value: 0x40},
            "state.adc_1.conversion_mode",
            ADCModes.CONV_MODE.value.values[ConvMode.PULSE.value.op_code],
        ),
        (
            {ADCReg.REG_MODE0.value: 0x00},
            "state.adc_1.conversion_mode",
            ADCModes.CONV_MODE.value.values[ConvMode.CONTINUOUS.value.op_code],
        ),
        # STATUS_MODE
        (
            {ADCReg.REG_INTERFACE.value: 0x0},
            "state.status_byte",
            ADCModes.STATUS_MODE.value.values[StatusByte.STATUS_BYTE_OFF.value.op_code],
        ),
        (
            {ADCReg.REG_INTERFACE.value: 0x4},
            "state.status_byte",
            ADCModes.STATUS_MODE.value.values[StatusByte.STATUS_BYTE_ON.value.op_code],
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
