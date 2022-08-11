"""" Unit tests for edgepi_adc module """


import sys
from unittest import mock

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel as CH, ADCReg
from edgepi.reg_helper.reg_helper import BitMask, OpCode


@pytest.fixture(name="adc")
def fixture_adc(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    yield EdgePiADC()


@pytest.mark.parametrize(
    "adc_1_ch, adc_2_ch, expected",
    [
        (None, None, []),
        (
            CH.AIN0,
            None,
            [
                OpCode(
                    op_code=0,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
        (
            None,
            CH.AIN1,
            [
                OpCode(
                    op_code=0x10,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
        (
            CH.AIN0,
            CH.AIN1,
            [
                OpCode(
                    op_code=0x00,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                ),
                OpCode(
                    op_code=0x10,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
    ],
)
def test_get_channel_assign_opcodes(adc_1_ch, adc_2_ch, expected, adc):
    out = adc._EdgePiADC__get_channel_assign_opcodes(adc_1_ch, adc_2_ch)
    assert list(out) == expected

# TODO: pytest does not see ChannelMappingError as equal to where it's defined
# def test_get_channel_assign_opcodes_raises(adc):
#     with pytest.raises(ChannelMappingError):
#         adc._EdgePiADC__get_channel_assign_opcodes(CH.AIN1, CH.AIN1)
