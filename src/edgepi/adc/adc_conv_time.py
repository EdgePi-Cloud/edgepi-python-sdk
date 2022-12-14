"""Utility module for computing ADC conversion delay time"""

# ADC conversion delay time is affected by the following factors:
# - Conversion delay (REG_MODE0) -> currently not user-configurable
# - Digital filter mode (REG_MODE1)
# - Data rate mode (REG_MODE2)
# - IDAC/Chop mode (REG_MODE0) -> currently not user-configurable


from edgepi.adc.adc_constants import (
    FilterMode as FILT,
    ADC1DataRate as DR1,
    ADC2DataRate as DR2,
    ADCNum,
)


# pulse conversion delay times for ADC1, or first conversion delay time for continuous conversions
ADC1_INITIAL_DELAYS = {
    DR1.SPS_2P5.value.op_code: {
        FILT.SINC1.value.op_code: 400.4,
        FILT.SINC2.value.op_code: 800.4,
        FILT.SINC3.value.op_code: 1200.0,
        FILT.SINC4.value.op_code: 1600.0,
        FILT.FIR.value.op_code: 402.4,
    },
    DR1.SPS_5.value.op_code: {
        FILT.SINC1.value.op_code: 200.4,
        FILT.SINC2.value.op_code: 400.4,
        FILT.SINC3.value.op_code: 600.4,
        FILT.SINC4.value.op_code: 800.4,
        FILT.FIR.value.op_code: 202.2,
    },
    DR1.SPS_10.value.op_code: {
        FILT.SINC1.value.op_code: 100.4,
        FILT.SINC2.value.op_code: 200.4,
        FILT.SINC3.value.op_code: 300.4,
        FILT.SINC4.value.op_code: 400.4,
        FILT.FIR.value.op_code: 102.2,
    },
    DR1.SPS_16P6.value.op_code: {
        FILT.SINC1.value.op_code: 60.35,
        FILT.SINC2.value.op_code: 120.4,
        FILT.SINC3.value.op_code: 180.4,
        FILT.SINC4.value.op_code: 240.4,
        FILT.FIR.value.op_code: 60.35,
    },
    DR1.SPS_20.value.op_code: {
        FILT.SINC1.value.op_code: 50.35,
        FILT.SINC2.value.op_code: 100.4,
        FILT.SINC3.value.op_code: 150.4,
        FILT.SINC4.value.op_code: 200.4,
        FILT.FIR.value.op_code: 52.22,
    },
    DR1.SPS_50.value.op_code: {
        FILT.SINC1.value.op_code: 20.35,
        FILT.SINC2.value.op_code: 40.42,
        FILT.SINC3.value.op_code: 60.42,
        FILT.SINC4.value.op_code: 80.42,
        FILT.FIR.value.op_code: 20.35,
    },
    DR1.SPS_60.value.op_code: {
        FILT.SINC1.value.op_code: 17.02,
        FILT.SINC2.value.op_code: 33.76,
        FILT.SINC3.value.op_code: 50.42,
        FILT.SINC4.value.op_code: 67.09,
        FILT.FIR.value.op_code: 17.02,
    },
    DR1.SPS_100.value.op_code: {
        FILT.SINC1.value.op_code: 10.35,
        FILT.SINC2.value.op_code: 20.42,
        FILT.SINC3.value.op_code: 30.42,
        FILT.SINC4.value.op_code: 40.42,
        FILT.FIR.value.op_code: 10.35,
    },
    DR1.SPS_400.value.op_code: {
        FILT.SINC1.value.op_code: 2.855,
        FILT.SINC2.value.op_code: 5.424,
        FILT.SINC3.value.op_code: 7.924,
        FILT.SINC4.value.op_code: 10.42,
        FILT.FIR.value.op_code: 2.855,
    },
    DR1.SPS_1200.value.op_code: {
        FILT.SINC1.value.op_code: 1.188,
        FILT.SINC2.value.op_code: 2.091,
        FILT.SINC3.value.op_code: 2.924,
        FILT.SINC4.value.op_code: 3.758,
        FILT.FIR.value.op_code: 1.188,
    },
    DR1.SPS_2400.value.op_code: {
        FILT.SINC1.value.op_code: 0.771,
        FILT.SINC2.value.op_code: 1.258,
        FILT.SINC3.value.op_code: 1.674,
        FILT.SINC4.value.op_code: 2.091,
        FILT.FIR.value.op_code: 0.771,
    },
    DR1.SPS_4800.value.op_code: {
        FILT.SINC1.value.op_code: 0.563,
        FILT.SINC2.value.op_code: 0.8409,
        FILT.SINC3.value.op_code: 1.049,
        FILT.SINC4.value.op_code: 1.258,
        FILT.FIR.value.op_code: 0.563,
    },
    DR1.SPS_7200.value.op_code: {
        FILT.SINC1.value.op_code: 0.494,
        FILT.SINC2.value.op_code: 0.702,
        FILT.SINC3.value.op_code: 0.841,
        FILT.SINC4.value.op_code: 0.980,
        FILT.FIR.value.op_code: 0.494,
    },
    DR1.SPS_14400.value.op_code: {
        FILT.SINC1.value.op_code: 0.424,
        FILT.SINC2.value.op_code: 0.424,
        FILT.SINC3.value.op_code: 0.424,
        FILT.SINC4.value.op_code: 0.424,
        FILT.FIR.value.op_code: 0.424,
    },
    DR1.SPS_19200.value.op_code: {
        FILT.SINC1.value.op_code: 0.337,
        FILT.SINC2.value.op_code: 0.337,
        FILT.SINC3.value.op_code: 0.337,
        FILT.SINC4.value.op_code: 0.337,
        FILT.FIR.value.op_code: 0.337,
    },
    DR1.SPS_38400.value.op_code: {
        FILT.SINC1.value.op_code: 0.207,
        FILT.SINC2.value.op_code: 0.207,
        FILT.SINC3.value.op_code: 0.207,
        FILT.SINC4.value.op_code: 0.207,
        FILT.FIR.value.op_code: 0.207,
    },
}


