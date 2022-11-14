import pytest

from edgepi.adc.edgepi_adc import ADCState, EdgePiADC
from edgepi.adc.adc_query_lang import ADCProperties, PropertyValue
from edgepi.adc.adc_constants import (
    IDACMAG,
    IDACMUX,
    REFMUX,
    ADCChannel,
    ADCReg,
    CheckMode,
    ConvMode,
    FilterMode,
    StatusByte,
)

# pylint: disable=protected-access
@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    adc = EdgePiADC(enable_cache=False)
    yield adc


# TODO: Test EdgePi Unit unavailable, these tests have not been run yet
@pytest.mark.parametrize("updates, state_property, expected", [
    # ADC1 MUX_P
    (
        {"adc_1_analog_in": ADCChannel.AIN0},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN0.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN1},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN1.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN2},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN2.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN3},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN3.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN4},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN4.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN5},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN5.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN6},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN6.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN7},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN7.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN8},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN8.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AIN9},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN9.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.AINCOM},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.AINCOM.value << 4],
    ),
    (
        {"adc_1_analog_in": ADCChannel.FLOAT},
        "state.adc_1.mux_p",
        ADCProperties.ADC1_MUXP.value.values[ADCChannel.FLOAT.value << 4],
    ),
    # ADC1 MUX_N
    (
        {"adc_1_mux_n": ADCChannel.AIN0},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN0.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN1},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN1.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN2},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN2.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN3},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN3.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN4},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN4.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN5},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN5.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN6},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN6.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN7},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN7.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN8},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN8.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AIN9},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN9.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.AINCOM},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.AINCOM.value],
    ),
    (
        {"adc_1_mux_n": ADCChannel.FLOAT},
        "state.adc_1.mux_n",
        ADCProperties.ADC1_MUXN.value.values[ADCChannel.FLOAT.value],
    ),
    # ADC2 MUX_P
    (
        {"adc_2_analog_in": ADCChannel.AIN0},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN0.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN1},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN1.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN2},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN2.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN3},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN3.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN4},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN4.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN5},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN5.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN6},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN6.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN7},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN7.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN8},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN8.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AIN9},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN9.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.AINCOM},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.AINCOM.value << 4],
    ),
    (
        {"adc_2_analog_in": ADCChannel.FLOAT},
        "state.adc_2.mux_p",
        ADCProperties.ADC2_MUXP.value.values[ADCChannel.FLOAT.value << 4],
    ),
    # ADC2 MUX_N
    (
        {"adc_2_mux_n": ADCChannel.AIN0},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN0.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN1},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN1.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN2},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN2.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN3},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN3.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN4},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN4.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN5},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN5.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN6},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN6.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN7},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN7.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN8},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN8.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AIN9},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN9.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.AINCOM},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.AINCOM.value],
    ),
    (
        {"adc_2_mux_n": ADCChannel.FLOAT},
        "state.adc_2.mux_n",
        ADCProperties.ADC2_MUXN.value.values[ADCChannel.FLOAT.value],
    ),
])
def test_edgepi_state_no_cache(updates, state_property, expected, adc):
    adc._EdgePiADC__config(**updates)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = adc.get_state()
    assert eval(state_property) == expected
