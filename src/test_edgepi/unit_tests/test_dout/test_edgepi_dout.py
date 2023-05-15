"""unit tests for edgepi_dout module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.digital_output.digital_output_constants import AoutPins, DoutPins
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput, InvalidPinName

@pytest.mark.parametrize("pin_name, state, error, aout_clear",
                        [(DoutPins.DOUT1, True, does_not_raise(), AoutPins.AO_EN1),
                         (DoutPins.DOUT2, True, does_not_raise(), AoutPins.AO_EN2),
                         (DoutPins.DOUT3, True, does_not_raise(), AoutPins.AO_EN3),
                         (DoutPins.DOUT4, True, does_not_raise(), AoutPins.AO_EN4),
                         (DoutPins.DOUT5, True, does_not_raise(), AoutPins.AO_EN5),
                         (DoutPins.DOUT6, True, does_not_raise(), AoutPins.AO_EN6),
                         (DoutPins.DOUT7, True, does_not_raise(), AoutPins.AO_EN7),
                         (DoutPins.DOUT8, True, does_not_raise(), AoutPins.AO_EN8),
                         (DoutPins.DOUT1, False, does_not_raise(), AoutPins.AO_EN1),
                         (DoutPins.DOUT2, False, does_not_raise(), AoutPins.AO_EN2),
                         (DoutPins.DOUT3, False, does_not_raise(), AoutPins.AO_EN3),
                         (DoutPins.DOUT4, False, does_not_raise(), AoutPins.AO_EN4),
                         (DoutPins.DOUT5, False, does_not_raise(), AoutPins.AO_EN5),
                         (DoutPins.DOUT6, False, does_not_raise(), AoutPins.AO_EN6),
                         (DoutPins.DOUT7, False, does_not_raise(), AoutPins.AO_EN7),
                         (DoutPins.DOUT8, False, does_not_raise(), AoutPins.AO_EN8),
                         (DoutPins.DOUT8, None, pytest.raises(ValueError), None),
                         (None, False, pytest.raises(InvalidPinName), None),
                         (AoutPins.AO_EN8, False, pytest.raises(InvalidPinName), None)])
def test_edgepi_digital_output_state(mocker, pin_name, state, error, aout_clear):
    expander_set = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin")
    expander_clear = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.clear_expander_pin")
    dout = EdgePiDigitalOutput()
    with error:
        dout.digital_output_state(pin_name, state)
        if state:
            expander_set.assert_called_once_with(pin_name.value)
        else:
            expander_set.assert_called_once_with(aout_clear.value)
            expander_clear.assert_has_calls([mocker.call(pin_name.value),
                                             mocker.call(aout_clear.value)])

@pytest.mark.parametrize("pin_name, direction, error",
                        [(DoutPins.DOUT1, True, does_not_raise()),
                         (DoutPins.DOUT2, True, does_not_raise()),
                         (DoutPins.DOUT3, True, does_not_raise()),
                         (DoutPins.DOUT4, True, does_not_raise()),
                         (DoutPins.DOUT5, True, does_not_raise()),
                         (DoutPins.DOUT6, True, does_not_raise()),
                         (DoutPins.DOUT7, True, does_not_raise()),
                         (DoutPins.DOUT8, True, does_not_raise()),
                         (DoutPins.DOUT1, False, does_not_raise()),
                         (DoutPins.DOUT2, False, does_not_raise()),
                         (DoutPins.DOUT3, False, does_not_raise()),
                         (DoutPins.DOUT4, False, does_not_raise()),
                         (DoutPins.DOUT5, False, does_not_raise()),
                         (DoutPins.DOUT6, False, does_not_raise()),
                         (DoutPins.DOUT7, False, does_not_raise()),
                         (DoutPins.DOUT8, False, does_not_raise()),
                         (DoutPins.DOUT8, None, pytest.raises(ValueError)),
                         (None, False, pytest.raises(InvalidPinName)),
                         (AoutPins.AO_EN8, False, pytest.raises(InvalidPinName))])
def test_edgepi_digital_output_direction(mocker, pin_name, direction, error):
    exp_dir_in = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin_direction_in")
    exp_dir_out = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin_direction_out")
    dout = EdgePiDigitalOutput()
    with error:
        dout.digital_output_direction(pin_name, direction)
        if direction:
            exp_dir_in.assert_called_once_with(pin_name.value)
        else:
            exp_dir_out.assert_called_once_with(pin_name.value)
