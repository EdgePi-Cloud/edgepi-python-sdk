""" Unit tests for edgepi_dac module """

from copy import deepcopy
from unittest import mock
from unittest.mock import call
import sys

sys.modules['periphery'] = mock.MagicMock()

# pylint: disable=wrong-import-position
# pylint: disable=protected-access

import pytest
from bitstring import pack
from edgepi.dac.dac_constants import (
    AOPins,
    PowerMode,
    EdgePiDacChannel as CH,
    EdgePiDacCom as COM,
)
from edgepi.dac.edgepi_dac import EdgePiDAC

@pytest.fixture(name="dac")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO")
    yield EdgePiDAC()

@pytest.fixture(name="dac_mock_periph")
def fixture_test_dac_write_voltage(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    yield EdgePiDAC()


_default_power_modes = {
    CH.DAC7.value: PowerMode.NORMAL.value,
    CH.DAC6.value: PowerMode.NORMAL.value,
    CH.DAC5.value: PowerMode.NORMAL.value,
    CH.DAC4.value: PowerMode.NORMAL.value,
    CH.DAC3.value: PowerMode.NORMAL.value,
    CH.DAC2.value: PowerMode.NORMAL.value,
    CH.DAC1.value: PowerMode.NORMAL.value,
    CH.DAC0.value: PowerMode.NORMAL.value,
}


@pytest.mark.parametrize(
    "power_modes, analog_out, mode, expected",
    [
        (deepcopy(_default_power_modes), 8, PowerMode.POWER_DOWN_GROUND, [64, 64, 0]),
        (deepcopy(_default_power_modes), 8, PowerMode.POWER_DOWN_3_STATE, [64, 192, 0]),
        (deepcopy(_default_power_modes), 8, PowerMode.NORMAL, [64, 0, 0]),
        (
            {
                CH.DAC7.value: PowerMode.POWER_DOWN_GROUND.value,
                CH.DAC6.value: PowerMode.NORMAL.value,
                CH.DAC5.value: PowerMode.NORMAL.value,
                CH.DAC4.value: PowerMode.NORMAL.value,
                CH.DAC3.value: PowerMode.NORMAL.value,
                CH.DAC2.value: PowerMode.NORMAL.value,
                CH.DAC1.value: PowerMode.NORMAL.value,
                CH.DAC0.value: PowerMode.NORMAL.value,
            },
            8,
            PowerMode.NORMAL,
            [64, 0, 0],
        ),
        (
            {
                CH.DAC7.value: PowerMode.NORMAL.value,
                CH.DAC6.value: PowerMode.NORMAL.value,
                CH.DAC5.value: PowerMode.POWER_DOWN_GROUND.value,
                CH.DAC4.value: PowerMode.NORMAL.value,
                CH.DAC3.value: PowerMode.NORMAL.value,
                CH.DAC2.value: PowerMode.NORMAL.value,
                CH.DAC1.value: PowerMode.NORMAL.value,
                CH.DAC0.value: PowerMode.NORMAL.value,
            },
            6,
            PowerMode.NORMAL,
            [0x40, 0, 0],
        ),
    ],
)
def test_dac_set_power_mode(mocker, power_modes, analog_out, mode, expected, dac):
    mocker.patch.object(dac, "_EdgePiDAC__dac_power_state", power_modes)
    mock_transfer = mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer")
    dac.set_power_mode(analog_out, mode)
    mock_transfer.assert_called_once_with(expected)


def test_dac_reset(mocker, dac):
    mock_transfer = mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer")
    dac.reset()
    mock_transfer.assert_called_once_with([96, 18, 52])

@pytest.mark.parametrize("analog_out, mock_val",
                         [(1, [0xA1,0x69, 0xDF]),
                          (2, [0xA1,0x69, 0xDF]),
                          (3, [0xA1,0x69, 0xDF]),
                          (4, [0xA1,0x69, 0xDF]),
                          (5, [0xA1,0x69, 0xDF]),
                          (6, [0xA1,0x69, 0xDF]),
                          (7, [0xA1,0x69, 0xDF]),
                          (8, [0xA1,0x69, 0xDF])])
def test_channel_readback(mocker, analog_out, mock_val, dac):
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", return_value=mock_val)
    bits = pack("uint:8, uint:8, uint:8", mock_val[0], mock_val[1], mock_val[2])
    result = bits[-16:].uint
    code = dac.channel_readback(analog_out)
    assert code == result

@pytest.mark.parametrize(
    "analog_out, read_data",
    [
        (8, [0, 0, 0]),
        (7, [0, 0, 0]),
        (6, [0, 0, 0]),
        (5, [0, 0, 0]),
        (4, [0, 0, 0]),
        (3, [0, 0, 0]),
        (2, [0, 0, 0]),
        (1, [0, 0, 0]),
    ]
)
def test_dac_compute_expected_voltage(mocker, analog_out, read_data, dac):

    mock_transfer = mocker.patch(
        "edgepi.peripherals.spi.SpiDevice.transfer", return_value=read_data
    )
    dac_ch = analog_out - 1
    byte_1 = (COM.COM_READBACK.value << 4) + dac_ch
    dac.compute_expected_voltage(analog_out)
    write_calls = [call([byte_1, 0, 0]), call([0, 0, 0])]
    mock_transfer.assert_has_calls(write_calls)


@pytest.mark.parametrize(
    "analog_out, pin_name, voltage, mock_name",
    [
        (1, AOPins.AO_EN1.value, 1.0, "mock_set"),
        (2, AOPins.AO_EN2.value, 1.0, "mock_set"),
        (3, AOPins.AO_EN3.value, 1.0, "mock_set"),
        (4, AOPins.AO_EN4.value, 1.0, "mock_set"),
        (5, AOPins.AO_EN5.value, 1.0, "mock_set"),
        (6, AOPins.AO_EN6.value, 1.0, "mock_set"),
        (7, AOPins.AO_EN7.value, 1.0, "mock_set"),
        (8, AOPins.AO_EN8.value, 1.0, "mock_set"),
        (1, AOPins.AO_EN1.value, 0, "mock_clear"),
        (2, AOPins.AO_EN2.value, 0, "mock_clear"),
        (3, AOPins.AO_EN3.value, 0, "mock_clear"),
        (4, AOPins.AO_EN4.value, 0, "mock_clear"),
        (5, AOPins.AO_EN5.value, 0, "mock_clear"),
        (6, AOPins.AO_EN6.value, 0, "mock_clear"),
        (7, AOPins.AO_EN7.value, 0, "mock_clear"),
        (8, AOPins.AO_EN8.value, 0, "mock_clear"),
    ]
)
def test_dac_send_to_gpio_pins(mocker, analog_out, pin_name, voltage, mock_name):
    # can't mock entire GPIO class here because need to access its methods
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio.I2CDevice")
    mock_set = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    mock_clear = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.clear_expander_pin")
    dac = EdgePiDAC()
    dac._EdgePiDAC__send_to_gpio_pins(analog_out, voltage)
    # check correct clause is entered depending on voltage written
    if voltage > 0:
        mock_set.assert_called_with(pin_name)
        mock_set.name = "mock_set"
        assert mock_set.name == mock_name
    else:
        mock_clear.assert_called_with(pin_name)
        mock_clear.name = "mock_clear"
        assert mock_clear.name == mock_name


@pytest.mark.parametrize('analog_out, voltage', [
    (1, -0.1),
    (2, -0.1),
    (3, -0.1),
    (4, -0.1),
    (5, -0.1),
    (6, -0.1),
    (7, -0.1),
    (8, -0.1),
])
def test_send_to_gpio_pins_raises(analog_out, voltage, dac):
    with pytest.raises(ValueError) as err:
        dac._EdgePiDAC__send_to_gpio_pins(analog_out, voltage)
        assert err.value == "voltage cannot be negative"


@pytest.mark.parametrize("anaolog_out, voltage, result",
                         [(1, 2.123, [27187]),
                          (2, 2.123, [27187]),
                          (3, 2.123, [27187]),
                          (4, 2.123, [27187]),
                          (5, 2.123, [27187]),
                          (6, 2.123, [27187]),
                          (7, 2.123, [27187]),
                          (8, 2.123, [27187])
                        ])
def test_write_voltage(anaolog_out, voltage, result, dac_mock_periph):
    assert result[0] == dac_mock_periph.write_voltage(anaolog_out, voltage)

@pytest.mark.parametrize("mock_val, analog_out, code, voltage, gain, result",
                         [([0xA1,0x69, 0xDF, True], 1, True, True, True, [27103, 2.116, True]),
                          ([0xA1,0x69, 0xDF, False], 2, True, True, True, [27103, 2.116, False]),
                          ([0xA1,0x69, 0xDF, True], 3, True, True, False, [27103, 2.116, None]),
                          ([0xA1,0x69, 0xDF, True], 4, True, True, None, [27103, 2.116, None]),
                          ([0xA1,0x69, 0xDF, True], 5, True, False, True, [27103, None, True]),
                          ([0xA1,0x69, 0xDF, True], 6, True, None, True, [27103, None, True]),
                          ([0xA1,0x69, 0xDF, True], 7, False, True, True, [None, 2.116, True]),
                          ([0xA1,0x69, 0xDF, True], 8, None, True, True, [None, 2.116, True])])
def test_get_state(mocker, analog_out, code, voltage, gain, result, mock_val):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio.I2CDevice")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.get_pin_direction", return_value = mock_val[3])
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", return_value=mock_val[0:3])
    dac = EdgePiDAC()
    code_val, voltage_val, gain_state = dac.get_state(analog_out, code, voltage, gain)
    assert code_val == result[0]
    assert pytest.approx(voltage_val, 1e-3) == voltage_val
    assert gain_state == result[2]
