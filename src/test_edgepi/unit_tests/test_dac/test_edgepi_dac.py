""" Unit tests for edgepi_dac module """

from copy import deepcopy
from unittest import mock
from unittest.mock import call
import sys

sys.modules['periphery'] = mock.MagicMock()

# pylint: disable=wrong-import-position
# pylint: disable=no-name-in-module
# pylint: disable=no-member
# https://github.com/protocolbuffers/protobuf/issues/10372
# pylint: disable=protected-access

from contextlib import nullcontext as does_not_raise
import pytest
from bitstring import pack
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.dac.dac_constants import (
    AOPins,
    PowerMode,
    DACChannel as CH,
    EdgePiDacCom as COM,
    EdgePiDacCalibrationConstants as CalibConst
)
from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.eeprom.edgepi_eeprom_data import EepromDataClass
from edgepi.eeprom.protobuf_assets.generated_pb2 import edgepi_module_pb2
from test_edgepi.unit_tests.test_eeprom.read_serialized import read_binfile

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
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    yield dac

@pytest.fixture(name="dac_mock_periph")
def fixture_test_dac_write_voltage(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    yield dac


_default_power_modes = {
    CH.AOUT8.value: PowerMode.NORMAL.value,
    CH.AOUT7.value: PowerMode.NORMAL.value,
    CH.AOUT6.value: PowerMode.NORMAL.value,
    CH.AOUT5.value: PowerMode.NORMAL.value,
    CH.AOUT4.value: PowerMode.NORMAL.value,
    CH.AOUT3.value: PowerMode.NORMAL.value,
    CH.AOUT2.value: PowerMode.NORMAL.value,
    CH.AOUT1.value: PowerMode.NORMAL.value,
}


@pytest.mark.parametrize(
    "power_modes, analog_out, mode, expected",
    [
        (deepcopy(_default_power_modes), CH.AOUT8, PowerMode.POWER_DOWN_GROUND, [64, 64, 0]),
        (deepcopy(_default_power_modes), CH.AOUT8, PowerMode.POWER_DOWN_3_STATE, [64, 192, 0]),
        (deepcopy(_default_power_modes), CH.AOUT8, PowerMode.NORMAL, [64, 0, 0]),
        (
            {
                CH.AOUT8.value: PowerMode.POWER_DOWN_GROUND.value,
                CH.AOUT7.value: PowerMode.NORMAL.value,
                CH.AOUT6.value: PowerMode.NORMAL.value,
                CH.AOUT5.value: PowerMode.NORMAL.value,
                CH.AOUT4.value: PowerMode.NORMAL.value,
                CH.AOUT3.value: PowerMode.NORMAL.value,
                CH.AOUT2.value: PowerMode.NORMAL.value,
                CH.AOUT1.value: PowerMode.NORMAL.value,
            },
            CH.AOUT8,
            PowerMode.NORMAL,
            [64, 0, 0],
        ),
        (
            {
                CH.AOUT8.value: PowerMode.NORMAL.value,
                CH.AOUT7.value: PowerMode.NORMAL.value,
                CH.AOUT6.value: PowerMode.POWER_DOWN_GROUND.value,
                CH.AOUT5.value: PowerMode.NORMAL.value,
                CH.AOUT4.value: PowerMode.NORMAL.value,
                CH.AOUT3.value: PowerMode.NORMAL.value,
                CH.AOUT2.value: PowerMode.NORMAL.value,
                CH.AOUT1.value: PowerMode.NORMAL.value,
            },
            CH.AOUT6,
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
                         [(CH.AOUT8, [0xA1,0x69, 0xDF]),
                          (CH.AOUT7, [0xA1,0x69, 0xDF]),
                          (CH.AOUT6, [0xA1,0x69, 0xDF]),
                          (CH.AOUT5, [0xA1,0x69, 0xDF]),
                          (CH.AOUT4, [0xA1,0x69, 0xDF]),
                          (CH.AOUT3, [0xA1,0x69, 0xDF]),
                          (CH.AOUT2, [0xA1,0x69, 0xDF]),
                          (CH.AOUT1, [0xA1,0x69, 0xDF])])
def test_channel_readback(mocker, analog_out, mock_val, dac):
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", return_value=mock_val)
    bits = pack("uint:8, uint:8, uint:8", mock_val[0], mock_val[1], mock_val[2])
    result = bits[-16:].uint
    code = dac.channel_readback(analog_out)
    assert code == result

@pytest.mark.parametrize(
    "analog_out, read_data",
    [
        (CH.AOUT8, [0, 0, 0]),
        (CH.AOUT7, [0, 0, 0]),
        (CH.AOUT6, [0, 0, 0]),
        (CH.AOUT5, [0, 0, 0]),
        (CH.AOUT4, [0, 0, 0]),
        (CH.AOUT3, [0, 0, 0]),
        (CH.AOUT2, [0, 0, 0]),
        (CH.AOUT1, [0, 0, 0]),
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
    "analog_out, voltage, result",
    [
        (0, 1.0, [2,1,GpioPins.DOUT1.value]),
        (1, 1.0, [2,1,GpioPins.DOUT2.value]),
        (2, 1.0, [1,1,GpioPins.DOUT3.value]),
        (3, 1.0, [1,1,GpioPins.DOUT4.value]),
        (4, 1.0, [1,1,GpioPins.DOUT5.value]),
        (5, 1.0, [1,1,GpioPins.DOUT6.value]),
        (6, 1.0, [1,1,GpioPins.DOUT7.value]),
        (7, 1.0, [1,1,GpioPins.DOUT8.value]),
        (0, 0, [2,2,AOPins.AO_EN1.value]),
        (1, 0, [2,2,AOPins.AO_EN2.value]),
        (2, 0, [1,2,AOPins.AO_EN3.value]),
        (3, 0, [1,2,AOPins.AO_EN4.value]),
        (4, 0, [1,2,AOPins.AO_EN5.value]),
        (5, 0, [1,2,AOPins.AO_EN6.value]),
        (6, 0, [1,2,AOPins.AO_EN7.value]),
        (7, 0, [1,2,AOPins.AO_EN8.value]),
    ]
)
def test_dac_send_to_gpio_pins(mocker, analog_out, voltage, result):
    # can't mock entire GPIO class here because need to access its methods
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mock_set = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    mock_clear = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.clear_expander_pin")
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    dac._EdgePiDAC__send_to_gpio_pins(analog_out, voltage)
    # check correct clause is entered depending on voltage written
    if voltage > 0:
        mock_clear.assert_called_with(result[2])
        assert mock_set.call_count == result[0]
        assert mock_clear.call_count == result[1]
    else:
        mock_clear.assert_called_with(result[2])
        assert mock_set.call_count == result[0]
        assert mock_clear.call_count == result[1]


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
                         [(CH.AOUT8, 2.123, True, [13913]),
                          (CH.AOUT7, 2.123, True, [13913]),
                          (CH.AOUT6, 2.123, True, [13913]),
                          (CH.AOUT5, 2.123, True, [13913]),
                          (CH.AOUT5, 9.999, True, [65528]),
                          (CH.AOUT5, 0, True, [0]),
                          (CH.AOUT5, 0, False, [0]),
                          (CH.AOUT5, 10.000, True, [65535]),
                          (CH.AOUT5, 5.000, False, [65535]),
                          (CH.AOUT4, 2.123, False, [27826]),
                          (CH.AOUT3, 2.123, False, [27826]),
                          (CH.AOUT2, 2.123, False, [27826]),
                          (CH.AOUT1, 2.123, False, [27826])
                        ])
def test_write_voltage(mocker,analog_out, voltage, mock_value, result, dac_mock_periph):
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC._EdgePiDAC__get_gain_state",
                  return_value = mock_value)
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.get_pin_direction", return_value = False)
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    assert result[0] == dac_mock_periph.write_voltage(analog_out, voltage)

@pytest.mark.parametrize("set_gain, code, result, error",
                    [(True, 2000, 1000, does_not_raise()),
                    (True, CalibConst.RANGE.value-1, 32767, does_not_raise()),
                    (False, CalibConst.RANGE.value-1, 0, pytest.raises(ValueError)),
                    (False,CalibConst.RANGE.value/2-1,CalibConst.RANGE.value-2,does_not_raise()),
                    ])
def test__compute_code_val(mocker, set_gain, code, result, error):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    with error:
        assert dac._EdgePiDAC__compute_code_val(set_gain, code) == result


@pytest.mark.parametrize("set_gain, result, mock_vals, error,",
                        [(True, [500]*8, [[1000,0,0]]*8, does_not_raise()),
                        (True, [500]*8, [[1001,0,0]]*8, does_not_raise()),
                        (False, [2000]*8, [[1000,0,0]]*8, does_not_raise()),
                        (False,
                         [CalibConst.RANGE.value-2]*8,
                         [[CalibConst.RANGE.value/2 -1,0,0]]*8,
                         does_not_raise()),
                        (False,
                         [CalibConst.RANGE.value]*8,
                         [[CalibConst.RANGE.value/2,0,0]]*8,
                         does_not_raise()),
                        (False, [40000]*8,[[40000,0,0]]*8,pytest.raises(ValueError)),
                        (False, [40000]*8,[[50000,0,0]]*8,pytest.raises(ValueError)),
                        ])
def test__get_ch_codes(mocker, set_gain, result, mock_vals, error):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC.get_state",
                  side_effect = mock_vals)
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    with error:
        assert result == dac._EdgePiDAC__get_ch_codes(set_gain)

@pytest.mark.parametrize("set_gain, result,",[(True, len(CH)), (False, len(CH))])
def test__auto_code_handler(mocker, set_gain, result):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC._EdgePiDAC__get_ch_codes",return_value=[0]*result)
    transfer_mock = mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC.transfer")
    set_dac_gain = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    clear_dac_gain = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.clear_expander_pin")
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    dac._EdgePiDAC__auto_code_handler(set_gain)
    assert transfer_mock.call_count == result
    # pylint: disable=expression-not-assigned
    set_dac_gain.assert_called_once_with("DAC_GAIN") if set_gain \
        else clear_dac_gain.assert_called_once_with("DAC_GAIN")

@pytest.mark.parametrize("set_gain, auto_code_change, mocker_values, result",
                        [
                        # case 1. current state is the same as set gain
                         (True, "Don't care", [True, "Don't care"], True),
                         (False, "Don't care", [False, "Don't care"], False),
                        # case 2. auto_code_change enabled
                         (True, True, [False, True], True),
                         (False, True, [True, False], False),
                        # case 3. auto_code_change disabled
                         (True, False, [False, True], True),
                         (False, False, [True, False], False),
                         ])
def test_set_gain_gain(mocker, set_gain, auto_code_change, mocker_values, result):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC._EdgePiDAC__get_gain_state",
                  side_effect=mocker_values)
    auto_code_handler=mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC._EdgePiDAC__auto_code_handler")
    set_dac_gain = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_expander_pin")
    clear_dac_gain = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.clear_expander_pin")
    # pylint: disable=expression-not-assigned
    assert dac.set_dac_gain(set_gain,auto_code_change) == result
    if auto_code_change and set_gain != mocker_values[0]:
        auto_code_handler.assert_called_once()
    if not auto_code_change and set_gain != mocker_values[0]:
        set_dac_gain.assert_called_once_with("DAC_GAIN") if set_gain \
            else clear_dac_gain.assert_called_once_with("DAC_GAIN")

