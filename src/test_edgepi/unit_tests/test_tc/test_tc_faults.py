'''unit tests for tc_faults.py module'''

import pytest
from bitstring import Bits
from edgepi.tc.tc_faults import map_fault_status, Fault, FaultMsg, FaultType


@pytest.mark.parametrize(
    "fault_bits, mask_bits, expected",
    [
        (
            Bits("0xFF"),
            Bits("0xFF"),
            {
                FaultType.CJRANGE: Fault(
                    FaultType.CJRANGE,
                    FaultMsg.CJRANGE_BAD_MSG,
                    at_fault=True,
                    is_masked=True,
                ),
                FaultType.TCRANGE: Fault(
                    FaultType.TCRANGE,
                    FaultMsg.TCRANGE_BAD_MSG,
                    at_fault=True,
                    is_masked=True,
                ),
                FaultType.CJHIGH: Fault(
                    FaultType.CJHIGH,
                    FaultMsg.CJHIGH_BAD_MSG,
                    at_fault=True,
                    is_masked=True,
                ),
                FaultType.CJLOW: Fault(
                    FaultType.CJLOW,
                    FaultMsg.CJLOW_BAD_MSG,
                    at_fault=True,
                    is_masked=True,
                ),
                FaultType.TCHIGH: Fault(
                    FaultType.TCHIGH,
                    FaultMsg.TCHIGH_BAD_MSG,
                    at_fault=True,
                    is_masked=True,
                ),
                FaultType.TCLOW: Fault(
                    FaultType.TCLOW,
                    FaultMsg.TCLOW_BAD_MSG,
                    at_fault=True,
                    is_masked=True,
                ),
                FaultType.OVUV: Fault(
                    FaultType.OVUV, FaultMsg.OVUV_BAD_MSG, at_fault=True, is_masked=True
                ),
                FaultType.OPEN: Fault(
                    FaultType.OPEN, FaultMsg.OPEN_BAD_MSG, at_fault=True, is_masked=True
                ),
            },
        ),  # all faults, all masks
        (
            Bits("0x00"),
            Bits("0xFF"),
            {
                FaultType.CJRANGE: Fault(
                    FaultType.CJRANGE, FaultMsg.CJRANGE_OK_MSG, is_masked=True
                ),
                FaultType.TCRANGE: Fault(
                    FaultType.TCRANGE, FaultMsg.TCRANGE_OK_MSG, is_masked=True
                ),
                FaultType.CJHIGH: Fault(
                    FaultType.CJHIGH, FaultMsg.CJHIGH_OK_MSG, is_masked=True
                ),
                FaultType.CJLOW: Fault(
                    FaultType.CJLOW, FaultMsg.CJLOW_OK_MSG, is_masked=True
                ),
                FaultType.TCHIGH: Fault(
                    FaultType.TCHIGH, FaultMsg.TCHIGH_OK_MSG, is_masked=True
                ),
                FaultType.TCLOW: Fault(
                    FaultType.TCLOW, FaultMsg.TCLOW_OK_MSG, is_masked=True
                ),
                FaultType.OVUV: Fault(
                    FaultType.OVUV, FaultMsg.OVUV_OK_MSG, is_masked=True
                ),
                FaultType.OPEN: Fault(
                    FaultType.OPEN, FaultMsg.OPEN_OK_MSG, is_masked=True
                ),
            },
        ),  # no faults, all masks
        (
            Bits("0x00"),
            Bits("0x00"),
            {
                FaultType.CJRANGE: Fault(
                    FaultType.CJRANGE, FaultMsg.CJRANGE_OK_MSG, is_masked=False
                ),
                FaultType.TCRANGE: Fault(
                    FaultType.TCRANGE, FaultMsg.TCRANGE_OK_MSG, is_masked=False
                ),
                FaultType.CJHIGH: Fault(
                    FaultType.CJHIGH, FaultMsg.CJHIGH_OK_MSG, is_masked=False
                ),
                FaultType.CJLOW: Fault(
                    FaultType.CJLOW, FaultMsg.CJLOW_OK_MSG, is_masked=False
                ),
                FaultType.TCHIGH: Fault(
                    FaultType.TCHIGH, FaultMsg.TCHIGH_OK_MSG, is_masked=False
                ),
                FaultType.TCLOW: Fault(
                    FaultType.TCLOW, FaultMsg.TCLOW_OK_MSG, is_masked=False
                ),
                FaultType.OVUV: Fault(
                    FaultType.OVUV, FaultMsg.OVUV_OK_MSG, is_masked=False
                ),
                FaultType.OPEN: Fault(
                    FaultType.OPEN, FaultMsg.OPEN_OK_MSG, is_masked=False
                ),
            },
        ),  # no faults, no masks
        (
            Bits("0xFF"),
            Bits("0x00"),
            {
                FaultType.CJRANGE: Fault(
                    FaultType.CJRANGE,
                    FaultMsg.CJRANGE_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
                FaultType.TCRANGE: Fault(
                    FaultType.TCRANGE,
                    FaultMsg.TCRANGE_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
                FaultType.CJHIGH: Fault(
                    FaultType.CJHIGH,
                    FaultMsg.CJHIGH_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
                FaultType.CJLOW: Fault(
                    FaultType.CJLOW,
                    FaultMsg.CJLOW_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
                FaultType.TCHIGH: Fault(
                    FaultType.TCHIGH,
                    FaultMsg.TCHIGH_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
                FaultType.TCLOW: Fault(
                    FaultType.TCLOW,
                    FaultMsg.TCLOW_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
                FaultType.OVUV: Fault(
                    FaultType.OVUV,
                    FaultMsg.OVUV_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
                FaultType.OPEN: Fault(
                    FaultType.OPEN,
                    FaultMsg.OPEN_BAD_MSG,
                    at_fault=True,
                    is_masked=False,
                ),
            },
        ),  # all faults, no masks
    ],
)
def test_map_fault_status(fault_bits, mask_bits, expected):
    out = map_fault_status(fault_bits, mask_bits)
    assert out == expected
