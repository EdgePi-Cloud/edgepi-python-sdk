"""
For ADC state querying
"""

from dataclasses import dataclass
from typing import Any
from enum import Enum

from edgepi.adc.adc_constants import (
    IDACMUX,
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
            StatusByte.STATUS_BYTE_OFF.value.op_code: "off",
            StatusByte.STATUS_BYTE_ON.value.op_code: "on",
        },
    )
    DATA_RATE_1 = ADCMode(
        "data-rate-adc-1",
        ADCReg.REG_MODE2.value,
        BitMask.LOW_NIBBLE.value,
        {
            ADC1DataRate.SPS_2P5.value.op_code: "2.5-sps",
            ADC1DataRate.SPS_5.value.op_code: "5-sps",
            ADC1DataRate.SPS_10.value.op_code: "10-sps",
            ADC1DataRate.SPS_16P6.value.op_code: "16.6-sps",
            ADC1DataRate.SPS_20.value.op_code: "20-sps",
            ADC1DataRate.SPS_50.value.op_code: "50-sps",
            ADC1DataRate.SPS_60.value.op_code: "60-sps",
            ADC1DataRate.SPS_100.value.op_code: "100-sps",
            ADC1DataRate.SPS_400.value.op_code: "400-sps",
            ADC1DataRate.SPS_1200.value.op_code: "1200-sps",
            ADC1DataRate.SPS_2400.value.op_code: "2400-sps",
            ADC1DataRate.SPS_4800.value.op_code: "4800-sps",
            ADC1DataRate.SPS_7200.value.op_code: "7200-sps",
            ADC1DataRate.SPS_14400.value.op_code: "14400-sps",
            ADC1DataRate.SPS_19200.value.op_code: "19200-sps",
            ADC1DataRate.SPS_38400.value.op_code: "38400-sps",
        },
    )
    DATA_RATE_2 = ADCMode(
        "data-rate-adc-2",
        ADCReg.REG_ADC2CFG.value,
        ADCMasks.ADC2_DR_BITS.value,
        {
            ADC2DataRate.SPS_10.value.op_code: "10-sps",
            ADC2DataRate.SPS_100.value.op_code: "100-sps",
            ADC2DataRate.SPS_400.value.op_code: "400-sps",
            ADC2DataRate.SPS_800.value.op_code: "800-sps",
        },
    )
    FILTER_MODE = ADCMode(
        "filter-mode",
        ADCReg.REG_MODE1.value,
        ADCMasks.FILTER_BITS.value,
        {
            FilterMode.SINC1.value.op_code: "sinc-1",
            FilterMode.SINC2.value.op_code: "sinc-2",
            FilterMode.SINC3.value.op_code: "sinc-3",
            FilterMode.SINC4.value.op_code: "sinc-4",
            FilterMode.FIR.value.op_code: "fir",
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
