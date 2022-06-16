import pytest
from edgepi.utilities.utilities import filter_dict
from edgepi.tc.tc_constants import *

@pytest.mark.parametrize('dict, keyword, out', [
    ({'self': 0x0}, 'self', []),
    ({'avg_mode': AvgMode.AVG_1}, 'self', [AvgMode.AVG_1]),
    ({'self': 0x0, 'avg_mode': AvgMode.AVG_1}, 'self', [AvgMode.AVG_1]),
])
def test_filter_dict(dict, keyword, out):
    assert filter_dict(dict, keyword) == out
    