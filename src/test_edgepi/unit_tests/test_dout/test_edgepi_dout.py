"""unit tests for edgepi_dout module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput, InvalidPinName

@pytest.mark.parametrize("pin_name, state, error, aout_clear",
                        [(GpioPins.DOUT1, True, does_not_raise(), GpioPins.AO_EN1),
                         (GpioPins.DOUT2, True, does_not_raise(), GpioPins.AO_EN2),
                         (GpioPins.DOUT3, True, does_not_raise(), GpioPins.AO_EN3),
                         (GpioPins.DOUT4, True, does_not_raise(), GpioPins.AO_EN4),
                         (GpioPins.DOUT5, True, does_not_raise(), GpioPins.AO_EN5),
                         (GpioPins.DOUT6, True, does_not_raise(), GpioPins.AO_EN6),
                         (GpioPins.DOUT7, True, does_not_raise(), GpioPins.AO_EN7),
                         (GpioPins.DOUT8, True, does_not_raise(), GpioPins.AO_EN8),
                         (GpioPins.DOUT1, False, does_not_raise(), GpioPins.AO_EN1),
                         (GpioPins.DOUT2, False, does_not_raise(), GpioPins.AO_EN2),
                         (GpioPins.DOUT3, False, does_not_raise(), GpioPins.AO_EN3),
                         (GpioPins.DOUT4, False, does_not_raise(), GpioPins.AO_EN4),
                         (GpioPins.DOUT5, False, does_not_raise(), GpioPins.AO_EN5),
                         (GpioPins.DOUT6, False, does_not_raise(), GpioPins.AO_EN6),
                         (GpioPins.DOUT7, False, does_not_raise(), GpioPins.AO_EN7),
                         (GpioPins.DOUT8, False, does_not_raise(), GpioPins.AO_EN8),
                         (GpioPins.DOUT8, None, pytest.raises(ValueError),None),
                         (None, False, pytest.raises(InvalidPinName), None),
                         (GpioPins.DIN1, False, pytest.raises(InvalidPinName), None)])
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
                        [(GpioPins.DOUT1, True, does_not_raise()),
                         (GpioPins.DOUT2, True, does_not_raise()),
                         (GpioPins.DOUT3, True, does_not_raise()),
                         (GpioPins.DOUT4, True, does_not_raise()),
                         (GpioPins.DOUT5, True, does_not_raise()),
                         (GpioPins.DOUT6, True, does_not_raise()),
                         (GpioPins.DOUT7, True, does_not_raise()),
                         (GpioPins.DOUT8, True, does_not_raise()),
                         (GpioPins.DOUT1, False, does_not_raise()),
                         (GpioPins.DOUT2, False, does_not_raise()),
                         (GpioPins.DOUT3, False, does_not_raise()),
                         (GpioPins.DOUT4, False, does_not_raise()),
                         (GpioPins.DOUT5, False, does_not_raise()),
                         (GpioPins.DOUT6, False, does_not_raise()),
                         (GpioPins.DOUT7, False, does_not_raise()),
                         (GpioPins.DOUT8, False, does_not_raise()),
                         (GpioPins.DOUT8, None, pytest.raises(ValueError)),
                         (None, False, pytest.raises(InvalidPinName)),
                         (GpioPins.DIN1, False, pytest.raises(InvalidPinName))])
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



@pytest.mark.parametrize("pin_name, mock_vals",
                        [(GpioPins.DOUT1,[True, False]),
                         (GpioPins.DOUT2,[True, True]),
                         (GpioPins.DOUT3,[False, False]),
                         (GpioPins.DOUT4,[False, True]),
                         (GpioPins.DOUT5,[True, False]),
                         (GpioPins.DOUT6,[True, True]),
                         (GpioPins.DOUT7,[False, False]),
                         (GpioPins.DOUT8,[False, True]),
                         ])
def test_get_state(mocker, pin_name, mock_vals):
    mock_state = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.read_pin_state", return_value = mock_vals[0])
    mock_direction = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.get_pin_direction", return_value = mock_vals[1])
    dout= EdgePiDigitalOutput()
    stat, dir = dout.get_state(pin_name)
    assert stat == mock_state.return_value
    assert dir == mock_direction.return_value
