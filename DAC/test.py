import pytest
from DAC_Methods import DAC_Methods


@pytest.fixture(name='dac_ops')
def fixture_test_DAC_ops():
    dac_ops = DAC_Methods()
    return dac_ops

'''
Combine command needs check for interger numbers for op-code, channel and value
It also needs to check the range of each value.
'''

@pytest.mark.parametrize("sample, result", [([1], True), ([1,2.22,3,4,], False), ([None, 1, 2, 3], False), ([], False), ([-1, -2.22], False)])
def test_check_for_int(sample, result, dac_ops):
    assert dac_ops.check_for_int(sample) == result

@pytest.mark.parametrize("min, target, max, result",[ (0, 0, 10, False), (0, 10, 10, False), (0, 5, 10, True), (0.5, 1, 1.1, True)])
def test_check_range(min, target, max, result, dac_ops):
    assert dac_ops.check_range(target, min, max) == result

@pytest.mark.parametrize("a, b, c, d",[(3, 1, 1000, [49, 3, 232]), (3, 0, 1000, [48, 3, 232]), (3, 3, 1000, [51, 3, 232])])
def test_combine_command(a, b, c, d, dac_ops):
    assert dac_ops.combine_command(a, b, c) == d


@pytest.mark.parametrize("a, b, c",[(1, 1000, [49, 3, 232]), (0, 1000, [48, 3, 232]), (3, 1000, [51, 3, 232])])
def test_write_and_update(a, b, c, dac_ops):
    assert dac_ops.write_and_update(a, b) == c
