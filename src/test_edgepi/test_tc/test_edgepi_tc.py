"""tests for edgepi_tc module"""


from copy import deepcopy
from unittest.mock import call, patch

import pytest
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import (
    AvgMode,
    CJMode,
    ConvMode,
    DecBits4,
    DecBits6,
    FaultMode,
    NoiseFilterMode,
    OpenCircuitMode,
    TCAddresses,
    TCType,
)
from edgepi.tc.tc_faults import FaultMsg, FaultType, Fault

# pylint: disable=protected-access


@pytest.fixture(name="tc")
def fixture_test_edgepi_tc(mocker):
    # mocker acts as context manager
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.tc.edgepi_tc.Bits")
    yield EdgePiTC()


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
    # insert mock register values -- set_config will update these with opcodes
    start_values = deepcopy(default_reg_values)

    # if needed, set default register value to another value
    if set_reg_value is not None:
        for addx, value in set_reg_value.items():
            start_values[addx] = value

    # needed for comparing updated values to start values below
    # otherwise, the modification of values above is counted as an update
    reg_values = deepcopy(start_values)

    mocker.patch(
        "edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__read_registers_to_map", return_value=reg_values
    )
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
