"""tests for edgepi_tc module"""


from copy import deepcopy
from unittest import mock
from unittest.mock import call, patch
import sys

sys.modules['periphery'] = mock.MagicMock()

# pylint: disable=wrong-import-position

import pytest
from edgepi.tc.edgepi_tc import EdgePiTC, TCState
from edgepi.tc.tc_constants import (
    AvgMode,
    CJHighMask,
    CJLowMask,
    CJMode,
    ConvMode,
    DecBits4,
    DecBits6,
    FaultMode,
    NoiseFilterMode,
    Masks,
    OpenCircuitMode,
    OpenMask,
    OvuvMask,
    TCAddresses,
    TCHighMask,
    TCLowMask,
    TCType,
    VoltageMode,
    TCOps,
)
from edgepi.tc.tc_faults import FaultMsg, FaultType, Fault

# pylint: disable=protected-access



@pytest.fixture(name="tc")
def fixture_test_edgepi_tc(mocker):
    # mocker acts as context manager
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.tc.edgepi_tc.Bits")
    # yield instead of return so local state (i.e mocks) not lost
    # upon returning EdgePiTC object in test functions below
    yield EdgePiTC()

@pytest.fixture(name="tc_state")
def fixture_test_edgepi_tc_state():
    # yield instead of return so local state (i.e mocks) not lost
    # upon returning EdgePiTC object in test functions below
    yield TCState()

@pytest.mark.parametrize(
    "reg_address, data",
    [
        (TCAddresses.CR0_R.value, [TCAddresses.CR0_R.value, 0xFF]),
        (TCAddresses.CR0_W.value, [TCAddresses.CR0_W.value, 0xFF]),
        (TCAddresses.CR1_R.value, [TCAddresses.CR1_R.value, 0xFF]),
        (TCAddresses.CR1_W.value, [TCAddresses.CR1_W.value, 0xFF]),
    ],
)
@patch("edgepi.peripherals.spi.SpiDevice.transfer")
def test_read_register_passes_data(mock_transfer, reg_address, data, tc):
    tc._EdgePiTC__read_register(reg_address)
    mock_transfer.assert_called_once_with(data)


@pytest.mark.parametrize(
    "reg_address, out",
    [
        (TCAddresses.CR0_R.value, [TCAddresses.CR0_R.value, 0x0]),
        (TCAddresses.CR0_W.value, [TCAddresses.CR0_W.value, 0x0]),
        (TCAddresses.CR1_R.value, [TCAddresses.CR1_R.value, 0x3]),
        (TCAddresses.CR1_W.value, [TCAddresses.CR1_W.value, 0x3]),
    ],
)
def test_read_register_returns_data(mocker, reg_address, out, tc):
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", return_value=out)
    out_data = tc._EdgePiTC__read_register(reg_address)
    assert out_data == out


@pytest.mark.parametrize(
    "reg_address, value",
    [
        (TCAddresses.CR0_W.value, 0xFF),
        (TCAddresses.CR1_W.value, 0xFF),
    ],
)
@patch("edgepi.peripherals.spi.SpiDevice.transfer")
def test_write_to_register_passes_data(mock_transfer, reg_address, value, tc):
    tc._EdgePiTC__read_register(reg_address)
    data = [reg_address] + [value]
    mock_transfer.assert_called_once_with(data)


@pytest.mark.parametrize(
    "filter_at_fault, pre_filter_map, expected",
    [
        (
            True,
            {FaultType.OPEN: Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)},
            {},
        ),  # no faults, return only asserting faults
        (
            False,
            {FaultType.OPEN: Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)},
            {FaultType.OPEN: Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)},
        ),  # no faults, return all faults
        (
            True,
            {
                FaultType.OVUV: Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True),
                FaultType.OPEN: Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True),
            },
            {FaultType.OVUV: Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True)},
        ),  # all faults, return only asserting faults
        (
            False,
            {
                FaultType.OVUV: Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True),
                FaultType.OPEN: Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True),
            },
            {
                FaultType.OVUV: Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True),
                FaultType.OPEN: Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True),
            },
        ),  # all faults, return all faults
    ],
)
def test_read_faults_filters(mocker, filter_at_fault, pre_filter_map, expected, tc):
    mocker.patch("edgepi.tc.edgepi_tc.Bits")
    with patch("edgepi.tc.edgepi_tc.map_fault_status", return_value=pre_filter_map):
        result = tc.read_faults(filter_at_fault=filter_at_fault)
        assert result == expected


