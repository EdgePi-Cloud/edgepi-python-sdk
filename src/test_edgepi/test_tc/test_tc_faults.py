import pytest
from bitstring import Bits
from edgepi.tc.tc_faults import map_fault_status, Fault, FaultMsg, TCFaults

@pytest.mark.parametrize('fault_bits, mask_bits, expected', [
    (Bits('0xFF'), Bits('0xFF'),
        {
            TCFaults.CJRANGE: Fault(TCFaults.CJRANGE, FaultMsg.CJRANGE_BAD_MSG, at_fault=True, is_masked=True),
            TCFaults.TCRANGE: Fault(TCFaults.TCRANGE, FaultMsg.TCRANGE_BAD_MSG, at_fault=True, is_masked=True),
            TCFaults.CJHIGH: Fault(TCFaults.CJHIGH, FaultMsg.CJHIGH_BAD_MSG, at_fault=True, is_masked=True),
            TCFaults.CJLOW: Fault(TCFaults.CJLOW, FaultMsg.CJLOW_BAD_MSG, at_fault=True, is_masked=True),
            TCFaults.TCHIGH: Fault(TCFaults.TCHIGH, FaultMsg.TCHIGH_BAD_MSG, at_fault=True, is_masked=True),
            TCFaults.TCLOW: Fault(TCFaults.TCLOW, FaultMsg.TCLOW_BAD_MSG, at_fault=True, is_masked=True),
            TCFaults.OVUV: Fault(TCFaults.OVUV, FaultMsg.OVUV_BAD_MSG, at_fault=True, is_masked=True),
            TCFaults.OPEN: Fault(TCFaults.OPEN, FaultMsg.OPEN_BAD_MSG, at_fault=True, is_masked=True)
        }
    ),   # all faults, all masks
    (Bits('0x00'), Bits('0xFF'),
        {
            TCFaults.CJRANGE: Fault(TCFaults.CJRANGE, FaultMsg.CJRANGE_OK_MSG, is_masked=True),
            TCFaults.TCRANGE: Fault(TCFaults.TCRANGE, FaultMsg.TCRANGE_OK_MSG, is_masked=True),
            TCFaults.CJHIGH: Fault(TCFaults.CJHIGH, FaultMsg.CJHIGH_OK_MSG, is_masked=True),
            TCFaults.CJLOW: Fault(TCFaults.CJLOW, FaultMsg.CJLOW_OK_MSG, is_masked=True),
            TCFaults.TCHIGH: Fault(TCFaults.TCHIGH, FaultMsg.TCHIGH_OK_MSG, is_masked=True),
            TCFaults.TCLOW: Fault(TCFaults.TCLOW, FaultMsg.TCLOW_OK_MSG, is_masked=True),
            TCFaults.OVUV: Fault(TCFaults.OVUV, FaultMsg.OVUV_OK_MSG, is_masked=True),
            TCFaults.OPEN: Fault(TCFaults.OPEN, FaultMsg.OPEN_OK_MSG, is_masked=True)
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
