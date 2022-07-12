"""unit test for utilities.py module"""

import pytest
from edgepi.utilities.utilities import filter_dict
from edgepi.tc.tc_constants import AvgMode


@pytest.mark.parametrize(
    "args_dict, key, val, out",
    [
        ({"self": 0x0}, "self", "", {}),
        ({"avg_mode": AvgMode.AVG_1}, "self", "", {"avg_mode": AvgMode.AVG_1}),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1},
            "self",
            "",
            {"avg_mode": AvgMode.AVG_1},
        ),
        ({"self": 0x0, "avg_mode": AvgMode.AVG_1}, "avg_mode", "", {"self": 0x0}),
        ({"self": 0x0, "avg_mode": AvgMode.AVG_1}, "", AvgMode.AVG_1, {"self": 0x0}),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1},
            "",
            0x0,
            {"avg_mode": AvgMode.AVG_1},
        ),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1, "test_var": 0x5},
            "test_var",
            0x0,
            {"avg_mode": AvgMode.AVG_1},
        ),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1, "test_var": 0x5},
            "test_var",
            0x5,
            {"self": 0x0, "avg_mode": AvgMode.AVG_1},
        ),
    ],
)
def test_filter_dict(args_dict, key, val, out):
    assert filter_dict(args_dict, key, val) == out
