"""
For ADC state querying
"""

import logging
from dataclasses import dataclass
from typing import Any
from enum import Enum

from edgepi.adc.adc_constants import (
    IDACMAG,
    IDACMUX,
    REFMUX,
    ADC1DataRate,
    ADC2DataRate,
    ADCChannel,
    ADCMasks,
    ADCReg,
    CheckMode,
    ConvMode,
    FilterMode,
    StatusByte,
)
from edgepi.reg_helper.reg_helper import BitMask


@dataclass
class ADCModeValue:
    """
    Stores information about a specific value of an ADC functional mode

    Attributes
        `value` (any): user-friendly description of this mode value
        `code` (Enum): internal code used to set this mode value
    """

    value: Any
    code: Enum

    def __repr__(self) -> str:
        return f"value: {self.value}, code: {self.code}"


@dataclass
class ADCMode:
    """Stores information about an ADC functional mode"""

    name: str
    addx: int
    mask: int
    values: dict[int, ADCModeValue]


class ADCModes(Enum):
    """Address and mask values for ADC functional modes"""

    CONV_MODE = ADCMode(
        "conversion-mode",
        ADCReg.REG_MODE0.value,
        BitMask.BIT6.value,
        {
            ConvMode.PULSE.value.op_code: ADCModeValue("pulse", ConvMode.PULSE),
            ConvMode.CONTINUOUS.value.op_code: ADCModeValue("continuous", ConvMode.CONTINUOUS),
        },
    )
    CHECK_MODE = ADCMode(
        "checksum-byte-mode",
        ADCReg.REG_INTERFACE.value,
        ADCMasks.CHECK_BITS.value,
        {
            CheckMode.CHECK_BYTE_OFF.value.op_code: ADCModeValue("off", CheckMode.CHECK_BYTE_OFF),
            CheckMode.CHECK_BYTE_CHK.value.op_code: ADCModeValue(
                "checksum", CheckMode.CHECK_BYTE_CHK
            ),
            CheckMode.CHECK_BYTE_CRC.value.op_code: ADCModeValue("crc", CheckMode.CHECK_BYTE_CRC),
        },
    )
    STATUS_MODE = ADCMode(
        "status-byte-mode",
        ADCReg.REG_INTERFACE.value,
        BitMask.BIT2.value,
        {
            StatusByte.STATUS_BYTE_OFF.value.op_code: ADCModeValue(
                "off", StatusByte.STATUS_BYTE_OFF
            ),
            StatusByte.STATUS_BYTE_ON.value.op_code: ADCModeValue("on", StatusByte.STATUS_BYTE_ON),
        },
    )
    DATA_RATE_1 = ADCMode(
        "data-rate-adc-1",
        ADCReg.REG_MODE2.value,
        BitMask.LOW_NIBBLE.value,
        {
            ADC1DataRate.SPS_2P5.value.op_code: ADCModeValue(2.5, ADC1DataRate.SPS_2P5),
            ADC1DataRate.SPS_5.value.op_code: ADCModeValue(5, ADC1DataRate.SPS_5),
            ADC1DataRate.SPS_10.value.op_code: ADCModeValue(10, ADC1DataRate.SPS_10),
            ADC1DataRate.SPS_16P6.value.op_code: ADCModeValue(16.6, ADC1DataRate.SPS_16P6),
            ADC1DataRate.SPS_20.value.op_code: ADCModeValue(20, ADC1DataRate.SPS_20),
            ADC1DataRate.SPS_50.value.op_code: ADCModeValue(50, ADC1DataRate.SPS_50),
            ADC1DataRate.SPS_60.value.op_code: ADCModeValue(60, ADC1DataRate.SPS_60),
            ADC1DataRate.SPS_100.value.op_code: ADCModeValue(100, ADC1DataRate.SPS_100),
            ADC1DataRate.SPS_400.value.op_code: ADCModeValue(400, ADC1DataRate.SPS_400),
            ADC1DataRate.SPS_1200.value.op_code: ADCModeValue(1200, ADC1DataRate.SPS_1200),
            ADC1DataRate.SPS_2400.value.op_code: ADCModeValue(2400, ADC1DataRate.SPS_2400),
            ADC1DataRate.SPS_4800.value.op_code: ADCModeValue(4800, ADC1DataRate.SPS_4800),
            ADC1DataRate.SPS_7200.value.op_code: ADCModeValue(7200, ADC1DataRate.SPS_7200),
            ADC1DataRate.SPS_14400.value.op_code: ADCModeValue(14400, ADC1DataRate.SPS_14400),
            ADC1DataRate.SPS_19200.value.op_code: ADCModeValue(19200, ADC1DataRate.SPS_19200),
            ADC1DataRate.SPS_38400.value.op_code: ADCModeValue(38400, ADC1DataRate.SPS_38400),
        },
    )
    DATA_RATE_2 = ADCMode(
        "data-rate-adc-2",
        ADCReg.REG_ADC2CFG.value,
        ADCMasks.ADC2_DR_BITS.value,
        {
            ADC2DataRate.SPS_10.value.op_code: ADCModeValue(10, ADC2DataRate.SPS_10),
            ADC2DataRate.SPS_100.value.op_code: ADCModeValue(10, ADC2DataRate.SPS_100),
            ADC2DataRate.SPS_400.value.op_code: ADCModeValue(400, ADC2DataRate.SPS_400),
            ADC2DataRate.SPS_800.value.op_code: ADCModeValue(800, ADC2DataRate.SPS_800),
        },
    )
    FILTER_MODE = ADCMode(
        "filter-mode",
        ADCReg.REG_MODE1.value,
        ADCMasks.FILTER_BITS.value,
        {
            FilterMode.SINC1.value.op_code: ADCModeValue("sinc-1", FilterMode.SINC1),
            FilterMode.SINC2.value.op_code: ADCModeValue("sinc-2", FilterMode.SINC2),
            FilterMode.SINC3.value.op_code: ADCModeValue("sinc-3", FilterMode.SINC3),
            FilterMode.SINC4.value.op_code: ADCModeValue("sinc-4", FilterMode.SINC4),
            FilterMode.FIR.value.op_code: ADCModeValue("FIR", FilterMode.FIR),
        },
    )
    ADC1_MUXP = ADCMode(
        "adc-1-mux-p",
        ADCReg.REG_INPMUX.value,
        BitMask.HIGH_NIBBLE.value,
        {
            0x00: ADCModeValue(0, ADCChannel.AIN0),
            0x10: ADCModeValue(1, ADCChannel.AIN1),
            0x20: ADCModeValue(2, ADCChannel.AIN2),
            0x30: ADCModeValue(3, ADCChannel.AIN3),
            0x40: ADCModeValue(4, ADCChannel.AIN4),
            0x50: ADCModeValue(5, ADCChannel.AIN5),
            0x60: ADCModeValue(6, ADCChannel.AIN6),
            0x70: ADCModeValue(7, ADCChannel.AIN7),
            0x80: ADCModeValue(8, ADCChannel.AIN8),
            0x90: ADCModeValue(9, ADCChannel.AIN9),
            0xA0: ADCModeValue("AINCOM", ADCChannel.AINCOM),
            0xF0: ADCModeValue("floating", ADCChannel.FLOAT),
        },
    )
    ADC2_MUXP = ADCMode(
        "adc-2-mux-p",
        ADCReg.REG_ADC2MUX.value,
        BitMask.HIGH_NIBBLE.value,
        {
            0x00: ADCModeValue(0, ADCChannel.AIN0),
            0x10: ADCModeValue(1, ADCChannel.AIN1),
            0x20: ADCModeValue(2, ADCChannel.AIN2),
            0x30: ADCModeValue(3, ADCChannel.AIN3),
            0x40: ADCModeValue(4, ADCChannel.AIN4),
            0x50: ADCModeValue(5, ADCChannel.AIN5),
            0x60: ADCModeValue(6, ADCChannel.AIN6),
            0x70: ADCModeValue(7, ADCChannel.AIN7),
            0x80: ADCModeValue(8, ADCChannel.AIN8),
            0x90: ADCModeValue(9, ADCChannel.AIN9),
            0xA0: ADCModeValue("AINCOM", ADCChannel.AINCOM),
            0xF0: ADCModeValue("floating", ADCChannel.FLOAT),
        },
    )
    ADC1_MUXN = ADCMode(
        "adc-1-mux-n",
        ADCReg.REG_INPMUX.value,
        BitMask.LOW_NIBBLE.value,
        {
            0x0: ADCModeValue(0, ADCChannel.AIN0),
            0x1: ADCModeValue(1, ADCChannel.AIN1),
            0x2: ADCModeValue(2, ADCChannel.AIN2),
            0x3: ADCModeValue(3, ADCChannel.AIN3),
            0x4: ADCModeValue(4, ADCChannel.AIN4),
            0x5: ADCModeValue(5, ADCChannel.AIN5),
            0x6: ADCModeValue(6, ADCChannel.AIN6),
            0x7: ADCModeValue(7, ADCChannel.AIN7),
            0x8: ADCModeValue(8, ADCChannel.AIN8),
            0x9: ADCModeValue(9, ADCChannel.AIN9),
            0xA: ADCModeValue("AINCOM", ADCChannel.AINCOM),
            0xF: ADCModeValue("floating", ADCChannel.FLOAT),
        },
    )
    ADC2_MUXN = ADCMode(
        "adc-2-mux-n",
        ADCReg.REG_ADC2MUX.value,
        BitMask.LOW_NIBBLE.value,
        {
            0x0: ADCModeValue(0, ADCChannel.AIN0),
            0x1: ADCModeValue(1, ADCChannel.AIN1),
            0x2: ADCModeValue(2, ADCChannel.AIN2),
            0x3: ADCModeValue(3, ADCChannel.AIN3),
            0x4: ADCModeValue(4, ADCChannel.AIN4),
            0x5: ADCModeValue(5, ADCChannel.AIN5),
            0x6: ADCModeValue(6, ADCChannel.AIN6),
            0x7: ADCModeValue(7, ADCChannel.AIN7),
            0x8: ADCModeValue(8, ADCChannel.AIN8),
            0x9: ADCModeValue(9, ADCChannel.AIN9),
            0xA: ADCModeValue("AINCOM", ADCChannel.AINCOM),
            0xF: ADCModeValue("floating", ADCChannel.FLOAT),
        },
    )
    IDAC1_MUX = ADCMode(
        "idac-1-mux",
        ADCReg.REG_IDACMUX.value,
        BitMask.LOW_NIBBLE.value,
        {
            IDACMUX.IDAC1_AIN0.value.op_code: ADCModeValue(0, IDACMUX.IDAC1_AIN0),
            IDACMUX.IDAC1_AIN1.value.op_code: ADCModeValue(1, IDACMUX.IDAC1_AIN1),
            IDACMUX.IDAC1_AIN2.value.op_code: ADCModeValue(2, IDACMUX.IDAC1_AIN2),
            IDACMUX.IDAC1_AIN3.value.op_code: ADCModeValue(3, IDACMUX.IDAC1_AIN3),
            IDACMUX.IDAC1_AIN4.value.op_code: ADCModeValue(4, IDACMUX.IDAC1_AIN4),
            IDACMUX.IDAC1_AIN5.value.op_code: ADCModeValue(5, IDACMUX.IDAC1_AIN5),
            IDACMUX.IDAC1_AIN6.value.op_code: ADCModeValue(6, IDACMUX.IDAC1_AIN6),
            IDACMUX.IDAC1_AIN7.value.op_code: ADCModeValue(7, IDACMUX.IDAC1_AIN7),
            IDACMUX.IDAC1_AIN8.value.op_code: ADCModeValue(8, IDACMUX.IDAC1_AIN8),
            IDACMUX.IDAC1_AIN9.value.op_code: ADCModeValue(9, IDACMUX.IDAC1_AIN9),
            IDACMUX.IDAC1_AINCOM.value.op_code: ADCModeValue("AINCOM", IDACMUX.IDAC1_AINCOM),
            IDACMUX.IDAC1_NO_CONNECT.value.op_code: ADCModeValue(
                "no-connection", IDACMUX.IDAC1_NO_CONNECT
            ),
        },
    )
    IDAC2_MUX = ADCMode(
        "idac-2-mux",
        ADCReg.REG_IDACMUX.value,
        BitMask.HIGH_NIBBLE.value,
        {
            IDACMUX.IDAC2_AIN0.value.op_code: ADCModeValue(0, IDACMUX.IDAC2_AIN0),
            IDACMUX.IDAC2_AIN1.value.op_code: ADCModeValue(1, IDACMUX.IDAC2_AIN1),
            IDACMUX.IDAC2_AIN2.value.op_code: ADCModeValue(2, IDACMUX.IDAC2_AIN2),
            IDACMUX.IDAC2_AIN3.value.op_code: ADCModeValue(3, IDACMUX.IDAC2_AIN3),
            IDACMUX.IDAC2_AIN4.value.op_code: ADCModeValue(4, IDACMUX.IDAC2_AIN4),
            IDACMUX.IDAC2_AIN5.value.op_code: ADCModeValue(5, IDACMUX.IDAC2_AIN5),
            IDACMUX.IDAC2_AIN6.value.op_code: ADCModeValue(6, IDACMUX.IDAC2_AIN6),
            IDACMUX.IDAC2_AIN7.value.op_code: ADCModeValue(7, IDACMUX.IDAC2_AIN7),
            IDACMUX.IDAC2_AIN8.value.op_code: ADCModeValue(8, IDACMUX.IDAC2_AIN8),
            IDACMUX.IDAC2_AIN9.value.op_code: ADCModeValue(9, IDACMUX.IDAC2_AIN9),
            IDACMUX.IDAC2_AINCOM.value.op_code: ADCModeValue("AINCOM", IDACMUX.IDAC2_AINCOM),
            IDACMUX.IDAC2_NO_CONNECT.value.op_code: ADCModeValue(
                "no-connection", IDACMUX.IDAC2_NO_CONNECT
            ),
        },
    )
    IDAC1_MAG = ADCMode(
        "idac-1-mag",
        ADCReg.REG_IDACMAG.value,
        BitMask.LOW_NIBBLE.value,
        {
            IDACMAG.IDAC1_OFF.value.op_code: ADCModeValue(0, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_50.value.op_code: ADCModeValue(50, IDACMAG.IDAC1_50),
            IDACMAG.IDAC1_100.value.op_code: ADCModeValue(100, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_250.value.op_code: ADCModeValue(250, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_500.value.op_code: ADCModeValue(500, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_750.value.op_code: ADCModeValue(750, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_1000.value.op_code: ADCModeValue(1000, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_1500.value.op_code: ADCModeValue(1500, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_2000.value.op_code: ADCModeValue(2000, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_2500.value.op_code: ADCModeValue(2500, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_3000.value.op_code: ADCModeValue(3000, IDACMAG.IDAC1_OFF),
        },
    )
    IDAC2_MAG = ADCMode(
        "idac-2-mag",
        ADCReg.REG_IDACMAG.value,
        BitMask.HIGH_NIBBLE.value,
        {
            IDACMAG.IDAC2_OFF.value.op_code: ADCModeValue(0, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_50.value.op_code: ADCModeValue(50, IDACMAG.IDAC2_50),
            IDACMAG.IDAC2_100.value.op_code: ADCModeValue(100, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_250.value.op_code: ADCModeValue(250, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_500.value.op_code: ADCModeValue(500, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_750.value.op_code: ADCModeValue(750, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_1000.value.op_code: ADCModeValue(1000, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_1500.value.op_code: ADCModeValue(1500, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_2000.value.op_code: ADCModeValue(2000, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_2500.value.op_code: ADCModeValue(2500, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_3000.value.op_code: ADCModeValue(3000, IDACMAG.IDAC2_OFF),
        },
    )
    REFMUX_POS = ADCMode(
        "ref-mux-positive",
        ADCReg.REG_REFMUX.value,
        ADCMasks.RMUXP_BITS.value,
        {
            REFMUX.POS_REF_INT_2P5.value.op_code: ADCModeValue(
                "2.5 V internal", REFMUX.POS_REF_INT_2P5
            ),
            REFMUX.POS_REF_EXT_AIN0.value.op_code: ADCModeValue(
                "channel 0 external", REFMUX.POS_REF_EXT_AIN0
            ),
            REFMUX.POS_REF_EXT_AIN2.value.op_code: ADCModeValue(
                "channel 2 external", REFMUX.POS_REF_EXT_AIN2
            ),
            REFMUX.POS_REF_EXT_AIN4.value.op_code: ADCModeValue(
                "channel 4 external", REFMUX.POS_REF_EXT_AIN4
            ),
            REFMUX.POS_REF_INT_VAVDD.value.op_code: ADCModeValue("VAVDD", REFMUX.POS_REF_INT_VAVDD),
        },
    )
    REFMUX_NEG = ADCMode(
        "ref-mux-negative",
        ADCReg.REG_REFMUX.value,
        ADCMasks.RMUXN_BITS.value,
        {
            REFMUX.NEG_REF_INT_2P5.value.op_code: ADCModeValue(
                "2.5 V internal", REFMUX.NEG_REF_INT_2P5
            ),
            REFMUX.NEG_REF_EXT_AIN1.value.op_code: ADCModeValue(
                "channel 1 external", REFMUX.NEG_REF_EXT_AIN1
            ),
            REFMUX.NEG_REF_EXT_AIN3.value.op_code: ADCModeValue(
                "channel 3 external", REFMUX.NEG_REF_EXT_AIN3
            ),
            REFMUX.NEG_REF_EXT_AIN5.value.op_code: ADCModeValue(
                "channel 5 external", REFMUX.NEG_REF_EXT_AIN5
            ),
            REFMUX.NEG_REF_INT_VAVSS.value.op_code: ADCModeValue("VAVSS", REFMUX.NEG_REF_INT_VAVSS),
        },
    )


_logger = logging.getLogger(__name__)


def query_state(mode: ADCModes, reg_map: dict[int, int]) -> ADCModeValue:
    """
    Read the current state of configurable ADC properties

    Args:
        `mode` (ADCModes): ADC property whose state is to be read
        `reg_map`: register map formatted as {addx (int): value (int)}

    Returns:
        `ADCModeValue`: information about the current value of this mode
    """
    # value of this mode's register
    reg_value = reg_map[mode.value.addx]

    # get value of bits corresponding to this mode by letting through only the bits
    # that were "masked" when setting this mode (clear all bits except the mode bits)
    mode_bits = (~mode.value.mask) & reg_value

    # name of current value of this mode
    mode_value = mode.value.values[mode_bits]
    _logger.debug(
        (
            f"query_state: query_mode='{mode}', mode_bits={hex(mode_bits)},"
            f" mode_value='{mode_value}'"
        )
    )

    return mode_value
