"""Integration testing for EdgePiADC get_state()"""

import logging
import pytest

from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_query_lang import ADCProperties
from edgepi.adc.adc_constants import (
    ADCNum,
    ADC1DataRate,
    ADC2DataRate,
    ADCChannel,
    CheckMode,
    ConvMode,
    FilterMode,
    RTDModes,
)

_logger = logging.getLogger(__name__)

# pylint: disable=protected-access, too-many-lines
@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    adc = EdgePiADC(enable_cache=False)
    # turn off to allow configuring RTD properties
    adc.set_rtd(set_rtd=False)
    yield adc

@pytest.mark.parametrize(
    "updates, state_property, expected",
    [
        # ADC1 MUX_P
        (
            {"adc_1_ch": ADCChannel.AIN0},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN1},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN2},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN3},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN4},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN5},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN6},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN7},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AINCOM},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.FLOAT},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC1 MUX_N: need to set mux_p as well, otherwise updates only to mux_n fail
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN0},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN1},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN2},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN3},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN4},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN5},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN6},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN7},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AINCOM},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.FLOAT},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # ADC2 MUX_P
        (
            {"adc_2_ch": ADCChannel.AIN0},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN1},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN2},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN3},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN4},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN5},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN6},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN7},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AINCOM},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.FLOAT},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC2 MUX_N
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN0},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN1},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN2},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN3},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN4},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN5},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN6},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN7},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AINCOM},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.FLOAT},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # CHECK MODE
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CRC},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CRC.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CHK},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CHK.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_OFF},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_OFF.value.op_code],
        ),
        # CONV MODE
        (
            {"conversion_mode": ConvMode.PULSE},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.PULSE.value.op_code],
        ),
        (
            {"conversion_mode": ConvMode.CONTINUOUS},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.CONTINUOUS.value.op_code],
        ),
        # ADC1 DATA RATE
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2P5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2P5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_10},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_16P6},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_16P6.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_20},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_20.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_50},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_50.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_60},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_60.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_100},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_1200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_1200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_4800},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_4800.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_7200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_7200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_14400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_14400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_19200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_19200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_38400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_38400.value.op_code],
        ),
        # ADC2 Data Rate
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_10},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_100},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_400},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_800},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_800.value.op_code],
        ),
        # FILTER MODE
        (
            {"filter_mode": FilterMode.SINC1},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC1.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC2},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC2.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC3},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC3.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC4},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC4.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.FIR},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.FIR.value.op_code],
        ),
    ],
)
def test_edgepi_state_no_cache(updates, state_property, expected, adc):
    adc._EdgePiADC__config(**updates)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = adc.get_state()
    assert eval(state_property) == expected

@pytest.mark.parametrize(
    "enable_rtd, adc_num, state_property, expected",
    [
        (
            True,
            ADCNum.ADC_1,
            "state.rtd_mode",
            RTDModes.RTD_ON
        ),
        (
            True,
            ADCNum.ADC_2,
            "state.rtd_mode",
            RTDModes.RTD_ON
        ),
        (
            False,
            ADCNum.ADC_2,
            "state.rtd_mode",
            RTDModes.RTD_OFF
        ),
        (
            True,
            ADCNum.ADC_1,
            "state.rtd_adc",
            ADCNum.ADC_1
        ),
        (
            True,
            ADCNum.ADC_2,
            "state.rtd_adc",
            ADCNum.ADC_2
        ),
        (
            False,
            ADCNum.ADC_2,
            "state.rtd_adc",
            None
        ),
    ],
)
def test_set_rtd_no_cache(enable_rtd, adc_num, state_property, expected, adc):
    adc.set_rtd(set_rtd=enable_rtd, adc_num=adc_num)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = adc.get_state()
    assert eval(state_property) == expected


# pylint: disable=protected-access
@pytest.fixture(name="adc_cache", scope="module")
def fixture_adc_cache():
    adc = EdgePiADC(enable_cache=True)
    yield adc


