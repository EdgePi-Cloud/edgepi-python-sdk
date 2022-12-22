""" Unit tests for edgepi_dac module """

from copy import deepcopy
from unittest import mock
from unittest.mock import call
import sys

sys.modules['periphery'] = mock.MagicMock()

# pylint: disable=wrong-import-position
# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372
# pylint: disable=protected-access

import pytest
from bitstring import pack
from edgepi.dac.dac_constants import (
    AOPins,
    PowerMode,
    DACChannel as CH,
    EdgePiDacCom as COM,
)
from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.calibration.protobuf_mapping import EdgePiEEPROMData
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout
from test_edgepi.unit_tests.test_calibration.read_serialized import read_binfile

dummy_calib_param_dict = {0:CalibParam(gain=1,offset=0),
                          1:CalibParam(gain=1,offset=0),
                          2:CalibParam(gain=1,offset=0),
                          3:CalibParam(gain=1,offset=0),
                          4:CalibParam(gain=1,offset=0),
                          5:CalibParam(gain=1,offset=0),
                          6:CalibParam(gain=1,offset=0),
                          7:CalibParam(gain=1,offset=0)}

@pytest.fixture(name="dac")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO")
    eelayout= EepromLayout()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.get_edgepi_reserved_data",
                  return_value = EdgePiEEPROMData(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    yield dac

@pytest.fixture(name="dac_mock_periph")
def fixture_test_dac_write_voltage(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    eelayout= EepromLayout()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.get_edgepi_reserved_data",
                  return_value = EdgePiEEPROMData(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    yield dac


_default_power_modes = {
    CH.AOUT7.value: PowerMode.NORMAL.value,
    CH.AOUT6.value: PowerMode.NORMAL.value,
    CH.AOUT5.value: PowerMode.NORMAL.value,
    CH.AOUT4.value: PowerMode.NORMAL.value,
    CH.AOUT3.value: PowerMode.NORMAL.value,
    CH.AOUT2.value: PowerMode.NORMAL.value,
    CH.AOUT1.value: PowerMode.NORMAL.value,
    CH.AOUT0.value: PowerMode.NORMAL.value,
}


@pytest.mark.parametrize(
    "power_modes, analog_out, mode, expected",
    [
        (deepcopy(_default_power_modes), CH.AOUT7, PowerMode.POWER_DOWN_GROUND, [64, 64, 0]),
        (deepcopy(_default_power_modes), CH.AOUT7, PowerMode.POWER_DOWN_3_STATE, [64, 192, 0]),
        (deepcopy(_default_power_modes), CH.AOUT7, PowerMode.NORMAL, [64, 0, 0]),
        (
            {
                CH.AOUT7.value: PowerMode.POWER_DOWN_GROUND.value,
                CH.AOUT6.value: PowerMode.NORMAL.value,
                CH.AOUT5.value: PowerMode.NORMAL.value,
                CH.AOUT4.value: PowerMode.NORMAL.value,
                CH.AOUT3.value: PowerMode.NORMAL.value,
                CH.AOUT2.value: PowerMode.NORMAL.value,
                CH.AOUT1.value: PowerMode.NORMAL.value,
                CH.AOUT0.value: PowerMode.NORMAL.value,
            },
            CH.AOUT7,
            PowerMode.NORMAL,
            [64, 0, 0],
        ),
        (
            {
                CH.AOUT7.value: PowerMode.NORMAL.value,
                CH.AOUT6.value: PowerMode.NORMAL.value,
                CH.AOUT5.value: PowerMode.POWER_DOWN_GROUND.value,
                CH.AOUT4.value: PowerMode.NORMAL.value,
                CH.AOUT3.value: PowerMode.NORMAL.value,
                CH.AOUT2.value: PowerMode.NORMAL.value,
                CH.AOUT1.value: PowerMode.NORMAL.value,
                CH.AOUT0.value: PowerMode.NORMAL.value,
            },
            CH.AOUT5,
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
                         [(CH.AOUT0, [0xA1,0x69, 0xDF]),
                          (CH.AOUT1, [0xA1,0x69, 0xDF]),
                          (CH.AOUT2, [0xA1,0x69, 0xDF]),
                          (CH.AOUT3, [0xA1,0x69, 0xDF]),
                          (CH.AOUT4, [0xA1,0x69, 0xDF]),
                          (CH.AOUT5, [0xA1,0x69, 0xDF]),
                          (CH.AOUT6, [0xA1,0x69, 0xDF]),
                          (CH.AOUT7, [0xA1,0x69, 0xDF])])
def test_channel_readback(mocker, analog_out, mock_val, dac):
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", return_value=mock_val)
    bits = pack("uint:8, uint:8, uint:8", mock_val[0], mock_val[1], mock_val[2])
    result = bits[-16:].uint
    code = dac.channel_readback(analog_out)
    assert code == result

@pytest.mark.parametrize(
    "analog_out, read_data",
    [
        (CH.AOUT7, [0, 0, 0]),
        (CH.AOUT6, [0, 0, 0]),
        (CH.AOUT5, [0, 0, 0]),
        (CH.AOUT4, [0, 0, 0]),
        (CH.AOUT3, [0, 0, 0]),
        (CH.AOUT2, [0, 0, 0]),
        (CH.AOUT1, [0, 0, 0]),
        (CH.AOUT0, [0, 0, 0]),
    ]
)
def test_dac_compute_expected_voltage(mocker, analog_out, read_data, dac):

    mock_transfer = mocker.patch(
        "edgepi.peripherals.spi.SpiDevice.transfer", return_value=read_data
    )
    byte_1 = (COM.COM_READBACK.value << 4) + analog_out.value
    dac.compute_expected_voltage(analog_out)
    write_calls = [call([byte_1, 0, 0]), call([0, 0, 0])]
    mock_transfer.assert_has_calls(write_calls)


@pytest.mark.parametrize(
    "analog_out, pin_name, voltage, mock_name",
    [
        (0, AOPins.AO_EN1.value, 1.0, "mock_set"),
        (1, AOPins.AO_EN2.value, 1.0, "mock_set"),
        (2, AOPins.AO_EN3.value, 1.0, "mock_set"),
        (3, AOPins.AO_EN4.value, 1.0, "mock_set"),
        (4, AOPins.AO_EN5.value, 1.0, "mock_set"),
        (5, AOPins.AO_EN6.value, 1.0, "mock_set"),
        (6, AOPins.AO_EN7.value, 1.0, "mock_set"),
        (7, AOPins.AO_EN8.value, 1.0, "mock_set"),
        (0, AOPins.AO_EN1.value, 0, "mock_clear"),
        (1, AOPins.AO_EN2.value, 0, "mock_clear"),
        (2, AOPins.AO_EN3.value, 0, "mock_clear"),
        (3, AOPins.AO_EN4.value, 0, "mock_clear"),
        (4, AOPins.AO_EN5.value, 0, "mock_clear"),
        (5, AOPins.AO_EN6.value, 0, "mock_clear"),
        (6, AOPins.AO_EN7.value, 0, "mock_clear"),
        (7, AOPins.AO_EN8.value, 0, "mock_clear"),
    ]
)
def test_dac_send_to_gpio_pins(mocker, analog_out, pin_name, voltage, mock_name):
    # can't mock entire GPIO class here because need to access its methods
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mock_set = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    mock_clear = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.clear_expander_pin")
    eelayout= EepromLayout()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.get_edgepi_reserved_data",
                  return_value = EdgePiEEPROMData(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
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
    (0, -0.1),
    (1, -0.1),
    (2, -0.1),
    (3, -0.1),
    (4, -0.1),
    (5, -0.1),
    (6, -0.1),
    (7, -0.1),
])
def test_send_to_gpio_pins_raises(analog_out, voltage, dac):
    with pytest.raises(ValueError) as err:
        dac._EdgePiDAC__send_to_gpio_pins(analog_out, voltage)
        assert err.value == "voltage cannot be negative"


@pytest.mark.parametrize("analog_out, voltage, mock_value, result",
                         [(CH.AOUT0, 2.123, [None, None, True], [13913]),
                          (CH.AOUT1, 2.123, [None, None, True], [13913]),
                          (CH.AOUT2, 2.123, [None, None, True], [13913]),
                          (CH.AOUT3, 2.123, [None, None, True], [13913]),
                          (CH.AOUT4, 2.123, [None, None, False], [27826]),
                          (CH.AOUT5, 2.123, [None, None, False], [27826]),
                          (CH.AOUT6, 2.123, [None, None, False], [27826]),
                          (CH.AOUT7, 2.123, [None, None, False], [27826])
                        ])
def test_write_voltage(mocker,analog_out, voltage, mock_value, result, dac_mock_periph):
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC.get_state",
                  return_value = (mock_value[0], mock_value[1], mock_value[2]))
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.get_pin_direction", return_value = False)
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    assert result[0] == dac_mock_periph.write_voltage(analog_out, voltage)

@pytest.mark.parametrize("enable, result, mocker_values,",
                        [(True, True, [None, None, True]),
                         (False, False, [None, None, False])])
def test_enable_dac_gain(mocker, enable, result, mocker_values):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC.get_state",
                  return_value = (mocker_values[0], mocker_values[1], mocker_values[2]))
    set_dac_gain = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    clear_dac_gain = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.clear_expander_pin")
    eelayout= EepromLayout()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.get_edgepi_reserved_data",
                  return_value = EdgePiEEPROMData(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    # pylint: disable=expression-not-assigned
    assert dac.enable_dac_gain(enable) == result
    set_dac_gain.assert_called_once_with("DAC_GAIN") if enable \
        else clear_dac_gain.assert_called_once_with("DAC_GAIN")

@pytest.mark.parametrize("mock_val, analog_out, code, voltage, gain, result",
    [([0xA1,0x69, 0xDF, True], CH.AOUT0, True, True, True, [27103, 2.116, True]),
    ([0xA1,0x69, 0xDF, False], CH.AOUT1, True, True, True, [27103, 2.116, False]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT2, True, True, False, [27103, 2.116, None]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT3, True, True, None, [27103, 2.116, None]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT4, True, False, True, [27103, None, True]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT5, True, None, True, [27103, None, True]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT6, False, True, True, [None, 2.116, True]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT7, None, True, True, [None, 2.116, True])])
def test_get_state(mocker, analog_out, code, voltage, gain, result, mock_val):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.get_pin_direction", return_value = mock_val[3])
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", return_value=mock_val[0:3])
    eelayout= EepromLayout()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.get_edgepi_reserved_data",
                  return_value = EdgePiEEPROMData(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    code_val, voltage_val, gain_state = dac.get_state(analog_out, code, voltage, gain)
    assert code_val == result[0]
    assert pytest.approx(voltage_val, 1e-3) == voltage_val
    assert gain_state == result[2]
