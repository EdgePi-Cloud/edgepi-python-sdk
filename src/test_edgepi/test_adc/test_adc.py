import pytest
from edgepi.adc.adc_constants import EDGEPI_ADC_CHANNEL as CH

""" 
Test read register content
In: Register address and number of register to read
Out: List of bytes Op-code and dummy bytes to transfer
"""
@pytest.mark.parametrize("address, num_of_regs, result", [(1, 1, []),
                                                          (2, 4, []), 
                                                          (3, 5, []), 
                                                          (10, 7, []), 
                                                          (16, 10, [])])
def test_read_register_command(address, num_of_regs, result):
