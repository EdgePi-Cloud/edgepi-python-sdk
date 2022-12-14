"""Utility module for ADC fault reading"""

from dataclasses import dataclass
from enum import Enum, unique

import bitstring


@unique
class ADCStatusBit(Enum):
    """
    Bit numbers for each ADC STATUS byte fault/field (in reverse order)
    """

    RESET = 7
    PGAD_ALM = 6
    PGAH_ALM = 5
    PGAL_ALM = 4
    REF_ALM = 3
    EXTCLK = 2
    ADC1_DATA = 1
    ADC2_DATA = 0


@unique
class ADCStatusMsg(Enum):
    """Debugging messages used in STATUS byte info returned to the user"""

    ADC2_DATA_NEW = "New voltage read data is available for ADC2"
    ADC2_DATA_OLD = "No new voltage read data is available for ADC2"
    ADC1_DATA_NEW = "New voltage read data is available for ADC1"
    ADC1_DATA_OLD = "No new voltage read data is available for ADC1"
    EXTCLK_EXT = "ADC clock source is external"
    EXTCLK_INT = "ADC clock source is internal"
    REF_ALM_OK = "ADC1: no low reference voltage alarm detected"
    REF_ALM_BAD = "ADC1: low reference voltage alarm detected, less than or equal to 0.4 V"
    PGAL_ALM_OK = "ADC1: no absolute low voltage alarm detected"
    PGAL_ALM_BAD = "ADC1: absolute low voltage alarm detected"
    PGAH_ALM_OK = "ADC1: no absolute high voltage alarm detected"
    PGAH_ALM_BAD = "ADC1: absolute high voltage alarm detected"
    PGAD_ALM_OK = "ADC1: no PGA differential output range alarm detected"
    PGAD_ALM_BAD = "ADC1: PGA differential output range alarm detected"
    RESET_TRUE = "New ADC device reset has occured"
    RESET_FALSE = "No new ADC device reset has occured since RESET bit last cleared"



@dataclass
class ADCStatus:
    """Represents the status of a STATUS byte field

    Attributes:
        name (str): the STATUS byte field's official ADS1263 name

        status_type (ADCStatusBit): the ADCFaultType STATUS bit type

        err_msg (ADCStatusMsg): a message containing the current fault output

        at_fault (bool): set to True if the STATUS bit is set
    """

    status_type: ADCStatusBit = None
    err_msg: ADCStatusMsg = None
    at_fault: bool = False

    def __repr__(self) -> str:
        msg = (
            "\n\t{"
            + f"""
            STATUS bit: {self.status_type},
            At Fault: {self.at_fault},
            Status Message: {self.err_msg.value},
        """
            + "}\n"
        )
        return msg


_fault_msg_map = {
    ADCStatusBit.ADC2_DATA: (ADCStatusMsg.ADC2_DATA_OLD, ADCStatusMsg.ADC2_DATA_NEW),
    ADCStatusBit.ADC1_DATA: (ADCStatusMsg.ADC1_DATA_OLD, ADCStatusMsg.ADC1_DATA_NEW),
    ADCStatusBit.EXTCLK: (ADCStatusMsg.EXTCLK_INT, ADCStatusMsg.EXTCLK_EXT),
    ADCStatusBit.REF_ALM: (ADCStatusMsg.REF_ALM_OK, ADCStatusMsg.REF_ALM_BAD),
    ADCStatusBit.PGAL_ALM: (ADCStatusMsg.PGAL_ALM_OK, ADCStatusMsg.PGAL_ALM_BAD),
    ADCStatusBit.PGAH_ALM: (ADCStatusMsg.PGAH_ALM_OK, ADCStatusMsg.PGAH_ALM_BAD),
    ADCStatusBit.PGAD_ALM: (ADCStatusMsg.PGAD_ALM_OK, ADCStatusMsg.PGAD_ALM_BAD),
    ADCStatusBit.RESET: (ADCStatusMsg.RESET_FALSE, ADCStatusMsg.RESET_TRUE),
}


def get_adc_status(status_code: int) -> dict:
    """Generates a dictionary of ADC Status objects

    Args:
        `status_byte` (int): uint value of ADC STATUS byte from voltage reading

    Returns:
        `dict`: contains information on the current status of each STATUS byte bit
    """
    status_dict = {}

    status_byte = bitstring.pack("uint:8", status_code)

    # check each bit in status_byte
    for bit_num in ADCStatusBit:
        status = ADCStatus(status_type=bit_num)

        # get value of ith bit in status byte, either 0 or 1
        bit_value = status_byte[bit_num.value]

        # get message depending on whether ith bit of status byte is set or not
        status.err_msg = _fault_msg_map[bit_num][bit_value]

        status.at_fault = bit_value

        status_dict[bit_num] = status

    return status_dict
