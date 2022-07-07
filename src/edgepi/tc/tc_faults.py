""" Helper module for reading thermocouple fault status

    Classes:

        FaultType
        FaultMsg
        Fault

    Functions:
        map_fault_status(Bits)
"""


from dataclasses import dataclass
from enum import Enum, unique
from bitstring import Bits


@unique
class FaultType(Enum):
    """Fault Register bit numbers for each fault type
    Note: the bit numbers are written in reverse order here in order to
    be compatible with the bitstring module, since it considers the MSB
    of a bitstring to be index 0. So CJRANGE actually maps to bit 7 on
    the MAX31856.
    """

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
    """Debugging messages used in Faults returned to the user"""

    CJRANGE_OK_MSG = "Cold-junction temperature is within normal operating range"
    CJRANGE_BAD_MSG = "Cold-junction temperature is outside normal operating range"
    TCRANGE_OK_MSG = "Thermocouple hot-junction temperature is within normal operating range"
    TCRANGE_BAD_MSG = "Thermocouple hot-junction temperature is outside normal operating range"
    CJHIGH_OK_MSG = (
        "Cold-junction temperature is less than or equal to cold-junction high threshold"
    )
    CJHIGH_BAD_MSG = "Cold-junction temperature is greater than cold-junction high threshold"
    CJLOW_OK_MSG = "Cold-junction temperature greater than or equal to cold-junction low threshold"
    CJLOW_BAD_MSG = "Cold-junction temperature less than cold-junction low threshold"
    TCHIGH_OK_MSG = "Thermocouple temperature is less than or equal to thermocouple high threshold"
    TCHIGH_BAD_MSG = "Thermocouple temperature is greater than thermocouple high threshold"
    TCLOW_OK_MSG = "Thermocouple temperature is greater than or equal to thermocouple low threshold"
    TCLOW_BAD_MSG = "Thermocouple temperature is less than thermocouple low threshold"
    OVUV_OK_MSG = "Input voltage is positive and less than V_DD"
    OVUV_BAD_MSG = "Input voltage is negative or greater than V_DD"
    OPEN_OK_MSG = "No open-circuit or broken thermocouple wires detected"
    OPEN_BAD_MSG = "Open-circuit detected"


@dataclass
class Fault:
    """Represents a Fault Status Register fault

    Attributes:
        name (str): the fault's official MAX31856 name

        fault_type (FaultType): the fault's FaultType type

        err_msg (FaultMsg): a message containing the current fault output

        at_fault (bool): set to True if the fault is currently occurring

        is_masked (bool): set to True if this fault is being masked in MASK register.
                          Note this means the FAULT pin will not assert even if this
                          fault is occurring. Faults are masked by default.
    """

    fault_type: FaultType = None
    err_msg: FaultMsg = None
    at_fault: bool = False
    is_masked: bool = True

    def __repr__(self) -> str:
        msg = (
            "\n\t{"
            + f"""
            Fault Type: {self.fault_type},
            At Fault: {self.at_fault},
            Fault Message: {self.err_msg.value},
            Fault Masked: {self.is_masked},
        """
            + "}\n"
        )
        return msg


_fault_msg_map = {
    FaultType.CJRANGE: (FaultMsg.CJRANGE_OK_MSG, FaultMsg.CJRANGE_BAD_MSG),
    FaultType.TCRANGE: (FaultMsg.TCRANGE_OK_MSG, FaultMsg.TCRANGE_BAD_MSG),
    FaultType.CJHIGH: (FaultMsg.CJHIGH_OK_MSG, FaultMsg.CJHIGH_BAD_MSG),
    FaultType.CJLOW: (FaultMsg.CJLOW_OK_MSG, FaultMsg.CJLOW_BAD_MSG),
    FaultType.TCHIGH: (FaultMsg.TCHIGH_OK_MSG, FaultMsg.TCHIGH_BAD_MSG),
    FaultType.TCLOW: (FaultMsg.TCLOW_OK_MSG, FaultMsg.TCLOW_BAD_MSG),
    FaultType.OVUV: (FaultMsg.OVUV_OK_MSG, FaultMsg.OVUV_BAD_MSG),
    FaultType.OPEN: (FaultMsg.OPEN_OK_MSG, FaultMsg.OPEN_BAD_MSG),
}


def map_fault_status(fault_bits: Bits, fault_masks: Bits) -> dict:
    """Generates a dictionary of Fault objects

    Args:
        fault_bits (bitstring.Bits): Fault Status register bits

        fault_masks (bitstring.Bits): Fault Mask register bits

    Returns:
        a dict containing information on the current status of each Fault Status register bit
    """
    faults_dict = {}

    # check each bit in fault status and fault mask registers to generate
    # Faults
    for tcfault_type in FaultType:
        fault = Fault(fault_type=tcfault_type)

        # get value of ith bit in fault_bits register, either 0 or 1
        fault_bit_value = fault_bits[tcfault_type.value]

        # get message depending on whether ith bit of fault_bits is set or not
        fault.err_msg = _fault_msg_map[tcfault_type][fault_bit_value]

        fault.at_fault = fault_bit_value

        # check ith bit in fault_masks register to see if this fault type is
        # being masked.
        fault.is_masked = fault_masks[tcfault_type.value]

        faults_dict[tcfault_type] = fault

    return faults_dict