default_reg_values = {
    TCAddresses.CR0_W.value: 0x0,
    TCAddresses.CR1_W.value: 0x0,
    TCAddresses.MASK_W.value: 0x0,
    TCAddresses.CJHF_W.value: 0x0,
    TCAddresses.CJLF_W.value: 0x0,
    TCAddresses.LTHFTH_W.value: 0x0,
    TCAddresses.LTHFTL_W.value: 0x0,
    TCAddresses.LTLFTH_W.value: 0x0,
    TCAddresses.LTLFTL_W.value: 0x0,
    TCAddresses.CJTO_W.value: 0x0,
    TCAddresses.CJTH_W.value: 0x0,
    TCAddresses.CJTL_W.value: 0x0,
}


@pytest.mark.parametrize(
    "args, set_reg_value, updated_regs",
    [
        (
            {"conversion_mode": ConvMode.SINGLE},
            {TCAddresses.CR0_W.value: 0x80},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"conversion_mode": ConvMode.AUTO},
            None,
            {TCAddresses.CR0_W.value: 0x80},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.HIGH_INPUT_IMPEDANCE},
            None,
            {TCAddresses.CR0_W.value: 0x30},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.MED_INPUT_IMPEDANCE},
            None,
            {TCAddresses.CR0_W.value: 0x20},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.LOW_INPUT_IMPEDANCE},
            None,
            {TCAddresses.CR0_W.value: 0x10},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.DISABLED},
            {TCAddresses.CR0_W.value: 0x10},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"cold_junction_mode": CJMode.DISABLE},
            None,
            {TCAddresses.CR0_W.value: 0x08},
        ),
        (
            {"cold_junction_mode": CJMode.ENABLE},
            {TCAddresses.CR0_W.value: 0x08},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"fault_mode": FaultMode.INTERRUPT},
            None,
            {TCAddresses.CR0_W.value: 0x04},
        ),
        (
            {"fault_mode": FaultMode.COMPARATOR},
            {TCAddresses.CR0_W.value: 0x04},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"noise_filter_mode": NoiseFilterMode.HZ_60},
            {TCAddresses.CR0_W.value: 0x01},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"noise_filter_mode": NoiseFilterMode.HZ_50},
            None,
            {TCAddresses.CR0_W.value: 0x01},
        ),
        (
            {"average_mode": AvgMode.AVG_16},
            None,
            {TCAddresses.CR1_W.value: 0x40},
        ),
        (
            {"average_mode": AvgMode.AVG_8},
            None,
            {TCAddresses.CR1_W.value: 0x30},
        ),
        (
            {"average_mode": AvgMode.AVG_4},
            None,
            {TCAddresses.CR1_W.value: 0x20},
        ),
        (
            {"average_mode": AvgMode.AVG_2},
            None,
            {TCAddresses.CR1_W.value: 0x10},
        ),
        (
            {"average_mode": AvgMode.AVG_1},
            {TCAddresses.CR1_W.value: 0x10},
            {TCAddresses.CR1_W.value: 0x00},
        ),
        (
            {"tc_type": TCType.TYPE_B},
            None,
            {TCAddresses.CR1_W.value: 0x00},
        ),
        (
            {"tc_type": TCType.TYPE_E},
            None,
            {TCAddresses.CR1_W.value: 0x01},
        ),
        (
            {"tc_type": TCType.TYPE_J},
            None,
            {TCAddresses.CR1_W.value: 0x02},
        ),
        (
            {"tc_type": TCType.TYPE_K},
            None,
            {TCAddresses.CR1_W.value: 0x03},
        ),
        (
            {"tc_type": TCType.TYPE_N},
            None,
            {TCAddresses.CR1_W.value: 0x04},
        ),
        (
            {"tc_type": TCType.TYPE_R},
            None,
            {TCAddresses.CR1_W.value: 0x05},
        ),
        (
            {"tc_type": TCType.TYPE_S},
            None,
            {TCAddresses.CR1_W.value: 0x06},
        ),
        (
            {"tc_type": TCType.TYPE_T},
            None,
            {TCAddresses.CR1_W.value: 0x07},
        ),
        (
            {"voltage_mode": VoltageMode.GAIN_8},
            None,
            {TCAddresses.CR1_W.value: 0x08},
        ),
        (
            {"voltage_mode": VoltageMode.GAIN_32},
            None,
            {TCAddresses.CR1_W.value: 0x0C},
        ),
        (
            {"cj_high_mask": CJHighMask.CJHIGH_MASK_OFF},
            {TCAddresses.MASK_W.value: 0x20},
            {TCAddresses.MASK_W.value: 0x00},
        ),
        (
            {"cj_high_mask": CJHighMask.CJHIGH_MASK_ON},
            None,
            {TCAddresses.MASK_W.value: 0x20},
        ),
        (
            {"cj_low_mask": CJLowMask.CJLOW_MASK_OFF},
            {TCAddresses.MASK_W.value: 0x10},
            {TCAddresses.MASK_W.value: 0x00},
        ),
        (
            {"cj_low_mask": CJLowMask.CJLOW_MASK_ON},
            None,
            {TCAddresses.MASK_W.value: 0x10},
        ),
        (
            {"tc_high_mask": TCHighMask.TCHIGH_MASK_OFF},
            {TCAddresses.MASK_W.value: 0x08},
            {TCAddresses.MASK_W.value: 0x00},
        ),
        (
            {"tc_high_mask": TCHighMask.TCHIGH_MASK_ON},
            None,
            {TCAddresses.MASK_W.value: 0x08},
        ),
        (
            {"tc_low_mask": TCLowMask.TCLOW_MASK_OFF},
            {TCAddresses.MASK_W.value: 0x04},
            {TCAddresses.MASK_W.value: 0x00},
        ),
        (
            {"tc_low_mask": TCLowMask.TCLOW_MASK_ON},
            None,
            {TCAddresses.MASK_W.value: 0x04},
        ),
        (
            {"ovuv_mask": OvuvMask.OVUV_MASK_OFF},
            {TCAddresses.MASK_W.value: 0x02},
            {TCAddresses.MASK_W.value: 0x00},
        ),
        (
            {"ovuv_mask": OvuvMask.OVUV_MASK_ON},
            None,
            {TCAddresses.MASK_W.value: 0x02},
        ),
        (
            {"open_mask": OpenMask.OPEN_MASK_OFF},
            {TCAddresses.MASK_W.value: 0x01},
            {TCAddresses.MASK_W.value: 0x00},
        ),
        (
            {"open_mask": OpenMask.OPEN_MASK_ON},
            None,
            {TCAddresses.MASK_W.value: 0x01},
        ),
        (
            {"cj_high_threshold": 100},
            {TCAddresses.CR1_W.value: 0x03},
            {TCAddresses.CJHF_W.value: 0x64},
        ),
        ({"cj_low_threshold": -16}, None, {TCAddresses.CJLF_W.value: 0x90}),
        (
            {"lt_high_threshold": 1000, "lt_high_threshold_decimals": DecBits4.P0_9375},
            {TCAddresses.CR1_W.value: 0x03},
            {TCAddresses.LTHFTH_W.value: 0x3E, TCAddresses.LTHFTL_W.value: 0x8F},
        ),
        (
            {"lt_low_threshold": -55, "lt_low_threshold_decimals": DecBits4.P0_9375},
            {TCAddresses.CR1_W.value: 0x03},
            {TCAddresses.LTLFTH_W.value: 0x83, TCAddresses.LTLFTL_W.value: 0x7F},
        ),
        (
            {"cj_offset": 4, "cj_offset_decimals": DecBits4.P0_9375},
            {TCAddresses.CR1_W.value: 0x03},
            {
                TCAddresses.CJTO_W.value: 0x4F,
            },
        ),
        (
            {"cj_temp": 100, "cj_temp_decimals": DecBits6.P0_984375},
            {TCAddresses.CR1_W.value: 0x03},
            {TCAddresses.CJTH_W.value: 0x64, TCAddresses.CJTL_W.value: 0xFC},
        ),
    ],
)
def test_set_config(mocker, args, set_reg_value, updated_regs, tc):
    # need to deepcopy in order to keep default_reg_values unaltered between test cases
    start_values = deepcopy(default_reg_values)

    # if needed, modify default register values for this test case
    if set_reg_value is not None:
        for addx, value in set_reg_value.items():
            start_values[addx] = value

    # need 2nd deepcopy for comparing updated values to start values below
    # otherwise, the modification of values above is counted as an update
    # i.e. keep start_values unaltered by code below
    reg_values = deepcopy(start_values)

    # insert mock register values -- set_config will update these with opcodes below
    mocker.patch(
        "edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__read_registers_to_map", return_value=reg_values
    )
    # mocked out SPI, so it can't read tc_type: need to return it manually
    mocker.patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__get_tc_type", return_value=TCType.TYPE_K)

    tc.set_config(**args)

    for addx, entry in reg_values.items():
        # check registers not updated have not been changed
        if addx not in updated_regs:
            assert not entry["is_changed"]
            assert entry["value"] == start_values[addx]
        # check updates were applied
        else:
            assert reg_values[addx]["value"] == updated_regs[addx]
            assert reg_values[addx]["is_changed"]


