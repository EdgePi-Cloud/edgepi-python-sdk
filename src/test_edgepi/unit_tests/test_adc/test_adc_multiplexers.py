"""" Unit tests for adc_multiplexers.py """


from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.adc.adc_constants import ADCChannel as CH, ADCReg
from edgepi.adc.adc_multiplexers import (
    _validate_mux_mapping,
    ChannelMappingError,
)


@pytest.mark.parametrize("mux_regs, expected", [
    (
        {
            ADCReg.REG_INPMUX: (CH.AIN0.value, CH.AIN1.value),
            ADCReg.REG_ADC2MUX: (CH.AIN2.value, CH.AIN3.value),
        },
        does_not_raise()
    ),
    (
        {
            ADCReg.REG_INPMUX: (CH.AIN0.value, CH.AIN0.value),
            ADCReg.REG_ADC2MUX: (CH.AIN2.value, CH.AIN3.value),
        },
        pytest.raises(ChannelMappingError)
    ),
    (
        {
            ADCReg.REG_INPMUX: (CH.AIN0.value, CH.AIN1.value),
            ADCReg.REG_ADC2MUX: (CH.AIN2.value, CH.AIN2.value),
        },
        pytest.raises(ChannelMappingError)
    ),
    (
        {
            ADCReg.REG_INPMUX: (CH.AIN0.value, CH.AIN1.value),
            ADCReg.REG_ADC2MUX: (CH.AIN2.value, CH.AIN0.value),
        },
        pytest.raises(ChannelMappingError)
    ),
    (
        {
            ADCReg.REG_INPMUX: (CH.AIN0.value, CH.AIN2.value),
            ADCReg.REG_ADC2MUX: (CH.AIN2.value, CH.AIN1.value),
        },
        pytest.raises(ChannelMappingError)
    ),
    (
        {
            ADCReg.REG_INPMUX: (CH.AIN0.value, CH.AIN2.value),
            ADCReg.REG_ADC2MUX: (CH.AIN0.value, CH.AIN1.value),
        },
        pytest.raises(ChannelMappingError)
    ),
    (
        {
            ADCReg.REG_INPMUX: (CH.AIN0.value, CH.AIN1.value),
            ADCReg.REG_ADC2MUX: (CH.AIN2.value, CH.AIN1.value),
        },
        pytest.raises(ChannelMappingError)
    ),
])
def test_validate_mux_mapping(mux_regs, expected):
    with expected:
        _validate_mux_mapping(mux_regs)
