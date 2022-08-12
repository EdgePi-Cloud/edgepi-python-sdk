"""" Unit tests for edgepi_adc module """


import sys
from unittest import mock

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADC_DEFAULT_VALS, ADC_NUM_REGS


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