@pytest.mark.parametrize(
    "reg_values",
    [
        ({TCAddresses.CR0_W.value: {"is_changed": True, "value": 0xFF}}),
        (
            {
                TCAddresses.CR0_W.value: {"is_changed": True, "value": 0xFF},
                TCAddresses.CR1_W.value: {"is_changed": True, "value": 0xFF},
            }
        ),
        ({TCAddresses.CR0_W.value: {"is_changed": False, "value": 0xFF}}),
        (
            {
                TCAddresses.CR0_W.value: {"is_changed": True, "value": 0xFF},
                TCAddresses.CR1_W.value: {"is_changed": True, "value": 0xFF},
            }
        ),
        (
            {
                TCAddresses.CR0_W.value: {"is_changed": True, "value": 0xFF},
                TCAddresses.CR1_W.value: {"is_changed": True, "value": 0xFF},
                TCAddresses.CJHF_W.value: {"is_changed": False, "value": 0x0},
            }
        ),
    ],
)
@patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__write_to_register")
def test_update_registers_from_dict(mock_write, reg_values, tc):
    # construct list of expected calls to __write_to_register
    write_calls = []
    for addx, entry in reg_values.items():
        if entry["is_changed"]:
            write_calls.append(call(addx, entry["value"]))

    tc._EdgePiTC__update_registers_from_dict(reg_values)

    # assert __write_to_register called with expected calls
    mock_write.assert_has_calls(write_calls, any_order=True)


