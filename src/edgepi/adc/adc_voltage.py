"""ADC voltage reading configuration and utility methods"""


import logging

from bitstring import BitArray
from edgepi.adc.adc_constants import ADCReadInfo, ADCNum, ADC1_NUM_DATA_BYTES, ADC2_NUM_DATA_BYTES
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.utilities.utilities import bitstring_from_list


# TODO: retrieve these values from EEPROM once added
STEP_DOWN_RESISTOR_1 = 19.1
STEP_DOWN_RESISTOR_2 = 4.99
REFERENCE_VOLTAGE = 2.5
# Instead of subracting Reference voltage use the code value of the max voltage to convert voltage
ADC1_UPPER_LIMIT = 2147483648
ADC2_UPPER_LIMIT = 8388608


_logger = logging.getLogger(__name__)


def _is_negative_voltage(code: BitArray):
    """
    Determines if voltage code is negative value
    """
    return code[0] == 1


def _code_to_input_voltage(code: int, v_ref: float, num_bits: int):
    """
    Converts digital code obtained from ADC voltage read to
    ADC input voltage (i.e. voltage measured at ADC) based on voltage range
    provided by reference voltage

    Args:
        `code` (int): uint value of ADC voltage read bytes

        `v_ref` (float): ADC reference voltage in Volts

        `num_bits` (int): number of bits in ADC voltage read (24 or 32)
    """
    voltage_range = v_ref / 2 ** (num_bits - 1)
    _logger.debug(f" _code_to_input_voltage: code {code}")
    return float(code) * voltage_range


def _adc_voltage_to_input_voltage(v_in: float, gain: float, offset: float):
    """
    Converts ADC input voltage (i.e. voltage measured at ADC) to
    ADC output voltage (i.e. voltage measured at terminal block)
    """
    step_up_ratio = (STEP_DOWN_RESISTOR_1 + STEP_DOWN_RESISTOR_2) / STEP_DOWN_RESISTOR_2
    return v_in * step_up_ratio * gain + offset


def code_to_voltage(code: list[int], adc_info: ADCReadInfo, calibs: CalibParam) -> float:
    """
    Converts ADC voltage read digital code to output voltage (voltage measured at terminal block)

    Args:
        `code` (list[int]): code bytes retrieved from ADC voltage read

        `adc_info` (ADCReadInfo): data about this adc's voltage reading configuration

        `calibs` (CalibParam): voltage reading gain and offset calibration values

    Returns:
        `float`: voltage value (V) corresponding to `code`
    """
    code_bits = bitstring_from_list(code[:adc_info.num_data_bytes])
    num_bits = adc_info.num_data_bytes * 8
    code_val = code_bits.uint

    if _is_negative_voltage(code_bits):
        code_val = code_val - 2**num_bits

    v_in = _code_to_input_voltage(code_val, REFERENCE_VOLTAGE, num_bits)

    v_out = _adc_voltage_to_input_voltage(v_in, calibs.gain, calibs.offset)

    return v_out

def code_to_voltage_single_ended(code: list[int], adc_info: ADCReadInfo, calibs: CalibParam):
    """
    Converts ADC voltage read digital code to output voltage (voltage measured at terminal block)

    Args:
        `code` (list[int]): code bytes retrieved from ADC voltage read

        `adc_info` (ADCReadInfo): data about this adc's voltage reading configuration

        `calibs` (CalibParam): voltage reading gain and offset calibration values

    Returns:
        `float`: voltage value (V) corresponding to `code`
    """
    code_bits = bitstring_from_list(code[:adc_info.num_data_bytes])
    num_bits = adc_info.num_data_bytes * 8
    code_val = code_bits.uint

    if _is_negative_voltage(code_bits) and adc_info.num_data_bytes == ADC1_NUM_DATA_BYTES:
        code_val = code_val - ADC1_UPPER_LIMIT
    elif _is_negative_voltage(code_bits) and adc_info.num_data_bytes == ADC2_NUM_DATA_BYTES:
        code_val = code_val - ADC2_UPPER_LIMIT
    elif adc_info.num_data_bytes == ADC1_NUM_DATA_BYTES:
        code_val = code_val + ADC1_UPPER_LIMIT
    elif adc_info.num_data_bytes == ADC2_NUM_DATA_BYTES:
        code_val = code_val + ADC2_UPPER_LIMIT

    v_in = _code_to_input_voltage(code_val, REFERENCE_VOLTAGE, num_bits)
    v_out = _adc_voltage_to_input_voltage(v_in, calibs.gain, calibs.offset)

    return v_out

def code_to_temperature(
    code: list[int],
    ref_resistance: float,
    rtd_sensor_resistance: float,
    rtd_sensor_resistance_variation: float,
    rtd_calib_gain: float,
    rtd_calib_offset: float,
    adc_num: ADCNum
    ) -> float:
    """
    Converts ADC voltage read digital code to temperature. Intended for use in RTD sampling.

    Args:
        `code` (list[int]): code bytes retrieved from ADC voltage read

       `ref_resistance` (float): EdgePi-specific RTD reference resistance (Ohms)

       `rtd_sensor_resistance` (float): RTD material-dependent resistance value (Ohms)

       `rtd_sensor_resistance_variation` (float): RTD model-dependent resistance variation (Ohms/°C)

    Returns:
        `float`: temperature value (°C) corresponding to `code`
    """
    code_bits = bitstring_from_list(code)

    # refer to Three-Wire RTD Measurement, Low-Side Reference
    # https://www.ti.com/lit/an/sbaa275a/sbaa275a.pdf?ts=1683111690519&ref_url=https%253A%252F%252Fduckduckgo.com%252F
    number_of_bits = 30 if adc_num == ADCNum.ADC_1 else 22
    r_rtd = code_bits.uint / (2 ** number_of_bits) * ref_resistance
    temperature = (r_rtd - rtd_sensor_resistance) / rtd_sensor_resistance_variation
    _logger.debug(f"computed rtd temperature = {temperature}, from code = {code_bits.uint}")
    temperature = temperature*rtd_calib_gain+rtd_calib_offset
    return temperature
