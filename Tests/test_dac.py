import pytest
from DAC.DAC_Commands import DAC_Commands


@pytest.fixture(name='dac_ops')
def fixture_test_DAC_ops():
    dac_ops = DAC_Commands()
    return dac_ops

'''
Combine command needs check for interger numbers for op-code, channel and value
It also needs to check the range of each value.
'''

@pytest.mark.parametrize("sample, result", [([1], True),
                                            ([1,2.22,3,4,], False), 
                                            ([None, 1, 2, 3], False), 
                                            ([], False), 
                                            ([-1, -2.22], False)])
# TODO: Is this the right way to test exception handler?
def test_check_for_int(sample, result, dac_ops):
    try:
        assert dac_ops.check_for_int(sample) == result
    except ValueError:
        assert False == result

@pytest.mark.parametrize("min, target, max, result",[(0, -1, 10, False), 
                                                     (0, 0, 10, True), 
                                                     (0, 10, 10, True), 
                                                     (0, 11, 10, False), 
                                                     (0, 5, 10, True), 
                                                     (0.5, 1, 1.1, True)])

def test_check_range(min, target, max, result, dac_ops):
    try:
        assert dac_ops.check_range(target, min, max) == result
    except ValueError:
        assert False == result

@pytest.mark.parametrize("a, b, c, d",[(3, 1, 1000, [49, 3, 232]), 
                                       (3, 0, 1000, [48, 3, 232]), 
                                       (3, 3, 1000, [51, 3, 232])])
def test_combine_command(a, b, c, d, dac_ops):
    assert dac_ops.combine_command(a, b, c) == d


@pytest.mark.parametrize("a, b, c",[(1, 1000, [49, 3, 232]), 
                                    (0, 1000, [48, 3, 232]), 
                                    (3, 1000, [51, 3, 232])])
def test_generate_write_and_update_command(a, b, c, dac_ops):
    assert dac_ops.generate_write_and_update_command(a, b) == c

'''
voltage to code conversion
voltage = positive floating number 0~5V ideally
code = positive integer number 0~65535
rounding up/down during conversion ?
'''

@pytest.mark.parametrize("ch, expected, result",[(1, 2.345, 30030), 
                                    (0, 2.345, 30030), 
                                    (3, 2.345, 30030)])
def test_voltage_to_code(ch, expected, result, dac_ops):
    assert dac_ops.voltage_to_code(ch, expected) == result