@pytest.mark.parametrize(
    "cj_temp, cj_temp_decimals",
    [
        (-50, DecBits4.P0_125),
        (-50, DecBits4.P0_125),
    ],
)
def test_overwrite_cold_junction_temp(cj_temp, cj_temp_decimals, tc):
    with patch("edgepi.tc.edgepi_tc.EdgePiTC.set_config") as mock_set_config:
        tc.overwrite_cold_junction_temp(cj_temp, cj_temp_decimals)
        args = {"cj_temp": cj_temp, "cj_temp_decimals": cj_temp_decimals}
        mock_set_config.assert_called_once_with(**args)


@pytest.mark.parametrize(
    "cr0_val, cmd",
    [
        (0x00, 0x40),
        (0b10111101, 0b11111101),
    ],
)
def test_single_sample(mocker, cr0_val, cmd, tc):
    mocker.patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__read_register", return_value=[0, cr0_val])
    mocker.patch("edgepi.tc.edgepi_tc.calc_conv_time", return_value=200)
    with patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__write_to_register") as mock_write:
        tc.single_sample()
        mock_write.assert_called_once_with(TCAddresses.CR0_W.value, cmd)


@pytest.mark.parametrize(
    "cr0_val, cmd",
    [
        (0x00, 0x02),
        (0b10111101, 0b10111111),
    ],
)
def test_clear_faults(mocker, cr0_val, cmd, tc):
    mocker.patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__read_register", return_value=[0, cr0_val])
    with patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__write_to_register") as mock_write:
        tc.clear_faults()
        mock_write.assert_called_once_with(TCAddresses.CR0_W.value, cmd)


