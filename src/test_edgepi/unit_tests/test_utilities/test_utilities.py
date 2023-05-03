"""unit test for utilities.py module"""

import pytest
from bitstring import pack
from edgepi.utilities.utilities import filter_dict, filter_dict_list_key_val, bitstring_from_list
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

@pytest.mark.parametrize(
    "args_dict, key, val, out",
    [
        ({"self": 0x0}, ["self"], [""], {}),
        ({"avg_mode": AvgMode.AVG_1}, ["self"], [""], {"avg_mode": AvgMode.AVG_1}),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1},
            ["self"],
            [""],
            {"avg_mode": AvgMode.AVG_1},
        ),
        ({"self": 0x0, "avg_mode": AvgMode.AVG_1}, ["avg_mode", "self"], [""], {}),
        ({"self": 0x0, "avg_mode": AvgMode.AVG_1}, [""], [0x0,AvgMode.AVG_1], {}),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1},
            [""],
            [0x0],
            {"avg_mode": AvgMode.AVG_1},
        ),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1, "test_var": 0x5},
            ["test_var"],
            [0x0],
            {"avg_mode": AvgMode.AVG_1},
        ),
        (
            {"self": 0x0, "avg_mode": AvgMode.AVG_1, "test_var": 0x5},
            ["test_var"],
            [0x5],
            {"self": 0x0, "avg_mode": AvgMode.AVG_1},
        ),
    ],
)
def test_filter_dict_list_keys_values(args_dict, key, val, out):
    assert filter_dict_list_key_val(args_dict, key, val) == out

@pytest.mark.parametrize("data_bytes, expected", [
    ([0x0, 0x0, 0x0], pack("uint:24", 0)),
    ([0x0, 0x0, 0x0, 0x0], pack("uint:32", 0)),
    ([0x01, 0x02, 0x03, 0x04], pack("hex:32", "0x01020304")),
    ([0x1, 0x2, 0x3, 0x4], pack("hex:32", "0x01020304")),
    ([0x10, 0x20, 0x30, 0x40], pack("hex:32", "0x10203040")),
    ([0xFF, 0xFF, 0xFF, 0xFF], pack("hex:32", "0xFFFFFFFF")),
])
def test_bitstring_from_list(data_bytes, expected):
    assert bitstring_from_list(data_bytes) == expected
