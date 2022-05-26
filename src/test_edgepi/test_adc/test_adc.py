from edgepi.adc.adc_commands import ADCCommands
import pytest
from edgepi.adc.adc_constants import EDGEPI_ADC_CHANNEL as CH
from edgepi.adc.adc_commands import ADCCommands

@pytest.fixture(name='adc_ops')
def fixture_test_ADC_ops():
    adc_ops = ADCCommands()
    return adc_ops

@pytest.mark.parametrize("sample, result", [([1], True),
                                            ([1,2,3,4, 5], True), 
                                            ([-1, 1, 2, 3], True), 
                                            ([444, 22, 3333, 5], True), 
                                            ([-111, -2222], True)])
def test_check_for_int(sample, result, adc_ops):
    assert adc_ops.check_for_int(sample) == result

""" 
Test read register content
In: Register address and number of register to read
Out: List of bytes Op-code and dummy bytes to transfer
"""
@pytest.mark.parametrize("address, num_of_regs, result", [(1, 1, [0x21, 0, 255]),
                                                          (2, 4, [0x22, 3, 255, 255, 255, 255]), 
                                                          (3, 5, [0x23, 4, 255, 255, 255, 255, 255]), 
                                                          (10, 7, [0x2A, 6, 255, 255, 255, 255, 255, 255, 255]), 
                                                          (16, 10, [0x30, 9, 255, 255, 255, 255, 255,255, 255, 255, 255, 255])])
def test_read_register_command(address, num_of_regs, result, adc_ops):
    assert adc_ops.read_register_command(address, num_of_regs) == result