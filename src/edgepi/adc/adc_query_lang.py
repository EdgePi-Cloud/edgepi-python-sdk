"""
For ADC state querying
"""

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
class PropertyValue:
    """
    Stores information about a specific value of an ADC functional adc_property

    Attributes
        `value` (any): user-friendly description of this adc_property value
        `code` (Enum): internal code used to set this adc_property value
    """

    value: Any
    code: Enum

    def __repr__(self) -> str:
        return f"value: {self.value}, code: {self.code}"


@dataclass
class Property:
    """Stores information about an ADC functional adc_property"""

    name: str
    addx: int
    mask: int
    values: dict[int, PropertyValue]


class ADCProperties(Enum):
    """Address and mask values for ADC properties"""

    CONV_MODE = Property(
        "conversion-adc_property",
        ADCReg.REG_MODE0.value,
        BitMask.BIT6.value,
        {
            ConvMode.PULSE.value.op_code: PropertyValue("pulse", ConvMode.PULSE),
            ConvMode.CONTINUOUS.value.op_code: PropertyValue("continuous", ConvMode.CONTINUOUS),
        },
    )
    CHECK_MODE = Property(
        "checksum-byte-adc_property",
        ADCReg.REG_INTERFACE.value,
        ADCMasks.CHECK_BITS.value,
        {
            CheckMode.CHECK_BYTE_OFF.value.op_code: PropertyValue("off", CheckMode.CHECK_BYTE_OFF),
            CheckMode.CHECK_BYTE_CHK.value.op_code: PropertyValue(
                "checksum", CheckMode.CHECK_BYTE_CHK
            ),
            CheckMode.CHECK_BYTE_CRC.value.op_code: PropertyValue("crc", CheckMode.CHECK_BYTE_CRC),
        },
    )
    STATUS_MODE = Property(
        "status-byte-adc_property",
        ADCReg.REG_INTERFACE.value,
        BitMask.BIT2.value,
        {
            StatusByte.STATUS_BYTE_OFF.value.op_code: PropertyValue(
                "off", StatusByte.STATUS_BYTE_OFF
            ),
            StatusByte.STATUS_BYTE_ON.value.op_code: PropertyValue("on", StatusByte.STATUS_BYTE_ON),
        },
    )
    DATA_RATE_1 = Property(
        "data-rate-adc-1",
        ADCReg.REG_MODE2.value,
        BitMask.LOW_NIBBLE.value,
        {
            ADC1DataRate.SPS_2P5.value.op_code: PropertyValue(2.5, ADC1DataRate.SPS_2P5),
            ADC1DataRate.SPS_5.value.op_code: PropertyValue(5, ADC1DataRate.SPS_5),
            ADC1DataRate.SPS_10.value.op_code: PropertyValue(10, ADC1DataRate.SPS_10),
            ADC1DataRate.SPS_16P6.value.op_code: PropertyValue(16.6, ADC1DataRate.SPS_16P6),
            ADC1DataRate.SPS_20.value.op_code: PropertyValue(20, ADC1DataRate.SPS_20),
            ADC1DataRate.SPS_50.value.op_code: PropertyValue(50, ADC1DataRate.SPS_50),
            ADC1DataRate.SPS_60.value.op_code: PropertyValue(60, ADC1DataRate.SPS_60),
            ADC1DataRate.SPS_100.value.op_code: PropertyValue(100, ADC1DataRate.SPS_100),
            ADC1DataRate.SPS_400.value.op_code: PropertyValue(400, ADC1DataRate.SPS_400),
            ADC1DataRate.SPS_1200.value.op_code: PropertyValue(1200, ADC1DataRate.SPS_1200),
            ADC1DataRate.SPS_2400.value.op_code: PropertyValue(2400, ADC1DataRate.SPS_2400),
            ADC1DataRate.SPS_4800.value.op_code: PropertyValue(4800, ADC1DataRate.SPS_4800),
            ADC1DataRate.SPS_7200.value.op_code: PropertyValue(7200, ADC1DataRate.SPS_7200),
            ADC1DataRate.SPS_14400.value.op_code: PropertyValue(14400, ADC1DataRate.SPS_14400),
            ADC1DataRate.SPS_19200.value.op_code: PropertyValue(19200, ADC1DataRate.SPS_19200),
            ADC1DataRate.SPS_38400.value.op_code: PropertyValue(38400, ADC1DataRate.SPS_38400),
        },
    )
    DATA_RATE_2 = Property(
        "data-rate-adc-2",
        ADCReg.REG_ADC2CFG.value,
        ADCMasks.ADC2_DR_BITS.value,
        {
            ADC2DataRate.SPS_10.value.op_code: PropertyValue(10, ADC2DataRate.SPS_10),
            ADC2DataRate.SPS_100.value.op_code: PropertyValue(10, ADC2DataRate.SPS_100),
            ADC2DataRate.SPS_400.value.op_code: PropertyValue(400, ADC2DataRate.SPS_400),
            ADC2DataRate.SPS_800.value.op_code: PropertyValue(800, ADC2DataRate.SPS_800),
        },
    )
    FILTER_MODE = Property(
        "filter-adc_property",
        ADCReg.REG_MODE1.value,
        ADCMasks.FILTER_BITS.value,
        {
            FilterMode.SINC1.value.op_code: PropertyValue("sinc-1", FilterMode.SINC1),
            FilterMode.SINC2.value.op_code: PropertyValue("sinc-2", FilterMode.SINC2),
            FilterMode.SINC3.value.op_code: PropertyValue("sinc-3", FilterMode.SINC3),
            FilterMode.SINC4.value.op_code: PropertyValue("sinc-4", FilterMode.SINC4),
            FilterMode.FIR.value.op_code: PropertyValue("FIR", FilterMode.FIR),
        },
    )
    ADC1_MUXP = Property(
        "adc-1-mux-p",
        ADCReg.REG_INPMUX.value,
        BitMask.HIGH_NIBBLE.value,
        {
            0x00: PropertyValue(0, ADCChannel.AIN0),
            0x10: PropertyValue(1, ADCChannel.AIN1),
            0x20: PropertyValue(2, ADCChannel.AIN2),
            0x30: PropertyValue(3, ADCChannel.AIN3),
            0x40: PropertyValue(4, ADCChannel.AIN4),
            0x50: PropertyValue(5, ADCChannel.AIN5),
            0x60: PropertyValue(6, ADCChannel.AIN6),
            0x70: PropertyValue(7, ADCChannel.AIN7),
            0x80: PropertyValue(8, ADCChannel.AIN8),
            0x90: PropertyValue(9, ADCChannel.AIN9),
            0xA0: PropertyValue("AINCOM", ADCChannel.AINCOM),
            0xF0: PropertyValue("floating", ADCChannel.FLOAT),
        },
    )
    ADC2_MUXP = Property(
        "adc-2-mux-p",
        ADCReg.REG_ADC2MUX.value,
        BitMask.HIGH_NIBBLE.value,
        {
            0x00: PropertyValue(0, ADCChannel.AIN0),
            0x10: PropertyValue(1, ADCChannel.AIN1),
            0x20: PropertyValue(2, ADCChannel.AIN2),
            0x30: PropertyValue(3, ADCChannel.AIN3),
            0x40: PropertyValue(4, ADCChannel.AIN4),
            0x50: PropertyValue(5, ADCChannel.AIN5),
            0x60: PropertyValue(6, ADCChannel.AIN6),
            0x70: PropertyValue(7, ADCChannel.AIN7),
            0x80: PropertyValue(8, ADCChannel.AIN8),
            0x90: PropertyValue(9, ADCChannel.AIN9),
            0xA0: PropertyValue("AINCOM", ADCChannel.AINCOM),
            0xF0: PropertyValue("floating", ADCChannel.FLOAT),
        },
    )
    ADC1_MUXN = Property(
        "adc-1-mux-n",
        ADCReg.REG_INPMUX.value,
        BitMask.LOW_NIBBLE.value,
        {
            0x0: PropertyValue(0, ADCChannel.AIN0),
            0x1: PropertyValue(1, ADCChannel.AIN1),
            0x2: PropertyValue(2, ADCChannel.AIN2),
            0x3: PropertyValue(3, ADCChannel.AIN3),
            0x4: PropertyValue(4, ADCChannel.AIN4),
            0x5: PropertyValue(5, ADCChannel.AIN5),
            0x6: PropertyValue(6, ADCChannel.AIN6),
            0x7: PropertyValue(7, ADCChannel.AIN7),
            0x8: PropertyValue(8, ADCChannel.AIN8),
            0x9: PropertyValue(9, ADCChannel.AIN9),
            0xA: PropertyValue("AINCOM", ADCChannel.AINCOM),
            0xF: PropertyValue("floating", ADCChannel.FLOAT),
        },
    )
    ADC2_MUXN = Property(
        "adc-2-mux-n",
        ADCReg.REG_ADC2MUX.value,
        BitMask.LOW_NIBBLE.value,
        {
            0x0: PropertyValue(0, ADCChannel.AIN0),
            0x1: PropertyValue(1, ADCChannel.AIN1),
            0x2: PropertyValue(2, ADCChannel.AIN2),
            0x3: PropertyValue(3, ADCChannel.AIN3),
            0x4: PropertyValue(4, ADCChannel.AIN4),
            0x5: PropertyValue(5, ADCChannel.AIN5),
            0x6: PropertyValue(6, ADCChannel.AIN6),
            0x7: PropertyValue(7, ADCChannel.AIN7),
            0x8: PropertyValue(8, ADCChannel.AIN8),
            0x9: PropertyValue(9, ADCChannel.AIN9),
            0xA: PropertyValue("AINCOM", ADCChannel.AINCOM),
            0xF: PropertyValue("floating", ADCChannel.FLOAT),
        },
    )
    IDAC1_MUX = Property(
        "idac-1-mux",
        ADCReg.REG_IDACMUX.value,
        BitMask.LOW_NIBBLE.value,
        {
            IDACMUX.IDAC1_AIN0.value.op_code: PropertyValue(0, IDACMUX.IDAC1_AIN0),
            IDACMUX.IDAC1_AIN1.value.op_code: PropertyValue(1, IDACMUX.IDAC1_AIN1),
            IDACMUX.IDAC1_AIN2.value.op_code: PropertyValue(2, IDACMUX.IDAC1_AIN2),
            IDACMUX.IDAC1_AIN3.value.op_code: PropertyValue(3, IDACMUX.IDAC1_AIN3),
            IDACMUX.IDAC1_AIN4.value.op_code: PropertyValue(4, IDACMUX.IDAC1_AIN4),
            IDACMUX.IDAC1_AIN5.value.op_code: PropertyValue(5, IDACMUX.IDAC1_AIN5),
            IDACMUX.IDAC1_AIN6.value.op_code: PropertyValue(6, IDACMUX.IDAC1_AIN6),
            IDACMUX.IDAC1_AIN7.value.op_code: PropertyValue(7, IDACMUX.IDAC1_AIN7),
            IDACMUX.IDAC1_AIN8.value.op_code: PropertyValue(8, IDACMUX.IDAC1_AIN8),
            IDACMUX.IDAC1_AIN9.value.op_code: PropertyValue(9, IDACMUX.IDAC1_AIN9),
            IDACMUX.IDAC1_AINCOM.value.op_code: PropertyValue("AINCOM", IDACMUX.IDAC1_AINCOM),
            IDACMUX.IDAC1_NO_CONNECT.value.op_code: PropertyValue(
                "no-connection", IDACMUX.IDAC1_NO_CONNECT
            ),
        },
    )
    IDAC2_MUX = Property(
        "idac-2-mux",
        ADCReg.REG_IDACMUX.value,
        BitMask.HIGH_NIBBLE.value,
        {
            IDACMUX.IDAC2_AIN0.value.op_code: PropertyValue(0, IDACMUX.IDAC2_AIN0),
            IDACMUX.IDAC2_AIN1.value.op_code: PropertyValue(1, IDACMUX.IDAC2_AIN1),
            IDACMUX.IDAC2_AIN2.value.op_code: PropertyValue(2, IDACMUX.IDAC2_AIN2),
            IDACMUX.IDAC2_AIN3.value.op_code: PropertyValue(3, IDACMUX.IDAC2_AIN3),
            IDACMUX.IDAC2_AIN4.value.op_code: PropertyValue(4, IDACMUX.IDAC2_AIN4),
            IDACMUX.IDAC2_AIN5.value.op_code: PropertyValue(5, IDACMUX.IDAC2_AIN5),
            IDACMUX.IDAC2_AIN6.value.op_code: PropertyValue(6, IDACMUX.IDAC2_AIN6),
            IDACMUX.IDAC2_AIN7.value.op_code: PropertyValue(7, IDACMUX.IDAC2_AIN7),
            IDACMUX.IDAC2_AIN8.value.op_code: PropertyValue(8, IDACMUX.IDAC2_AIN8),
            IDACMUX.IDAC2_AIN9.value.op_code: PropertyValue(9, IDACMUX.IDAC2_AIN9),
            IDACMUX.IDAC2_AINCOM.value.op_code: PropertyValue("AINCOM", IDACMUX.IDAC2_AINCOM),
            IDACMUX.IDAC2_NO_CONNECT.value.op_code: PropertyValue(
                "no-connection", IDACMUX.IDAC2_NO_CONNECT
            ),
        },
    )
    IDAC1_MAG = Property(
        "idac-1-mag",
        ADCReg.REG_IDACMAG.value,
        BitMask.LOW_NIBBLE.value,
        {
            IDACMAG.IDAC1_OFF.value.op_code: PropertyValue(0, IDACMAG.IDAC1_OFF),
            IDACMAG.IDAC1_50.value.op_code: PropertyValue(50, IDACMAG.IDAC1_50),
            IDACMAG.IDAC1_100.value.op_code: PropertyValue(100, IDACMAG.IDAC1_100),
            IDACMAG.IDAC1_250.value.op_code: PropertyValue(250, IDACMAG.IDAC1_250),
            IDACMAG.IDAC1_500.value.op_code: PropertyValue(500, IDACMAG.IDAC1_500),
            IDACMAG.IDAC1_750.value.op_code: PropertyValue(750, IDACMAG.IDAC1_750),
            IDACMAG.IDAC1_1000.value.op_code: PropertyValue(1000, IDACMAG.IDAC1_1000),
            IDACMAG.IDAC1_1500.value.op_code: PropertyValue(1500, IDACMAG.IDAC1_1500),
            IDACMAG.IDAC1_2000.value.op_code: PropertyValue(2000, IDACMAG.IDAC1_2000),
            IDACMAG.IDAC1_2500.value.op_code: PropertyValue(2500, IDACMAG.IDAC1_2500),
            IDACMAG.IDAC1_3000.value.op_code: PropertyValue(3000, IDACMAG.IDAC1_3000),
        },
    )
    IDAC2_MAG = Property(
        "idac-2-mag",
        ADCReg.REG_IDACMAG.value,
        BitMask.HIGH_NIBBLE.value,
        {
            IDACMAG.IDAC2_OFF.value.op_code: PropertyValue(0, IDACMAG.IDAC2_OFF),
            IDACMAG.IDAC2_50.value.op_code: PropertyValue(50, IDACMAG.IDAC2_50),
            IDACMAG.IDAC2_100.value.op_code: PropertyValue(100, IDACMAG.IDAC2_100),
            IDACMAG.IDAC2_250.value.op_code: PropertyValue(250, IDACMAG.IDAC2_250),
            IDACMAG.IDAC2_500.value.op_code: PropertyValue(500, IDACMAG.IDAC2_500),
            IDACMAG.IDAC2_750.value.op_code: PropertyValue(750, IDACMAG.IDAC2_750),
            IDACMAG.IDAC2_1000.value.op_code: PropertyValue(1000, IDACMAG.IDAC2_1000),
            IDACMAG.IDAC2_1500.value.op_code: PropertyValue(1500, IDACMAG.IDAC2_1500),
            IDACMAG.IDAC2_2000.value.op_code: PropertyValue(2000, IDACMAG.IDAC2_2000),
            IDACMAG.IDAC2_2500.value.op_code: PropertyValue(2500, IDACMAG.IDAC2_2500),
            IDACMAG.IDAC2_3000.value.op_code: PropertyValue(3000, IDACMAG.IDAC2_3000),
        },
    )
    REFMUX_POS = Property(
        "ref-mux-positive",
        ADCReg.REG_REFMUX.value,
        ADCMasks.RMUXP_BITS.value,
        {
            REFMUX.POS_REF_INT_2P5.value.op_code: PropertyValue(
                "2.5 V internal", REFMUX.POS_REF_INT_2P5
            ),
            REFMUX.POS_REF_EXT_AIN0.value.op_code: PropertyValue(
                "channel 0 external", REFMUX.POS_REF_EXT_AIN0
            ),
            REFMUX.POS_REF_EXT_AIN2.value.op_code: PropertyValue(
                "channel 2 external", REFMUX.POS_REF_EXT_AIN2
            ),
            REFMUX.POS_REF_EXT_AIN4.value.op_code: PropertyValue(
                "channel 4 external", REFMUX.POS_REF_EXT_AIN4
            ),
            REFMUX.POS_REF_INT_VAVDD.value.op_code: PropertyValue(
                "VAVDD", REFMUX.POS_REF_INT_VAVDD
            ),
        },
    )
    REFMUX_NEG = Property(
        "ref-mux-negative",
        ADCReg.REG_REFMUX.value,
        ADCMasks.RMUXN_BITS.value,
        {
            REFMUX.NEG_REF_INT_2P5.value.op_code: PropertyValue(
                "2.5 V internal", REFMUX.NEG_REF_INT_2P5
            ),
            REFMUX.NEG_REF_EXT_AIN1.value.op_code: PropertyValue(
                "channel 1 external", REFMUX.NEG_REF_EXT_AIN1
            ),
            REFMUX.NEG_REF_EXT_AIN3.value.op_code: PropertyValue(
                "channel 3 external", REFMUX.NEG_REF_EXT_AIN3
            ),
            REFMUX.NEG_REF_EXT_AIN5.value.op_code: PropertyValue(
                "channel 5 external", REFMUX.NEG_REF_EXT_AIN5
            ),
            REFMUX.NEG_REF_INT_VAVSS.value.op_code: PropertyValue(
                "VAVSS", REFMUX.NEG_REF_INT_VAVSS
            ),
        },
    )
