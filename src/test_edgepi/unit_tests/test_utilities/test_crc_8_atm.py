"""Unit tests for crc_8_atm.py"""

from contextlib import nullcontext as does_not_raise

import pytest

from edgepi.utilities.crc_8_atm import (
    generate_crc_8_table,
    check_crc,
    get_crc,
    CRCCheckError,
    CRC_8_ATM_GEN,
    CRC_8_ATM_LUT,
)

@pytest.mark.parametrize(
    "voltage_bytes, crc_code, err",
    [
        ([51, 16, 126, 166], 62, does_not_raise()),
        ([51, 14, 170, 195], 98, does_not_raise()),
        ([51, 16, 133, 237], 75, does_not_raise()),
        ([51, 17, 166, 166], 71, does_not_raise()),
        ([51, 16, 148, 157], 94, does_not_raise()),
        ([51, 14, 144, 155], 150, does_not_raise()),
        ([51, 14, 166, 18], 167, does_not_raise()),
        ([51, 16, 5, 109], 116, does_not_raise()),
        ([51, 15, 16, 130], 4, does_not_raise()),
        ([51, 16, 126, 166], 61, pytest.raises(CRCCheckError)),
        ([51, 14, 170, 195], 99, pytest.raises(CRCCheckError)),
        ([51, 16, 133, 237], 70, pytest.raises(CRCCheckError)),
    ],
)
def test_crc_8_atm_adc_1(voltage_bytes, crc_code, err):
    with err:
        check_crc(voltage_bytes, crc_code)


def test_generate_crc_8_table():
    assert generate_crc_8_table(CRC_8_ATM_GEN) == CRC_8_ATM_LUT


@pytest.mark.parametrize(
    "data, expected, err",
    [
        ([51, 16, 126, 166], 62, does_not_raise()),
        ([51, 14, 170, 195], 98, does_not_raise()),
        ([51, 16, 133, 237], 75, does_not_raise()),
        ([51, 17, 166, 166], 71, does_not_raise()),
        ([51, 16, 148, 157], 94, does_not_raise()),
        ([51, 14, 144, 155], 150, does_not_raise()),
        ([51, 14, 166, 18], 167, does_not_raise()),
        ([51, 16, 5, 109], 116, does_not_raise()),
        ([51, 15, 16, 130], 4, does_not_raise())
    ],
)
def test_get_crc(data, expected, err):
    data_crc = get_crc(data)
    assert len(data)+1 == len(data_crc)
    assert data_crc[-1] == expected
    with err:
        check_crc(data, data_crc[-1])