@pytest.mark.parametrize(
    "cr1_val, tc_type",
    [
        (0x00, TCType.TYPE_B),
        (0x01, TCType.TYPE_E),
        (0x02, TCType.TYPE_J),
        (0x03, TCType.TYPE_K),
        (0x04, TCType.TYPE_N),
        (0x05, TCType.TYPE_R),
        (0x06, TCType.TYPE_S),
        (0x07, TCType.TYPE_T),
        (0xFF, None),
    ],
)
def test_get_tc_type(mocker, cr1_val, tc_type):
    # not using fixture because need Bits not mocked here
    mocker.patch("edgepi.peripherals.spi.SPI")
    tc = EdgePiTC()
    mocker.patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__read_register", return_value=[0, cr1_val])
    assert tc._EdgePiTC__get_tc_type() == tc_type


@patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__write_to_register")
def test_tc_reset_registers(mock_write, tc):
    write_calls = [call(addx, value) for addx, value in tc.default_reg_values.items()]
    tc.reset_registers()
    mock_write.assert_has_calls(write_calls, any_order=True)

def test_tc_state_init(tc):
    assert tc.tc_state.cmode is None
    assert tc.tc_state.one_shot is None
    assert tc.tc_state.open_circuit_fault is None
    assert tc.tc_state.cold_junction is None
    assert tc.tc_state.fault is None
    assert tc.tc_state.fault_clr is None
    assert tc.tc_state.noise_rejection is None
    assert tc.tc_state.sampling_average is None
    assert tc.tc_state.tc_type is None