@pytest.mark.parametrize(
    "updates, state_property, expected",
    [
        # ADC1 MUX_P
        (
            {"adc_1_ch": ADCChannel.AIN0},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN1},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN2},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN3},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN4},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN5},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN6},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN7},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AINCOM},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.FLOAT},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC2 MUX_P
        (
            {"adc_2_ch": ADCChannel.AIN0},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN1},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN2},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN3},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN4},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN5},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN6},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN7},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AINCOM},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.FLOAT},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # CHECK MODE
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CRC},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CRC.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CHK},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CHK.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_OFF},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_OFF.value.op_code],
        ),
        # CONV MODE
        (
            {"checksum_mode": ConvMode.PULSE},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.PULSE.value.op_code],
        ),
        (
            {"checksum_mode": ConvMode.CONTINUOUS},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.CONTINUOUS.value.op_code],
        ),
        # ADC1 DATA RATE
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2P5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2P5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_10},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_16P6},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_16P6.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_20},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_20.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_50},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_50.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_60},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_60.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_100},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_1200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_1200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_4800},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_4800.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_7200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_7200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_14400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_14400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_19200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_19200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_38400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_38400.value.op_code],
        ),
        # ADC2 Data Rate
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_10},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_100},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_400},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_800},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_800.value.op_code],
        ),
        # FILTER MODE
        (
            {"filter_mode": FilterMode.SINC1},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC1.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC2},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC2.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC3},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC3.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC4},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC4.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.FIR},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.FIR.value.op_code],
        ),
    ],
)
def test_edgepi_state_with_cache(updates, state_property, expected, adc_cache):
    adc_cache._EdgePiADC__config(**updates)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = adc_cache.get_state()
    assert eval(state_property) == expected


@pytest.mark.parametrize(
    "enable_rtd, adc_num, state_property, expected",
    [
        (
            True,
            ADCNum.ADC_1,
            "state.rtd_mode",
            RTDModes.RTD_ON
        ),
        (
            True,
            ADCNum.ADC_2,
            "state.rtd_mode",
            RTDModes.RTD_ON
        ),
        (
            False,
            ADCNum.ADC_2,
            "state.rtd_mode",
            RTDModes.RTD_OFF
        ),
        (
            True,
            ADCNum.ADC_1,
            "state.rtd_adc",
            ADCNum.ADC_1
        ),
        (
            True,
            ADCNum.ADC_2,
            "state.rtd_adc",
            ADCNum.ADC_2
        ),
        (
            False,
            ADCNum.ADC_2,
            "state.rtd_adc",
            None
        ),
    ],
)
def test_set_rtd_with_cache(enable_rtd, adc_num, state_property, expected, adc_cache):
    adc_cache.set_rtd(set_rtd=enable_rtd, adc_num=adc_num)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = adc_cache.get_state()
    assert eval(state_property) == expected


@pytest.mark.parametrize(
    "updates, state_property, expected",
    [
        # ADC1 MUX_P
        (
            {"adc_1_ch": ADCChannel.AIN0},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN1},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN2},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN3},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN4},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN5},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN6},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN7},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AINCOM},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.FLOAT},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC1 MUX_N: need to set mux_p as well, otherwise updates only to mux_n fail
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN0},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN1},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN2},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN3},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN4},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN5},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN6},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN7},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AINCOM},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.FLOAT},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # ADC2 MUX_P
        (
            {"adc_2_ch": ADCChannel.AIN0},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN1},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN2},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN3},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN4},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN5},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN6},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN7},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AINCOM},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.FLOAT},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC2 MUX_N
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN0},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN1},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN2},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN3},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN4},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN5},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN6},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN7},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AINCOM},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.FLOAT},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # CHECK MODE
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CRC},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CRC.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CHK},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CHK.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_OFF},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_OFF.value.op_code],
        ),
        # CONV MODE
        (
            {"checksum_mode": ConvMode.PULSE},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.PULSE.value.op_code],
        ),
        (
            {"checksum_mode": ConvMode.CONTINUOUS},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.CONTINUOUS.value.op_code],
        ),
        # ADC1 DATA RATE
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2P5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2P5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_10},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_16P6},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_16P6.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_20},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_20.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_50},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_50.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_60},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_60.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_100},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_1200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_1200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_4800},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_4800.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_7200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_7200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_14400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_14400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_19200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_19200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_38400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_38400.value.op_code],
        ),
        # ADC2 Data Rate
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_10},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_100},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_400},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_800},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_800.value.op_code],
        ),
        # FILTER MODE
        (
            {"filter_mode": FilterMode.SINC1},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC1.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC2},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC2.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC3},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC3.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC4},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC4.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.FIR},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.FIR.value.op_code],
        ),
    ]
)
def test_combined_cacheless_writes_caching_reads(
    updates, state_property, expected, adc, adc_cache
    ):
    adc._EdgePiADC__config(**updates)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = adc_cache.get_state()
    assert eval(state_property) == expected


