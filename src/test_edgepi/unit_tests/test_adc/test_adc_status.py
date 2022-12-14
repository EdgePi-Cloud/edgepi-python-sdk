"""unit tests for adc_status.py module"""


import pytest
from edgepi.adc.adc_status import get_adc_status, ADCStatusBit, ADCStatusMsg, ADCStatus


@pytest.mark.parametrize(
    "status_byte, expected_status",
    [
        # MSB (bit 7) = index 0 in bitstring
        (
            0b0,
            {
                ADCStatusBit.ADC2_DATA: ADCStatus(
                    ADCStatusBit.ADC2_DATA,
                    ADCStatusMsg.ADC2_DATA_OLD,
                    False
                ),
                ADCStatusBit.ADC1_DATA: ADCStatus(
                    ADCStatusBit.ADC1_DATA,
                    ADCStatusMsg.ADC1_DATA_OLD,
                    False
                ),
                ADCStatusBit.EXTCLK: ADCStatus(
                    ADCStatusBit.EXTCLK,
                    ADCStatusMsg.EXTCLK_INT,
                    False
                ),
                ADCStatusBit.REF_ALM: ADCStatus(
                    ADCStatusBit.REF_ALM,
                    ADCStatusMsg.REF_ALM_OK,
                    False
                ),
                ADCStatusBit.PGAL_ALM: ADCStatus(
                    ADCStatusBit.PGAL_ALM,
                    ADCStatusMsg.PGAL_ALM_OK,
                    False
                ),
                ADCStatusBit.PGAH_ALM: ADCStatus(
                    ADCStatusBit.PGAH_ALM,
                    ADCStatusMsg.PGAH_ALM_OK,
                    False
                ),
                ADCStatusBit.PGAD_ALM: ADCStatus(
                    ADCStatusBit.PGAD_ALM,
                    ADCStatusMsg.PGAD_ALM_OK,
                    False
                ),
                ADCStatusBit.RESET: ADCStatus(
                    ADCStatusBit.RESET,
                    ADCStatusMsg.RESET_FALSE,
                    False
                ),
            },
        ),
        (
            0xFF,
            {
                ADCStatusBit.ADC2_DATA: ADCStatus(
                    ADCStatusBit.ADC2_DATA,
                    ADCStatusMsg.ADC2_DATA_NEW,
                    True
                ),
                ADCStatusBit.ADC1_DATA: ADCStatus(
                    ADCStatusBit.ADC1_DATA,
                    ADCStatusMsg.ADC1_DATA_NEW,
                    True
                ),
                ADCStatusBit.EXTCLK: ADCStatus(
                    ADCStatusBit.EXTCLK,
                    ADCStatusMsg.EXTCLK_EXT,
                    True
                ),
                ADCStatusBit.REF_ALM: ADCStatus(
                    ADCStatusBit.REF_ALM,
                    ADCStatusMsg.REF_ALM_BAD,
                    True
                ),
                ADCStatusBit.PGAL_ALM: ADCStatus(
                    ADCStatusBit.PGAL_ALM,
                    ADCStatusMsg.PGAL_ALM_BAD,
                    True
                ),
                ADCStatusBit.PGAH_ALM: ADCStatus(
                    ADCStatusBit.PGAH_ALM,
                    ADCStatusMsg.PGAH_ALM_BAD,
                    True
                ),
                ADCStatusBit.PGAD_ALM: ADCStatus(
                    ADCStatusBit.PGAD_ALM,
                    ADCStatusMsg.PGAD_ALM_BAD,
                    True
                ),
                ADCStatusBit.RESET: ADCStatus(
                    ADCStatusBit.RESET,
                    ADCStatusMsg.RESET_TRUE,
                    True
                ),
            },
        ),
    ],
)
def test_get_adc_status(status_byte, expected_status):
    assert get_adc_status(status_byte) == expected_status
