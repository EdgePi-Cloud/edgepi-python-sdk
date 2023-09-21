"""unit tests for edgepi_dout module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_output.digital_output_constants import DoutPins, DoutTriState
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput, InvalidPinName

@pytest.mark.parametrize("pin_name, state, error, aout_clear",
                        [(DoutPins.DOUT1, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN1),
                         (DoutPins.DOUT2, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN2),
                         (DoutPins.DOUT3, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN3),
                         (DoutPins.DOUT4, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN4),
                         (DoutPins.DOUT5, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN5),
                         (DoutPins.DOUT6, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN6),
                         (DoutPins.DOUT7, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN7),
                         (DoutPins.DOUT8, DoutTriState.HIGH, does_not_raise(), GpioPins.AO_EN8),
                         (DoutPins.DOUT1, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN1),
                         (DoutPins.DOUT2, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN2),
                         (DoutPins.DOUT3, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN3),
                         (DoutPins.DOUT4, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN4),
                         (DoutPins.DOUT5, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN5),
                         (DoutPins.DOUT6, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN6),
                         (DoutPins.DOUT7, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN7),
                         (DoutPins.DOUT8, DoutTriState.LOW, does_not_raise(), GpioPins.AO_EN8),
                         (DoutPins.DOUT1, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN1),
                         (DoutPins.DOUT2, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN2),
                         (DoutPins.DOUT3, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN3),
                         (DoutPins.DOUT4, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN4),
                         (DoutPins.DOUT5, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN5),
                         (DoutPins.DOUT6, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN6),
                         (DoutPins.DOUT7, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN7),
                         (DoutPins.DOUT8, DoutTriState.HI_Z, does_not_raise(), GpioPins.AO_EN8),
                         (DoutPins.DOUT8, None, pytest.raises(ValueError), None),
                         (None, False, pytest.raises(InvalidPinName), None),
                         (GpioPins.AO_EN8, False, pytest.raises(InvalidPinName), None)])
def test_set_dout_state(mocker, pin_name, state, error, aout_clear):
    expander_set = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin")
    expander_clear = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.clear_expander_pin")
    exp_dir_in = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin_direction_in")
    mock_eeprom = mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM")
    dout = EdgePiDigitalOutput()
    dout.dac=mock_eeprom
    with error:
        dout.set_dout_state(pin_name, state)
        if state == DoutTriState.HIGH:
            assert expander_set.call_count == 2
            assert expander_clear.call_count == 1
            expander_clear.assert_called_once_with(aout_clear.value)
        elif state == DoutTriState.LOW:
            expander_set.assert_called_once_with(aout_clear.value)
            expander_clear.assert_has_calls([mocker.call(pin_name.value),
                                             mocker.call(aout_clear.value)])
        else:
            expander_set.assert_called_once_with(aout_clear.value)
            expander_clear.assert_called_once_with(pin_name.value)
            exp_dir_in.assert_called_once_with(pin_name.value)
            dout.dac.write_voltage.assert_called_once()

@pytest.mark.parametrize("pin_name, mock_vals, result",
                        [(DoutPins.DOUT1,[True, False], DoutTriState.HIGH),
                         (DoutPins.DOUT3,[False, False], DoutTriState.LOW),
                         (DoutPins.DOUT2,[True, True], DoutTriState.HI_Z),
                         (DoutPins.DOUT4,[False, True], DoutTriState.HI_Z),
                         (DoutPins.DOUT5,[True, False], DoutTriState.HIGH),
                         (DoutPins.DOUT7,[False, False], DoutTriState.LOW),
                         (DoutPins.DOUT6,[True, True], DoutTriState.HI_Z),
                         (DoutPins.DOUT8,[False, True], DoutTriState.HI_Z),
                         ])
def test_get_state(mocker, pin_name, mock_vals, result):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.read_pin_state",
                               return_value = mock_vals[0])
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.get_pin_direction",
                                   return_value = mock_vals[1])
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM")
    dout= EdgePiDigitalOutput()
    gpio_state = dout.get_state(pin_name)
    assert gpio_state == result