@pytest.mark.parametrize("mock_val, result", [([True,True], False),
                                                ([True,False], True),
                                                ([False,True], False),
                                                ([False,False], False),
                                                ])
def test__get_gain_state(mocker, mock_val, result):
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM")
    # mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO")
    dac = EdgePiDAC()
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.read_pin_state", return_value = mock_val[0])
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.get_pin_direction", return_value = mock_val[1])
    dac_gain = dac._EdgePiDAC__get_gain_state()
    assert dac_gain == result

@pytest.mark.parametrize("mock_val, analog_out, code, voltage, gain, result",
    [([0xA1,0x69, 0xDF, True], CH.AOUT8, True, True, True, [27103, 2.116, True]),
    ([0xA1,0x69, 0xDF, False], CH.AOUT7, True, True, True, [27103, 2.116, False]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT6, True, True, False, [27103, 2.116, None]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT5, True, True, None, [27103, 2.116, None]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT4, True, False, True, [27103, None, True]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT3, True, None, True, [27103, None, True]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT2, False, True, True, [None, 2.116, True]),
    ([0xA1,0x69, 0xDF, True], CH.AOUT1, None, True, True, [None, 2.116, True])])
def test_get_state(mocker, analog_out, code, voltage, gain, result, mock_val):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.read_pin_state", return_value = mock_val[3])
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", return_value=mock_val[0:3])
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiDAC._EdgePiDAC__get_gain_state",
                  side_effect=[mock_val[3] if gain is True else result[2], mock_val[3]])
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    code_val, voltage_val, gain_state = dac.get_state(analog_out, code, voltage, gain)
    assert code_val == result[0]
    assert pytest.approx(voltage_val, 1e-3) == voltage_val
    assert gain_state == result[2]

@pytest.mark.parametrize("analog_out, result",
                        [(CH.AOUT1.value,  [1, 'PWM1']),
                         (CH.AOUT2.value,  [1, 'PWM2']),
                        ])
def test__dac_switching_logic(mocker, analog_out, result):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.gpio.edgepi_gpio_expander.I2CDevice")
    mock_set_pin_dir_out = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_pin_direction_out")
    mock_set_pin_state = mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO.set_pin_state")
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    dac = EdgePiDAC()
    dac.dac_ops.dict_calib_param = dummy_calib_param_dict
    dac._EdgePiDAC__dac_switching_logic(analog_out)

    assert mock_set_pin_dir_out.call_count == result[0]
    mock_set_pin_state.assert_called_once_with(result[1])
