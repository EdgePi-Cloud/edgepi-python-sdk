from dataclasses import dataclass
from bitstring import Bits
from enum import Enum, unique
from copy import deepcopy

@unique
class TCFaults(Enum):
    ''' Fault Register bit numbers for each fault type 
        Note: the bit numbers are written in reverse order here in order to 
        be compatible with the bitstring module, since it considers the MSB
        of a bitstring to be index 0. So CJRANGE actually maps to bit 7 on
        the MAX31856.
    '''
    OPEN = 7
    OVUV = 6
    TCLOW = 5
    TCHIGH = 4
    CJLOW = 3
    CJHIGH = 2
    TCRANGE = 1
    CJRANGE = 0

@unique
class FaultMsg(Enum):
    CJRANGE_OK_MSG = 'Cold-junction temperature is within normal operating range'
    CJRANGE_BAD_MSG = 'Cold-junction temperature is outside normal operating range'
    TCRANGE_OK_MSG = 'Thermocouple hot-junction temperature is within normal operating range'
    TCRANGE_BAD_MSG = 'Thermocouple hot-junction temperature is outside normal operating range'
    CJHIGH_OK_MSG = 'Cold-junction temperature is less than or equal to cold-junction high threshold'
    CJHIGH_BAD_MSG = 'Cold-junction temperature is greater than cold-junction high threshold'
    CJLOW_OK_MSG = 'Cold-junction temperature greater than or equal to cold-junction low threshold'
    CJLOW_BAD_MSG = 'Cold-junction temperature less than cold-junction low threshold'
    TCHIGH_OK_MSG = 'Thermocouple temperature is less than or equal to thermocouple high threshold'
    TCHIGH_BAD_MSG = 'Thermocouple temperature is greater than thermocouple high threshold'
    TCLOW_OK_MSG = 'Thermocouple temperature is greater than or equal to thermocouple low threshold'
    TCLOW_BAD_MSG = 'Thermocouple temperature is less than thermocouple low threshold'
    OVUV_OK_MSG = 'Input voltage is positive and less than V_DD'
    OVUV_BAD_MSG = 'Input voltage is negative or greater than V_DD'
    OPEN_OK_MSG = 'No open-circuit or broken thermocouple wires detected'
    OPEN_BAD_MSG = 'Open-circuit detected'

@dataclass
class Fault:
    ''' Represents a Fault Status Register fault

        Attributes:
            name (str): the fault's official MAX31856 name

            fault_type (TCFaults): the fault's TCFaults type

            err_msg (FaultMsg): a message containing the current fault output

            at_fault (bool): set to True if the fault is currently occurring

            is_masked (bool): set to True if this fault is being masked in MASK register.
                              Note this means the FAULT pin will not assert even if this
                              fault is occurring. Faults are masked by default.
    '''
    fault_type : TCFaults
    err_msg : FaultMsg
    at_fault : bool = False
    is_masked : bool = True

@unique
class Faults(Enum):
    CJRANGE_OK = Fault(TCFaults.CJRANGE, FaultMsg.CJRANGE_OK_MSG)
    CJRANGE_BAD = Fault(TCFaults.CJRANGE, FaultMsg.CJRANGE_BAD_MSG, True)
    TCRANGE_OK = Fault(TCFaults.TCRANGE, FaultMsg.TCRANGE_OK_MSG)
    TCRANGE_BAD = Fault(TCFaults.TCRANGE, FaultMsg.TCRANGE_BAD_MSG, True)
    CJHIGH_OK = Fault(TCFaults.CJHIGH, FaultMsg.CJHIGH_OK_MSG)
    CJHIGH_BAD = Fault(TCFaults.CJHIGH, FaultMsg.CJHIGH_BAD_MSG, True)
    CJLOW_OK = Fault(TCFaults.CJLOW, FaultMsg.CJLOW_OK_MSG)
    CJLOW_BAD = Fault(TCFaults.CJLOW, FaultMsg.CJLOW_BAD_MSG, True)
    TCHIGH_OK = Fault(TCFaults.TCHIGH, FaultMsg.TCHIGH_OK_MSG)
    TCHIGH_BAD = Fault(TCFaults.TCHIGH, FaultMsg.TCHIGH_BAD_MSG, True)
    TCLOW_OK = Fault(TCFaults.TCLOW, FaultMsg.TCLOW_OK_MSG)
    TCLOW_BAD = Fault(TCFaults.TCLOW, FaultMsg.TCLOW_BAD_MSG, True)
    OVUV_OK = Fault(TCFaults.OVUV, FaultMsg.OVUV_OK_MSG)
    OVUV_BAD = Fault(TCFaults.OVUV, FaultMsg.OVUV_BAD_MSG, True)
    OPEN_OK = Fault(TCFaults.OPEN, FaultMsg.OPEN_OK_MSG)
    OPEN_BAD = Fault(TCFaults.OPEN, FaultMsg.OPEN_BAD_MSG, True)

_faults_map = {
    TCFaults.CJRANGE.value: (Faults.CJRANGE_OK, Faults.CJRANGE_BAD),
    TCFaults.TCRANGE.value: (Faults.TCRANGE_OK, Faults.TCRANGE_BAD),
    TCFaults.CJHIGH.value: (Faults.CJHIGH_OK, Faults.CJHIGH_BAD),
    TCFaults.CJLOW.value: (Faults.CJLOW_OK, Faults.CJLOW_BAD),
    TCFaults.TCHIGH.value: (Faults.TCHIGH_OK, Faults.TCHIGH_BAD),
    TCFaults.TCLOW.value: (Faults.TCLOW_OK, Faults.TCLOW_BAD),
    TCFaults.OVUV.value: (Faults.OVUV_OK, Faults.OVUV_BAD),
    TCFaults.OPEN.value: (Faults.OPEN_OK, Faults.OPEN_BAD)
    }

def map_fault_status(fault_bits:Bits, fault_masks:Bits) -> dict:
    ''' Generates a dictionary of Fault objects

        Args:
            fault_bits (bitstring.Bits): Fault Status register bits

            fault_masks (bitstring.Bits): Fault Mask register bits
        
        Returns:
            a dict containing information on the current status of each Fault Status register bit
    '''
    faults_dict = {}

    # check each bit in fault status and fault mask registers to generate Faults
    for i in range(8):
        # choose Fault type from _faults_map based on whether this bit is set or not
        fault = deepcopy(_faults_map[i][fault_bits[i]].value)

        # is the corresponding bit for this fault type set in fault mask register
        fault.is_masked = fault_masks[i]

        faults_dict[fault.fault_type] = fault

    return faults_dict
    