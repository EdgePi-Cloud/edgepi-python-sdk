""" Integration tests for EdgePi ADC module """


from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.adc.adc_constants import ADC_NUM_REGS, ADCReg, ADCChannel as CH, ConvMode, CheckMode
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_multiplexers import ChannelMappingError

# pylint: disable=protected-access
@pytest.fixture(name="adc")
def fixture_adc():
    adc = EdgePiADC()
    adc._EdgePiADC__config(checksum_mode=CheckMode.CHECK_BYTE_CRC)
    yield adc


def test_read_register_individual(adc):
    # read each ADC register individually
    for reg_addx in ADCReg:
        out = adc._EdgePiADC__read_register(reg_addx, 1)
        # output data frame bytes = [null, null, reg_data]
        assert len(out) == 1


# __init__ configures INPMUX = 0xFA


@pytest.mark.parametrize(
    "args, expected_vals, err",
    [
        (
            {
                "adc_1_analog_in": CH.AIN2,
            },
            {
                ADCReg.REG_INPMUX.value: 0x2A,
            },
            does_not_raise(),
        ),
        (
            {
                "adc_1_mux_n": CH.AIN2,
            },
            {
                ADCReg.REG_INPMUX.value: 0xF2,
            },
            does_not_raise(),
        ),
        (
            {
                "adc_1_analog_in": CH.AIN1,
                "adc_2_analog_in": CH.AIN2,
                "adc_1_mux_n": CH.AIN3,
                "adc_2_mux_n": CH.AIN4,
            },
            {
                ADCReg.REG_INPMUX.value: 0x13,
                ADCReg.REG_ADC2MUX.value: 0x24,
            },
            does_not_raise(),
        ),
        (
            {
                "adc_1_analog_in": CH.AIN2,
                "adc_2_analog_in": CH.AIN2,
            },
            {
                ADCReg.REG_INPMUX.value: 0x2A,
                ADCReg.REG_ADC2MUX.value: 0x21,
            },
            does_not_raise(),
        ),
        (
            {
                "adc_1_analog_in": CH.AINCOM,
            },
            {
                ADCReg.REG_INPMUX.value: 0xAA,
            },
            pytest.raises(ChannelMappingError),
        ),
        (
            {
                "adc_1_analog_in": CH.AIN1,
                "adc_1_mux_n": CH.AIN1,
            },
            {
                ADCReg.REG_INPMUX.value: 0x11,
            },
            pytest.raises(ChannelMappingError),
        ),
    ],
)
def test_config(args, expected_vals, err, adc):
    regs = adc._EdgePiADC__read_register(ADCReg.REG_ID, ADC_NUM_REGS)

    with err:
        updated_regs = adc._EdgePiADC__config(**args)

        for addx, entry in updated_regs.items():
            if entry["is_changed"]:
                assert entry["value"] == expected_vals[addx]
            else:
                assert entry["value"] == regs[addx]

        # reset adc registers to pre-test values
        # TODO: replace with reset command once implemented
        adc._EdgePiADC__write_register(ADCReg.REG_ID, regs)


# def test_read_voltage_pulse(adc):
#     read_len = adc._EdgePiADC__get_data_read_len()
#     adc._EdgePiADC__config(conversion_mode=ConvMode.PULSE)
#     for ch in CH:
#         if ch != CH.FLOAT:
#             args = {
#                 "adc_1_analog_in": ch,
#                 "adc_1_mux_n": CH.FLOAT,
#             }
#             adc._EdgePiADC__config(**args)
#             data = adc.read_voltage()
#             print(data)
#             assert len(data[1:]) == read_len
#             assert data[1:] != [0] * read_len


# def test_read_voltage_continuous(adc):
#     read_len = adc._EdgePiADC__get_data_read_len()
#     adc._EdgePiADC__config(conversion_mode=ConvMode.CONTINUOUS)
#     adc.start_auto_conversions()
#     for ch in CH:
#         if ch != CH.FLOAT:
#             args = {
#                 "adc_1_analog_in": ch,
#                 "adc_1_mux_n": CH.FLOAT,
#             }
#             adc._EdgePiADC__config(**args)
#             data = adc.read_voltage()
#             print(data)
#             assert len(data[1:]) == read_len
#             assert data[1:] != [0] * read_len
#     adc.stop_auto_conversions()


def test_voltage_individual(adc):
    adc._EdgePiADC__config(conversion_mode=ConvMode.PULSE, adc_1_analog_in=CH.AIN3)
    out = adc.single_sample()
    print(out)


def test_voltage_continuous(adc):
    try:
        adc._EdgePiADC__config(conversion_mode=ConvMode.CONTINUOUS, adc_1_analog_in=CH.AIN3)
        adc.start_conversions()
        for _ in range(10):
            out = adc.read_voltage()
            print(out)
    finally:
        adc.stop_conversions()
