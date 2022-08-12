""" Integration tests for EdgePi ADC module """


import pytest
from edgepi.adc.adc_constants import ADCReg
from edgepi.adc.edgepi_adc import EdgePiADC


@pytest.fixture(name="adc")
def fixture_adc():
    return EdgePiADC()


# pylint: disable=protected-access
def test_read_register_individual(adc):
    # read each ADC register individually
    for reg_addx in ADCReg:
        out = adc._EdgePiADC__read_register(reg_addx, 1)
        # output data frame bytes = [null, null, reg_data]
        assert len(out) == 1