@pytest.mark.parametrize(
    "cr_val, state_mask, state_expected",
    [
        # TC Type Test
        (0x00, Masks.CR1_HIGH_MASK.value, TCType.TYPE_B),
        (0x01, Masks.CR1_HIGH_MASK.value, TCType.TYPE_E),
        (0x02, Masks.CR1_HIGH_MASK.value, TCType.TYPE_J),
        (0x03, Masks.CR1_HIGH_MASK.value, TCType.TYPE_K),
        (0x04, Masks.CR1_HIGH_MASK.value, TCType.TYPE_N),
        (0x05, Masks.CR1_HIGH_MASK.value, TCType.TYPE_R),
        (0x06, Masks.CR1_HIGH_MASK.value, TCType.TYPE_S),
        (0x07, Masks.CR1_HIGH_MASK.value, TCType.TYPE_T),
        (0xFF, Masks.CR1_HIGH_MASK.value, None),
        (0x00, Masks.CR1_HIGH_MASK.value, TCType.TYPE_B),
        (0xF1, Masks.CR1_HIGH_MASK.value, TCType.TYPE_E),
        (0xF2, Masks.CR1_HIGH_MASK.value, TCType.TYPE_J),
        (0xF3, Masks.CR1_HIGH_MASK.value, TCType.TYPE_K),
        (0xF4, Masks.CR1_HIGH_MASK.value, TCType.TYPE_N),
        (0xF5, Masks.CR1_HIGH_MASK.value, TCType.TYPE_R),
        (0xF6, Masks.CR1_HIGH_MASK.value, TCType.TYPE_S),
        (0xF7, Masks.CR1_HIGH_MASK.value, TCType.TYPE_T),
        (0xFF, Masks.CR1_HIGH_MASK.value, None),
        # Ave Sample Mask
        (0x00, Masks.CR1_LOW_MASK.value, AvgMode.AVG_1),
        (0x10, Masks.CR1_LOW_MASK.value, AvgMode.AVG_2),
        (0x20, Masks.CR1_LOW_MASK.value, AvgMode.AVG_4),
        (0x30, Masks.CR1_LOW_MASK.value, AvgMode.AVG_8),
        (0x40, Masks.CR1_LOW_MASK.value, AvgMode.AVG_16),
        (0xFF, Masks.CR1_LOW_MASK.value, None),
        (0x0F, Masks.CR1_LOW_MASK.value, AvgMode.AVG_1),
        (0x1F, Masks.CR1_LOW_MASK.value, AvgMode.AVG_2),
        (0x2F, Masks.CR1_LOW_MASK.value, AvgMode.AVG_4),
        (0x3F, Masks.CR1_LOW_MASK.value, AvgMode.AVG_8),
        (0x4F, Masks.CR1_LOW_MASK.value, AvgMode.AVG_16)
    ],
)
def test__tc_get_state(cr_val, state_mask, state_expected, tc_state):
    result = tc_state._TCState__tc_get_state(cr_val,state_mask)
    assert result == state_expected

@pytest.mark.parametrize(
    "cr_val, state_mask, state_expected",
    [
        # (0xFF, [True, True, True, True, True]),
        # (0x7F, [False, True, True, True, True]),
        # (0x3F, [False, False, True, True, True]),
        # (0x0F, [False, False, True, True, True]),
        # (0x07, [False, False, False, True, True]),
        # (0x03, [False, False, False, False, True]),
        # (0x01, [False, False, False, False, True]),
        # (0x00, [False, False, False, False, False]),

        (0xFF, ConvMode.AUTO.value.op_code, True),
        (0x7F, ConvMode.AUTO.value.op_code, False),
        (0x7F, TCOps.SINGLE_SHOT.value.op_code, True),
        (0x3F, TCOps.SINGLE_SHOT.value.op_code, False),
        (0x0F, CJMode.DISABLE.value.op_code, True),
        (0x07, CJMode.DISABLE.value.op_code, False),
        (0x07, FaultMode.INTERRUPT.value.op_code, True),
        (0x03, FaultMode.INTERRUPT.value.op_code, False),
        (0x01, NoiseFilterMode.HZ_50.value.op_code, True),
        (0x00, NoiseFilterMode.HZ_50.value.op_code, False),
    ],
)
def test__tc_get_state_bool(cr_val, state_mask, state_expected, tc_state):
    result = tc_state._TCState__tc_get_state_bool(cr_val,state_mask)
    assert result == state_expected