# ADC1 continuous conversion delay times, for conversions 2..n (following first conversion)
ADC1_CONT_DELAYS = {
    DR1.SPS_2P5.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_2P5.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_5.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_5.value.op_code][FILT.SINC1.value.op_code],
    DR1.SPS_10.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_10.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_16P6.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_16P6.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_20.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_20.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_50.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_50.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_60.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_60.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_100.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_100.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_400.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_400.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_1200.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_1200.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_2400.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_2400.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_4800.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_4800.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_7200.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_7200.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_14400.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_14400.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_19200.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_19200.value.op_code][
        FILT.SINC1.value.op_code
    ],
    DR1.SPS_38400.value.op_code: ADC1_INITIAL_DELAYS[DR1.SPS_38400.value.op_code][
        FILT.SINC1.value.op_code
    ],
}


# continuous conversion delay times for ADC2 (ADC2 only uses continuous mode)
ADC2_DELAYS = {
    DR2.SPS_10.value.op_code: 121,
    DR2.SPS_100.value.op_code: 31.2,
    DR2.SPS_400.value.op_code: 8.71,
    DR2.SPS_800.value.op_code: 4.97,
}


def expected_initial_time_delay(adc_num: ADCNum, data_rate: int, filter_mode: int):
    """
    Computes conversion latency (ms) based on ADC configuration
    for PULSE mode reads or initial read in CONTINUOUS mode.

    Args:
        `adc_num` (ADCNum): ADC whose conversions are being sampled

        `data_rate` (int): opcode value of data rate bits

        `filter_mode` (int): opcode value of filter mode bits

    Returns:
        `float`: conversion delay in milliseconds (ms)
    """
    if adc_num == ADCNum.ADC_1:
        # this is the initial delay for both pulse and continuous modes
        return ADC1_INITIAL_DELAYS[data_rate][filter_mode]

    # no initial figures given in documentation, but estimate initial delay
    # is 3 times longer than subsequent conversion delays
    return ADC2_DELAYS[data_rate] * 3


def expected_continuous_time_delay(adc_num: ADCNum, data_rate: int):
    """
    Computes conversion latency (ms) based on ADC configuration
    for reads 2...n in continuous conversion mode.

    Args:
        `adc_num` (ADCNum): ADC whose conversions are being sampled

        `data_rate` (int): opcode value of data rate bits

    Returns:
        `float`: conversion delay in milliseconds (ms)
    """
    if adc_num == ADCNum.ADC_1:
        return ADC1_CONT_DELAYS[data_rate]

    return ADC2_DELAYS[data_rate]
