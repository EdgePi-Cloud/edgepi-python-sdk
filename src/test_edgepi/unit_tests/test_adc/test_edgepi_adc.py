"""" Unit tests for edgepi_adc module """


import sys
from unittest import mock

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADC_DEFAULT_VALS, ADC_NUM_REGS, ADCChannel as CH, ADCReg


@pytest.fixture(name="adc")
def fixture_adc(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    yield EdgePiADC()


def test_read_registers_to_map(mocker, adc):
    mocker.patch(
        "edgepi.peripherals.spi.SpiDevice.transfer", return_value=[0, 0] + ADC_DEFAULT_VALS
    )
    reg_dict = adc._EdgePiADC__read_registers_to_map()
    assert len(reg_dict) == ADC_NUM_REGS
    for i in range(ADC_NUM_REGS):
        assert reg_dict[i] == ADC_DEFAULT_VALS[i]


@pytest.mark.parametrize(
    "args, update_vals",
    [
        ({"adc_1_mux_p": CH.AIN0}, {ADCReg.REG_INPMUX.value: 0x01}),
        ({"adc_1_mux_p": CH.AIN2}, {ADCReg.REG_INPMUX.value: 0x21}),
    ],
)
def test_config(mocker, args, update_vals, adc):
    mocker.patch(
        "edgepi.peripherals.spi.SpiDevice.transfer", return_value=[0, 0] + ADC_DEFAULT_VALS
    )
    reg_values = adc._EdgePiADC__config(**args)

    for addx, entry in reg_values.items():
        if entry["is_changed"]:
            assert entry["value"] == update_vals[addx]
        else:
            assert entry["value"] == ADC_DEFAULT_VALS[addx]
