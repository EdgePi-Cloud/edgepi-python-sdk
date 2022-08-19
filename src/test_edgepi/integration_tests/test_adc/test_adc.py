""" Integration tests for EdgePi ADC module """


import pytest
from edgepi.adc.adc_constants import ADC_NUM_REGS, ADCReg, ADCChannel as CH
from edgepi.adc.edgepi_adc import EdgePiADC


@pytest.fixture(name="adc")
def fixture_adc():
    return EdgePiADC()


# pylint: disable=protected-access
def test_read_register_individual(adc):
    # read each ADC register individually
    for reg_addx in ADCReg:
        out = adc._EdgePiADC__read_register(reg_addx, 1)
        # output data frame bytes = [null, null, reg_data]
        assert len(out) == 1


@pytest.mark.parametrize(
    "args, expected_vals",
    [
        (
            # TODO: can't test individually, since by default mux are set
            # to same pins, which raises ChannelMappingError. Each mux needs
            # to be set to different pin at __init__.
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
        ),
    ],
)
def test_config(args, expected_vals, adc):
    regs = adc._EdgePiADC__read_register(ADCReg.REG_ID, ADC_NUM_REGS)

    updated_regs = adc._EdgePiADC__config(**args)

    for addx, entry in updated_regs.items():
        if entry["is_changed"]:
            assert entry["value"] == expected_vals[addx]
        else:
            assert entry["value"] == regs[addx]

    # reset adc registers to pre-test values
    # TODO: replace with reset command once implemented
    adc._EdgePiADC__write_register(ADCReg.REG_ID, regs)