@pytest.mark.parametrize(
    "cr_val, state_expected",
    [
        ([0xFF, 0xFF], [True, True, True, True, True, None, None]),
        ([0x7F, 0xFF], [False, True, True, True, True, None, None]),
        ([0x3F, 0xFF], [False, False, True, True, True, None, None]),
        ([0x0F, 0xFF], [False, False, True, True, True, None, None]),
        ([0x07, 0xFF], [False, False, False, True, True, None, None]),
        ([0x03, 0xFF], [False, False, False, False, True, None, None]),
        ([0x01, 0xFF], [False, False, False, False, True, None, None]),
        ([0x00, 0xFF], [False, False, False, False, False, None, None]),

        ([0xFF, 0x7F], [True, True, True, True, True, None, None]),
        ([0xFF, 0x4F], [True, True, True, True, True, AvgMode.AVG_16, None]),
        ([0x7F, 0x3F], [False, True, True, True, True, AvgMode.AVG_8, None]),
        ([0x3F, 0x2F], [False, False, True, True, True, AvgMode.AVG_4, None]),
        ([0x0F, 0x1F], [False, False, True, True, True, AvgMode.AVG_2, None]),
        ([0x07, 0x0F], [False, False, False, True, True, AvgMode.AVG_1, None]),
        ([0x03, 0x07], [False, False, False, False, True, AvgMode.AVG_1, TCType.TYPE_T]),
        ([0x01, 0x03], [False, False, False, False, True, AvgMode.AVG_1, TCType.TYPE_K]),
        ([0x00, 0x01], [False, False, False, False, False, AvgMode.AVG_1, TCType.TYPE_E]),
        ([0x00, 0x00], [False, False, False, False, False, AvgMode.AVG_1, TCType.TYPE_B]),
    ],
)
def test_tc_update_state(cr_val, state_expected, tc_state):
    tc_state.tc_update_state(cr_val)
    assert tc_state.cmode == state_expected[0]
    assert tc_state.one_shot == state_expected[1]
    assert tc_state.cold_junction == state_expected[2]
    assert tc_state.fault == state_expected[3]
    assert tc_state.noise_rejection == state_expected[4]
    assert tc_state.sampling_average == state_expected[5]
    assert tc_state.tc_type == state_expected[6]


@pytest.mark.parametrize(
    "cr_val, state_expected",
    [
        ([0x2f, 0xFF, 0xFF], [True, True, True, True, True, None, None]),
        ([0x2f, 0x7F, 0xFF], [False, True, True, True, True, None, None]),
        ([0x2f, 0x3F, 0xFF], [False, False, True, True, True, None, None]),
        ([0x2f, 0x0F, 0xFF], [False, False, True, True, True, None, None]),
        ([0x2f, 0x07, 0xFF], [False, False, False, True, True, None, None]),
        ([0x2f, 0x03, 0xFF], [False, False, False, False, True, None, None]),
        ([0x2f, 0x01, 0xFF], [False, False, False, False, True, None, None]),
        ([0x2f, 0x00, 0xFF], [False, False, False, False, False, None, None]),

        ([0x2f, 0xFF, 0x7F], [True, True, True, True, True, None, None]),
        ([0x2f, 0xFF, 0x4F], [True, True, True, True, True, AvgMode.AVG_16, None]),
        ([0x2f, 0x7F, 0x3F], [False, True, True, True, True, AvgMode.AVG_8, None]),
        ([0x2f, 0x3F, 0x2F], [False, False, True, True, True, AvgMode.AVG_4, None]),
        ([0x2f, 0x0F, 0x1F], [False, False, True, True, True, AvgMode.AVG_2, None]),
        ([0x2f, 0x07, 0x0F], [False, False, False, True, True, AvgMode.AVG_1, None]),
        ([0x2f, 0x03, 0x07], [False, False, False, False, True, AvgMode.AVG_1, TCType.TYPE_T]),
        ([0x2f, 0x01, 0x03], [False, False, False, False, True, AvgMode.AVG_1, TCType.TYPE_K]),
        ([0x2f, 0x00, 0x01], [False, False, False, False, False, AvgMode.AVG_1, TCType.TYPE_E]),
        ([0x2f, 0x00, 0x00], [False, False, False, False, False, AvgMode.AVG_1, TCType.TYPE_B]),
    ],
)
def test_get_state(mocker, cr_val, state_expected, tc):
    mocker.patch("edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__read_registers", return_value=cr_val)
    tc.get_state()
    assert tc.tc_state.cmode == state_expected[0]
    assert tc.tc_state.one_shot == state_expected[1]
    assert tc.tc_state.cold_junction == state_expected[2]
    assert tc.tc_state.fault == state_expected[3]
    assert tc.tc_state.noise_rejection == state_expected[4]
    assert tc.tc_state.sampling_average == state_expected[5]
    assert tc.tc_state.tc_type == state_expected[6]
