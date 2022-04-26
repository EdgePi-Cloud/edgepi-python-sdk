import pytest
from DAC_Methods import DAC_Methods


@pytest.fixture(name='dac_ops')
def fixture_test_DAC_ops():
    dac_ops = DAC_Methods()
    yield dac_ops

@pytest.mark.parametrize("a, b, c, d",[(3, 1, 1000, [49, 3, 232]), (3, 0, 1000, [48, 3, 232]), (3, 3, 1000, [51, 3, 232])])
def test_write_and_update(a, b, c, d, dac_ops):
    assert dac_ops.combine_command(a, b, c) == d