@pytest.mark.parametrize(
    "updates, state_property, expected",
    [
        # ADC1 MUX_P
        (
            {"adc_1_ch": ADCChannel.AIN0},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN1},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN2},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN3},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN4},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN5},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN6},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN7},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.AINCOM},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_1_ch": ADCChannel.FLOAT},
            "state.adc_1.mux_p",
            ADCProperties.ADC1_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC1 MUX_N: need to set mux_p as well, otherwise updates only to mux_n fail
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN0},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN1},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN2},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN3},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN4},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN5},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN6},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AIN7},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.AINCOM},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {"adc_1_ch": ADCChannel.AIN0, "adc_1_mux_n": ADCChannel.FLOAT},
            "state.adc_1.mux_n",
            ADCProperties.ADC1_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # ADC2 MUX_P
        (
            {"adc_2_ch": ADCChannel.AIN0},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN0.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN1},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN1.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN2},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN2.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN3},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN3.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN4},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN4.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN5},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN5.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN6},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN6.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN7},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AIN7.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.AINCOM},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.AINCOM.value << 4],
        ),
        (
            {"adc_2_ch": ADCChannel.FLOAT},
            "state.adc_2.mux_p",
            ADCProperties.ADC2_MUXP.value.values[ADCChannel.FLOAT.value << 4],
        ),
        # ADC2 MUX_N
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN0},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN0.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN1},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN1.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN2},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN2.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN3},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN3.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN4},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN4.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN5},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN5.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN6},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN6.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AIN7},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AIN7.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.AINCOM},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.AINCOM.value],
        ),
        (
            {"adc_2_ch": ADCChannel.AIN0, "adc_2_mux_n": ADCChannel.FLOAT},
            "state.adc_2.mux_n",
            ADCProperties.ADC2_MUXN.value.values[ADCChannel.FLOAT.value],
        ),
        # CHECK MODE
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CRC},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CRC.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_CHK},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_CHK.value.op_code],
        ),
        (
            {"checksum_mode": CheckMode.CHECK_BYTE_OFF},
            "state.checksum_mode",
            ADCProperties.CHECK_MODE.value.values[CheckMode.CHECK_BYTE_OFF.value.op_code],
        ),
        # CONV MODE
        (
            {"checksum_mode": ConvMode.PULSE},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.PULSE.value.op_code],
        ),
        (
            {"checksum_mode": ConvMode.CONTINUOUS},
            "state.adc_1.conversion_mode",
            ADCProperties.CONV_MODE.value.values[ConvMode.CONTINUOUS.value.op_code],
        ),
        # ADC1 DATA RATE
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2P5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2P5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_5},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_5.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_10},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_16P6},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_16P6.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_20},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_20.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_50},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_50.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_60},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_60.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_100},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_1200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_1200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_2400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_2400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_4800},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_4800.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_7200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_7200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_14400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_14400.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_19200},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_19200.value.op_code],
        ),
        (
            {"adc_1_data_rate": ADC1DataRate.SPS_38400},
            "state.adc_1.data_rate",
            ADCProperties.DATA_RATE_1.value.values[ADC1DataRate.SPS_38400.value.op_code],
        ),
        # ADC2 Data Rate
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_10},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_10.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_100},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_100.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_400},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_400.value.op_code],
        ),
        (
            {"adc_2_data_rate": ADC2DataRate.SPS_800},
            "state.adc_2.data_rate",
            ADCProperties.DATA_RATE_2.value.values[ADC2DataRate.SPS_800.value.op_code],
        ),
        # FILTER MODE
        (
            {"filter_mode": FilterMode.SINC1},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC1.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC2},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC2.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC3},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC3.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.SINC4},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.SINC4.value.op_code],
        ),
        (
            {"filter_mode": FilterMode.FIR},
            "state.filter_mode",
            ADCProperties.FILTER_MODE.value.values[FilterMode.FIR.value.op_code],
        ),
    ]
)
def test_combined_caching_writes_cacheless_reads(
    updates, state_property, expected, adc, adc_cache
    ):
    adc_cache._EdgePiADC__config(**updates)
    # pylint: disable=eval-used, unused-variable
    # using eval to access nested attributes of state with dot notation
    state = adc.get_state()
    assert eval(state_property) == expected
