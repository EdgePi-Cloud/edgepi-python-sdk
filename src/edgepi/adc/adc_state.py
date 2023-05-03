"""ADC State Module"""
from dataclasses import dataclass
import logging

from edgepi.adc.adc_query_lang import PropertyValue, ADCProperties
from edgepi.adc.adc_constants import (
    ADCNum,
    RTDModes,
    ADC1RtdConfig,
    ADC2RtdConfig,
)

_logger = logging.getLogger(__name__)

@dataclass
class ADCReadFields:
    """
    ADC state properties specific to each of ADC1 and ADC2
    """
    conversion_mode: PropertyValue
    data_rate: PropertyValue
    mux_p: PropertyValue
    mux_n: PropertyValue

class ADCState:
    """ADC state intended for reading by users"""
# pylint: disable=too-many-instance-attributes
    def __init__(self, reg_map: dict):
        self.__reg_map = reg_map
        self.adc_1: ADCReadFields = ADCReadFields(
            self.__get_state(ADCProperties.CONV_MODE),
            self.__get_state(ADCProperties.DATA_RATE_1),
            self.__get_state(ADCProperties.ADC1_MUXP),
            self.__get_state(ADCProperties.ADC1_MUXN),
        )
        self.adc_2: ADCReadFields = ADCReadFields(
            PropertyValue("continuous", ADCProperties.CONV_MODE),
            self.__get_state(ADCProperties.DATA_RATE_2),
            self.__get_state(ADCProperties.ADC2_MUXP),
            self.__get_state(ADCProperties.ADC2_MUXN),
        )
        self.filter_mode: PropertyValue = self.__get_state(ADCProperties.FILTER_MODE)
        self.status_byte: PropertyValue = self.__get_state(ADCProperties.STATUS_MODE)
        self.checksum_mode: PropertyValue = self.__get_state(ADCProperties.CHECK_MODE)
        self.rtd_adc: ADCNum = self.__get_rtd_adc_num()
        self.rtd_mode: RTDModes = self.__get_rtd_mode()

    def __query_state(self, adc_property: ADCProperties) -> PropertyValue:
        """
        Read the current state of configurable ADC properties

        Args:
            `adc_property` (ADCProperties): ADC property whose state is to be read
            `reg_map`: register map formatted as {addx (int): value (int)}

        Returns:
            `PropertyValue`: information about the current value of this property
        """
        # value of this adc_property's register
        reg_value = self.__reg_map[adc_property.value.addx]
        # get value of bits corresponding to this property by letting through only the bits
        # that were "masked" when setting this property (clear all bits except the property bits)
        adc_property_bits = (~adc_property.value.mask) & reg_value
        # name of current value of this adc_property
        adc_property_value = adc_property.value.values[adc_property_bits]
        _logger.debug(
            (
                f"query_state: query_property='{adc_property}',"
                " adc_property_bits={hex(adc_property_bits)},"
                f" adc_property_value='{adc_property_value}'"
            )
        )
        return adc_property_value

    def __get_state(self, adc_property: ADCProperties) -> PropertyValue:
        """
        Read the current state of configurable ADC properties. Read both ADC1 and ADC2 configuration
        to verify which one is attached to the RTD

        Args:
            `adc_property` (ADCProperties): ADC property whose state is to be read

        Returns:
            `PropertyValue`: information about the current value of this mode
        """
        return self.__query_state(adc_property)

    def __get_current_rtd_state(self) -> dict[str, PropertyValue]:
        return {
            "adc_1_ch": self.adc_1.mux_p.code,
            "adc_1_mux_n": self.adc_1.mux_n.code,
            "adc_2_ch": self.adc_2.mux_p.code,
            "adc_2_mux_n": self.adc_2.mux_n.code,
            "idac_1_mux": self.__get_state(ADCProperties.IDAC1_MUX).code,
            "idac_2_mux": self.__get_state(ADCProperties.IDAC2_MUX).code,
            "idac_1_mag": self.__get_state(ADCProperties.IDAC1_MAG).code,
            "idac_2_mag": self.__get_state(ADCProperties.IDAC2_MAG).code,
            "pos_ref_inp": self.__get_state(ADCProperties.REFMUX_POS).code,
            "neg_ref_inp": self.__get_state(ADCProperties.REFMUX_NEG).code,
            "adc2_ref_inp": self.__get_state(ADCProperties.ADC2_REFMUX).code,
        }

    def __get_rtd_adc_num(self):
        """
        Get the number of ADC that is attached to RTD
        """
        rtd_state = self.__get_current_rtd_state()
        is_rtd_off = all(rtd_state.get(key)== value for key,value in RTDModes.RTD_OFF.value.items())
        if is_rtd_off:
            return None

        if all(rtd_state.get(key) == value for key, value in\
               (RTDModes.RTD_ON.value | ADC1RtdConfig.ON.value).items()):
            return ADCNum.ADC_1

        if all(rtd_state.get(key) == value for key, value in\
              (RTDModes.RTD_ON.value | ADC2RtdConfig.ON.value).items()):
            return ADCNum.ADC_2

        return None

    def __get_rtd_mode(self):
        """
        Get on/off RTD mode.
        Returns:
            RTDModes (Enum): RTD_ON when RTD is on, RTD_OFF, when RTD is off, and None for undefined
                             configuration.
        """
        # This is assuming, idac_1_mux - adc2_ref_inp are modified only when RTD is enabled.
        # compare the current rtd_state to RTDMode.RTD_OFF.value dictionary. If it doesn't match,
        # it means RTD is enabled

        if self.rtd_adc in set(ADCNum):
            return RTDModes.RTD_ON
        rtd_state = self.__get_current_rtd_state()
        if all(rtd_state.get(key)==value for key,value in RTDModes.RTD_OFF.value.items()):
            return RTDModes.RTD_OFF
        return None
