"""unit tests for tc_conv_time module"""


import pytest
from edgepi.tc.tc_conv_time import SAFETY_MARGIN, calc_conv_time, ConvTimes

# pylint: disable=too-many-lines

@pytest.mark.parametrize(
    "cr0_val, cr1_val, safe_delay, expected",
    [
        ########################## 60 hz, max base time
        (0x00, 0x03, True, ConvTimes.DEFAULT_HZ60_MAX.value),  # AV_1, OC_OFF, CJ_ON, DEF_MAX, 60HZ
        (
            0x00,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_2.value,
        ),  # AV_2, OC_OFF, CJ_ON, DEF_MAX, 60HZ
        (
            0x00,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_4.value,
        ),  # AV_4, OC_OFF, CJ_ON, DEF_MAX, 60HZ
        (
            0x00,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_8.value,
        ),  # AV_8, OC_OFF, CJ_ON, DEF_MAX, 60HZ
        (
            0x00,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_16.value,
        ),  # AV_16, OC_OFF, CJ_ON, DEF_MAX, 60HZ
        (
            0x10,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_1, OC_L_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x10,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_2, OC_L_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x10,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_4, OC_L_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x10,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_8, OC_L_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x10,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_16, OC_L_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x20,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_1, OC_M_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x20,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_2, OC_M_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x20,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_4, OC_M_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x20,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_8, OC_M_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x20,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_16, OC_M_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x30,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_1, OC_H_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x30,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_2, OC_H_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x30,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_4, OC_H_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x30,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_8, OC_H_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x30,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_16, OC_H_MAX, CJ_ON, DEF_MAX, 60HZ
        (
            0x08,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_OFF, CJ_OFF, DEF_MAX, 60HZ
        (
            0x08,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_2.value + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_OFF, CJ_OFF, DEF_MAX, 60HZ
        (
            0x08,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_4.value + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_OFF, CJ_OFF, DEF_MAX, 60HZ
        (
            0x08,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_8.value + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_OFF, CJ_OFF, DEF_MAX, 60HZ
        (
            0x08,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value + ConvTimes.HZ60_AVG_16.value + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_OFF, CJ_OFF, DEF_MAX, 60HZ
        (
            0x18,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_L_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x18,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_L_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x18,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_L_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x18,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_L_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x18,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_L_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x28,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_M_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x28,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_M_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x28,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_M_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x28,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_M_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x28,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_M_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x38,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_H_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x38,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_H_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x38,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_H_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x38,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_H_MAX, CJ_OFF, DEF_MAX, 60HZ
        (
            0x38,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ60_MAX.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_H_MAX, CJ_OFF, DEF_MAX, 60HZ
        ########################## 60 hz, nominal base time
        (0x00, 0x03, False, ConvTimes.DEFAULT_HZ60_NOM.value),  # AV_1, OC_OFF, CJ_ON, DEF_NOM, 60HZ
        (
            0x00,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_2.value,
        ),  # AV_2, OC_OFF, CJ_ON, DEF_NOM, 60HZ
        (
            0x00,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_4.value,
        ),  # AV_4, OC_OFF, CJ_ON, DEF_NOM, 60HZ
        (
            0x00,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_8.value,
        ),  # AV_8, OC_OFF, CJ_ON, DEF_NOM, 60HZ
        (
            0x00,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_16.value,
        ),  # AV_16, OC_OFF, CJ_ON, DEF_NOM, 60HZ
        (
            0x10,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_1, OC_L_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x10,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_2, OC_L_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x10,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_4, OC_L_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x10,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_8, OC_L_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x10,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_16, OC_L_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x20,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_1, OC_M_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x20,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_2, OC_M_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x20,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_4, OC_M_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x20,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_8, OC_M_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x20,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_16, OC_M_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x30,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_1, OC_H_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x30,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_2, OC_H_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x30,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_4, OC_H_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x30,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_8, OC_H_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x30,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_16, OC_H_NOM, CJ_ON, DEF_NOM, 60HZ
        (
            0x08,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_OFF, CJ_OFF, DEF_NOM, 60HZ
        (
            0x08,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_2.value + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_OFF, CJ_OFF, DEF_NOM, 60HZ
        (
            0x08,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_4.value + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_OFF, CJ_OFF, DEF_NOM, 60HZ
        (
            0x08,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_8.value + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_OFF, CJ_OFF, DEF_NOM, 60HZ
        (
            0x08,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value + ConvTimes.HZ60_AVG_16.value + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_OFF, CJ_OFF, DEF_NOM, 60HZ
        (
            0x18,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_L_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x18,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_L_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x18,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_L_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x18,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_L_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x18,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_L_NOM, CJ_OFF, DEF_V, 60HZ
        (
            0x28,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_M_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x28,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_M_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x28,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_M_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x28,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_M_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x28,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_M_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x38,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_H_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x38,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_2.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_H_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x38,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_4.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_H_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x38,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_8.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_H_NOM, CJ_OFF, DEF_NOM, 60HZ
        (
            0x38,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ60_NOM.value
            + ConvTimes.HZ60_AVG_16.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_H_NOM, CJ_OFF, DEF_NOM, 60HZ
        ########################## 50 hz, max base time
        (0x01, 0x03, True, ConvTimes.DEFAULT_HZ50_MAX.value),  # AV_1, OC_OFF, CJ_ON, DEF_MAX, 50HZ
        (
            0x01,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_2.value,
        ),  # AV_2, OC_OFF, CJ_ON, DEF_MAX, 50HZ
        (
            0x01,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_4.value,
        ),  # AV_4, OC_OFF, CJ_ON, DEF_MAX, 50HZ
        (
            0x01,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_8.value,
        ),  # AV_8, OC_OFF, CJ_ON, DEF_MAX, 50HZ
        (
            0x01,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_16.value,
        ),  # AV_16, OC_OFF, CJ_ON, DEF_MAX, 50HZ
        (
            0x11,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_1, OC_L_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x11,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_2, OC_L_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x11,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_4, OC_L_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x11,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_8, OC_L_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x11,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_ON_OC_LOW_MAX.value,
        ),  # AV_16, OC_L_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x21,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_1, OC_M_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x21,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_2, OC_M_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x21,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_4, OC_M_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x21,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_8, OC_M_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x21,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_ON_OC_MED_MAX.value,
        ),  # AV_16, OC_M_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x31,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_1, OC_H_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x31,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_2, OC_H_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x31,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_4, OC_H_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x31,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_8, OC_H_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x31,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_ON_OC_HIGH_MAX.value,
        ),  # AV_16, OC_H_MAX, CJ_ON, DEF_MAX, 50HZ
        (
            0x09,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_OFF, CJ_OFF, DEF_MAX, 50HZ
        (
            0x09,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_2.value + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_OFF, CJ_OFF, DEF_MAX, 50HZ
        (
            0x09,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_4.value + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_OFF, CJ_OFF, DEF_MAX, 50HZ
        (
            0x09,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_8.value + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_OFF, CJ_OFF, DEF_MAX, 50HZ
        (
            0x09,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value + ConvTimes.HZ50_AVG_16.value + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_OFF, CJ_OFF, DEF_MAX, 50HZ
        (
            0x19,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_L_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x19,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_L_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x19,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_L_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x19,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_L_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x19,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_OFF_OC_LOW_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_L_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x29,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_M_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x29,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_M_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x29,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_M_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x29,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_M_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x29,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_OFF_OC_MED_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_M_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x39,
            0x03,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_H_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x39,
            0x13,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_H_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x39,
            0x23,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_H_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x39,
            0x33,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_H_MAX, CJ_OFF, DEF_MAX, 50HZ
        (
            0x39,
            0x43,
            True,
            ConvTimes.DEFAULT_HZ50_MAX.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_OFF_OC_HIGH_MAX.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_H_MAX, CJ_OFF, DEF_MAX, 50HZ
        ########################## 50 hz, nominal base time
        (0x01, 0x03, False, ConvTimes.DEFAULT_HZ50_NOM.value),  # AV_1, OC_OFF, CJ_ON, DEF_NOM, 50HZ
        (
            0x01,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_2.value,
        ),  # AV_2, OC_OFF, CJ_ON, DEF_NOM, 50HZ
        (
            0x01,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_4.value,
        ),  # AV_4, OC_OFF, CJ_ON, DEF_NOM, 50HZ
        (
            0x01,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_8.value,
        ),  # AV_8, OC_OFF, CJ_ON, DEF_NOM, 50HZ
        (
            0x01,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_16.value,
        ),  # AV_16, OC_OFF, CJ_ON, DEF_NOM, 50HZ
        (
            0x11,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_1, OC_L_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x11,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_2, OC_L_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x11,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_4, OC_L_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x11,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_8, OC_L_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x11,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_ON_OC_LOW_NOM.value,
        ),  # AV_16, OC_L_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x21,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_1, OC_M_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x21,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_2, OC_M_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x21,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_4, OC_M_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x21,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_8, OC_M_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x21,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_ON_OC_MED_NOM.value,
        ),  # AV_16, OC_M_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x31,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_1, OC_H_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x31,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_2, OC_H_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x31,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_4, OC_H_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x31,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_8, OC_H_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x31,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_ON_OC_HIGH_NOM.value,
        ),  # AV_16, OC_H_NOM, CJ_ON, DEF_NOM, 50HZ
        (
            0x09,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_OFF, CJ_OFF, DEF_NOM, 50HZ
        (
            0x09,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_2.value + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_OFF, CJ_OFF, DEF_NOM, 50HZ
        (
            0x09,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_4.value + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_OFF, CJ_OFF, DEF_NOM, 50HZ
        (
            0x09,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_8.value + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_OFF, CJ_OFF, DEF_NOM, 50HZ
        (
            0x09,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value + ConvTimes.HZ50_AVG_16.value + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_OFF, CJ_OFF, DEF_NOM, 50HZ
        (
            0x19,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_L_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x19,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_L_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x19,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_L_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x19,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_L_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x19,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_OFF_OC_LOW_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_L_NOM, CJ_OFF, DEF_V, 50HZ
        (
            0x29,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_M_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x29,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_M_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x29,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_M_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x29,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_M_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x29,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_OFF_OC_MED_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_M_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x39,
            0x03,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_1, OC_H_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x39,
            0x13,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_2.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_2, OC_H_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x39,
            0x23,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_4.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_4, OC_H_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x39,
            0x33,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_8.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_8, OC_H_NOM, CJ_OFF, DEF_NOM, 50HZ
        (
            0x39,
            0x43,
            False,
            ConvTimes.DEFAULT_HZ50_NOM.value
            + ConvTimes.HZ50_AVG_16.value
            + ConvTimes.CJ_OFF_OC_HIGH_NOM.value
            + ConvTimes.CJ_OFF.value,
        ),  # AV_16, OC_H_NOM, CJ_OFF, DEF_NOM, 50HZ
    ],
)
def test_calc_conv_time(cr0_val, cr1_val, safe_delay, expected):
    assert calc_conv_time(cr0_val, cr1_val, safe_delay) == pytest.approx(expected * SAFETY_MARGIN)
