"""
Hardware-dependent integration tests for thermocouple module

Hardware Requirements:
- SPI capable device
- MAX31856 thermocouple chip connected

- if using SPI device tree overlay - SPI interface disabled
- else, SPI interface enabled
"""

import pytest

from edgepi.tc.edgepi_tc import EdgePiTC
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
    OpenCircuitMode,
    OpenMask,
    OvuvMask,
    TCAddresses,
    TCHighMask,
    TCLowMask,
    TCType,
    VoltageMode,
)
from edgepi.tc.tc_faults import FaultType


def test_tc_init():
    tc = EdgePiTC()
    assert tc.devpath == f"/dev/spidev{6}.{2}"


@pytest.fixture(name="tc")
def fixture_test_edgepi_tc():
    return EdgePiTC()


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
            {TCAddresses.CR1_W.value: 0x43},
        ),
        (
            {"average_mode": AvgMode.AVG_8},
            None,
            {TCAddresses.CR1_W.value: 0x33},
        ),
        (
            {"average_mode": AvgMode.AVG_4},
            None,
            {TCAddresses.CR1_W.value: 0x23},
        ),
        (
            {"average_mode": AvgMode.AVG_2},
            None,
            {TCAddresses.CR1_W.value: 0x13},
        ),
        (
            {"average_mode": AvgMode.AVG_1},
            {TCAddresses.CR1_W.value: 0x13},
            {TCAddresses.CR1_W.value: 0x03},
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
            None,
            {TCAddresses.MASK_W.value: 0xDF},
        ),
        (
            {"cj_high_mask": CJHighMask.CJHIGH_MASK_ON},
            {TCAddresses.MASK_W.value: 0xDF},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"cj_low_mask": CJLowMask.CJLOW_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xEF},
        ),
        (
            {"cj_low_mask": CJLowMask.CJLOW_MASK_ON},
            {TCAddresses.MASK_W.value: 0xEF},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"tc_high_mask": TCHighMask.TCHIGH_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xF7},
        ),
        (
            {"tc_high_mask": TCHighMask.TCHIGH_MASK_ON},
            {TCAddresses.MASK_W.value: 0xF7},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"tc_low_mask": TCLowMask.TCLOW_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xFB},
        ),
        (
            {"tc_low_mask": TCLowMask.TCLOW_MASK_ON},
            {TCAddresses.MASK_W.value: 0xFB},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"ovuv_mask": OvuvMask.OVUV_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xFD},
        ),
        (
            {"ovuv_mask": OvuvMask.OVUV_MASK_ON},
            {TCAddresses.MASK_W.value: 0xFD},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"open_mask": OpenMask.OPEN_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xFE},
        ),
        (
            {"open_mask": OpenMask.OPEN_MASK_ON},
            {TCAddresses.MASK_W.value: 0xFE},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"cj_high_threshold": 100},
            None,
            {TCAddresses.CJHF_W.value: 0x64},
        ),
        ({"cj_low_threshold": -16}, None, {TCAddresses.CJLF_W.value: 0x90}),
        (
            {"lt_high_threshold": 1000, "lt_high_threshold_decimals": DecBits4.P0_9375},
            None,
            {TCAddresses.LTHFTH_W.value: 0x3E, TCAddresses.LTHFTL_W.value: 0x8F},
        ),
        (
            {"lt_low_threshold": -55, "lt_low_threshold_decimals": DecBits4.P0_9375},
            None,
            {TCAddresses.LTLFTH_W.value: 0x83, TCAddresses.LTLFTL_W.value: 0x7F},
        ),
        (
            {"cj_offset": 4, "cj_offset_decimals": DecBits4.P0_9375},
            None,
            {TCAddresses.CJTO_W.value: 0x4F},
        ),
        (
            {"cj_temp": 100, "cj_temp_decimals": DecBits6.P0_984375},
            {TCAddresses.CR0_W.value: 0x08},  # disable cold junction sensor
            {TCAddresses.CJTH_W.value: 0x64, TCAddresses.CJTL_W.value: 0xFC},
        ),
    ],
)
def test_set_config(tc, args, set_reg_value, updated_regs):
    # pylint: disable=protected-access

    # reset registers to default values
    tc.reset_registers()

    # modify default values for this test only if needed
    if set_reg_value is not None:
        for addx, value in set_reg_value.items():
            tc._EdgePiTC__write_to_register(addx, value)

    # update registers with user args
    tc.set_config(**args)

    # if overwriting cold junction temp, re-enable sensing to return
    # CR0 to default value for value comparison below
    if "cj_temp" in args.keys() or "cj_temp_decimals" in args.keys():
        tc.set_config(cold_junction_mode=CJMode.ENABLE)

    # read updated register values
    reg_values = tc._EdgePiTC__read_registers_to_map()

    # compare to expected register values
    for addx, value in reg_values.items():
        # these require cold-junction sensor to be disabled, otherwise
        # they are continously updated and cannot be tested against default values
        if addx in (TCAddresses.CJTH_W.value, TCAddresses.CJTL_W.value):
            continue

        # check registers not updated have not been changed
        if addx not in updated_regs:
            assert value == tc.default_reg_values[addx]
        # check updates were applied
        else:
            assert value == updated_regs[addx]


def test_single_sample(tc):
    temps = tc.single_sample()
    assert len(temps) == 2
    for temp in temps:
        assert isinstance(temp, float)
        assert temp != 0


@pytest.mark.parametrize(
    "threshold_args, fault_names, filter_at_fault, num_faults",
    [
        ({"cj_high_threshold": 1}, [FaultType.CJHIGH], False, 8),
        ({"cj_high_threshold": 1}, [FaultType.CJHIGH], True, 1),
        ({"cj_low_threshold": 100}, [FaultType.CJLOW], True, 1),
        (
            {"cj_high_threshold": 1, "cj_low_threshold": 100},
            [FaultType.CJHIGH, FaultType.CJLOW],
            True,
            2,
        ),
        ({"cj_low_threshold": 100}, [FaultType.CJLOW], True, 1),
        (
            {"cj_high_threshold": 1, "cj_low_threshold": 100},
            [FaultType.CJHIGH, FaultType.CJLOW],
            False,
            8,
        ),
        (
            {"lt_high_threshold": 1, "lt_high_threshold_decimals": DecBits4.P0_25},
            [FaultType.TCHIGH],
            True,
            1,
        ),
        (
            {
                "lt_high_threshold": 1,
                "lt_high_threshold_decimals": DecBits4.P0_25,
                "lt_low_threshold": 100,
                "lt_low_threshold_decimals": DecBits4.P0_25,
            },
            [FaultType.TCHIGH, FaultType.TCLOW, FaultType.TCRANGE],
            True,
            2,
        ),
        (
            {
                "lt_high_threshold": 1,
                "lt_high_threshold_decimals": DecBits4.P0_25,
                "lt_low_threshold": 100,
                "lt_low_threshold_decimals": DecBits4.P0_25,
                "cj_high_threshold": 1,
                "cj_low_threshold": 100,
            },
            [
                FaultType.CJHIGH,
                FaultType.CJLOW,
                FaultType.TCHIGH,
                FaultType.TCLOW,
                FaultType.TCRANGE,
            ],
            True,
            4,
        ),
    ],
)
def test_read_faults(threshold_args, fault_names, filter_at_fault, num_faults, tc):
    tc.set_config(**threshold_args)
    tc.single_sample()
    faults = tc.read_faults(filter_at_fault)
    assert len(faults) == num_faults
    for key, fault in faults.items():
        if key in fault_names:
            assert fault.at_fault
        else:
            assert not fault.at_fault
    tc.reset_registers()
