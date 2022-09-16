"""ADC voltage reading configuration and utility methods"""


from bitstring import BitArray


# TODO: retrieve these values from EEPROM once added
STEP_DOWN_RESISTOR_1 = 19.1
STEP_DOWN_RESISTOR_2 = 4.99


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
    """
    voltage_range = v_ref / 2 ** (num_bits - 1)
    return float(code) * voltage_range


def _input_voltage_to_output_voltage(v_in: float, gain: float, offset: float):
    """
    Converts ADC input voltage (i.e. voltage measured at ADC) to
    ADC output voltage (i.e. voltage measured at terminal block)
    """
    step_up_ratio = (STEP_DOWN_RESISTOR_1 + STEP_DOWN_RESISTOR_2) / STEP_DOWN_RESISTOR_2
    return v_in * step_up_ratio * gain - offset


def code_to_voltage(code: BitArray, adc_info):
    """
    Converts ADC voltage read digital code to output voltage (voltage measured at terminal block)

    Args:
        code (BitArray): bitstring representation of digital code retrieved from ADC voltage read

        adc_info (ADCReadInfo): data about this adc's voltage reading configuration
    """
    num_bits = adc_info.num_data_bytes * 8
    config = adc_info.voltage_config

    # code is given in 2's complement, remove leading 1
    if _is_negative_voltage(code):
        code[0] = 0

    v_in = _code_to_input_voltage(code.uint, config.v_ref, num_bits)

    v_out = _input_voltage_to_output_voltage(v_in, config.gain, config.offset)

    return code, v_in, v_out
