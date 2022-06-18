import pytest
from bitstring import Bits
from edgepi.tc.tc_faults import map_fault_status, Faults, Fault, FaultMsg
from edgepi.tc.tc_constants import TCFaults

@pytest.mark.parametrize('fault_bits, mask_bits, expected', [
    (Bits('0xFF'), Bits('0xFF'),
        {
            TCFaults.CJRANGE: Faults.CJRANGE_BAD.value,
            TCFaults.TCRANGE: Faults.TCRANGE_BAD.value,
            TCFaults.CJHIGH: Faults.CJHIGH_BAD.value,
            TCFaults.CJLOW: Faults.CJLOW_BAD.value,
            TCFaults.TCHIGH: Faults.TCHIGH_BAD.value,
            TCFaults.TCLOW: Faults.TCLOW_BAD.value,
            TCFaults.OVUV: Faults.OVUV_BAD.value,
            TCFaults.OPEN: Faults.OPEN_BAD.value
        }
    ),   # all faults, all masks
    (Bits('0x00'), Bits('0xFF'),
        {
            TCFaults.CJRANGE: Faults.CJRANGE_OK.value,
            TCFaults.TCRANGE: Faults.TCRANGE_OK.value,
            TCFaults.CJHIGH: Faults.CJHIGH_OK.value,
            TCFaults.CJLOW: Faults.CJLOW_OK.value,
            TCFaults.TCHIGH: Faults.TCHIGH_OK.value,
            TCFaults.TCLOW: Faults.TCLOW_OK.value,
            TCFaults.OVUV: Faults.OVUV_OK.value,
            TCFaults.OPEN: Faults.OPEN_OK.value
        }
    ),   # no faults, all masks
    (Bits('0x00'), Bits('0x00'),
        {
            TCFaults.CJRANGE: Fault(TCFaults.CJRANGE, FaultMsg.CJRANGE_OK_MSG, is_masked=False),
            TCFaults.TCRANGE: Fault(TCFaults.TCRANGE, FaultMsg.TCRANGE_OK_MSG, is_masked=False),
            TCFaults.CJHIGH: Fault(TCFaults.CJHIGH, FaultMsg.CJHIGH_OK_MSG, is_masked=False),
            TCFaults.CJLOW: Fault(TCFaults.CJLOW, FaultMsg.CJLOW_OK_MSG, is_masked=False),
            TCFaults.TCHIGH: Fault(TCFaults.TCHIGH, FaultMsg.TCHIGH_OK_MSG, is_masked=False),
            TCFaults.TCLOW: Fault(TCFaults.TCLOW, FaultMsg.TCLOW_OK_MSG, is_masked=False),
            TCFaults.OVUV: Fault(TCFaults.OVUV, FaultMsg.OVUV_OK_MSG, is_masked=False),
            TCFaults.OPEN: Fault(TCFaults.OPEN, FaultMsg.OPEN_OK_MSG, is_masked=False)
        }
    ),   # no faults, no masks
    (Bits('0xFF'), Bits('0x00'),
        {
            TCFaults.CJRANGE: Fault(TCFaults.CJRANGE, FaultMsg.CJRANGE_BAD_MSG, at_fault=True, is_masked=False),
            TCFaults.TCRANGE: Fault(TCFaults.TCRANGE, FaultMsg.TCRANGE_BAD_MSG, at_fault=True, is_masked=False),
            TCFaults.CJHIGH: Fault(TCFaults.CJHIGH, FaultMsg.CJHIGH_BAD_MSG, at_fault=True, is_masked=False),
            TCFaults.CJLOW: Fault(TCFaults.CJLOW, FaultMsg.CJLOW_BAD_MSG, at_fault=True, is_masked=False),
            TCFaults.TCHIGH: Fault(TCFaults.TCHIGH, FaultMsg.TCHIGH_BAD_MSG, at_fault=True, is_masked=False),
            TCFaults.TCLOW: Fault(TCFaults.TCLOW, FaultMsg.TCLOW_BAD_MSG, at_fault=True, is_masked=False),
            TCFaults.OVUV: Fault(TCFaults.OVUV, FaultMsg.OVUV_BAD_MSG, at_fault=True, is_masked=False),
            TCFaults.OPEN: Fault(TCFaults.OPEN, FaultMsg.OPEN_BAD_MSG, at_fault=True, is_masked=False)
        }
    ),   # all faults, no masks
])
def test_map_fault_status(fault_bits, mask_bits, expected):
    out = map_fault_status(fault_bits, mask_bits)
    assert out == expected
