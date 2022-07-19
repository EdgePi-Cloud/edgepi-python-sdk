""" Unit tests for edgepi_dac module """

from copy import deepcopy

import pytest
from edgepi.dac.dac_constants import (
    GainMode,
    PowerMode,
    EdgePiDacChannel as CH,
    EdgePiDacCom as COM,
)
from edgepi.dac.edgepi_dac import EdgePiDAC


@pytest.fixture(name="dac")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
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
    ],
)
# TODO: add more test cases
def test_set_power_mode(mocker, power_modes, analog_out, mode, expected, dac):
    mocker.patch.object(dac, "_dac_state", power_modes)
    mock_transfer = mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer")
    dac.set_power_mode(analog_out, mode)
    mock_transfer.assert_called_once_with(expected)


@pytest.mark.parametrize(
    "gain_mode, expected",
    [
        (GainMode.SINGLE, [112, 0, 0]),
        (GainMode.DOUBLE, [112, 0, 4]),
    ],
)
def test_set_gain_mode(mocker, gain_mode, expected, dac):
    mock_transfer = mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer")
    dac.set_gain_mode(gain_mode)
    mock_transfer.assert_called_once_with(expected)


def test_reset(mocker, dac):
    mock_transfer = mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer")
    dac.reset()
    mock_transfer.assert_called_once_with([96, 18, 52])


@pytest.mark.parametrize("analog_out",
    [(8), (7), (6), (5), (4), (3), (2), (1)]
)
def test_read_voltage(mocker, analog_out, dac):
    mock_transfer = mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer")
    dac_ch = analog_out - 1
    byte_1 = (COM.COM_READBACK.value << 4) + dac_ch
    dac.read_voltage(analog_out)
    mock_transfer.assert_called_once_with([byte_1, 0, 0])
