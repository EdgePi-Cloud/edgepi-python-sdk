"""unit tests for edgepi_dout module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.gpio_configs import DOUTPins
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput, InvalidPinName

@pytest.mark.parametrize("pin_name, state, error",
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
def test_edgepi_digital_output_state(mocker, pin_name, state, error):
    gpio_chip=mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.write_gpio_pin_state")
    expander_set = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin")
    expander_clear = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.clear_expander_pin")
    dout = EdgePiDigitalOutput()
    with error:
        dout.digital_output_state(pin_name, state)
        if pin_name.value in [DOUTPins.DOUT1.value,DOUTPins.DOUT2.value]:
            gpio_chip.assert_called_once_with(pin_name.value, state)
        else:
            if state:
                expander_set.assert_called_once_with(pin_name.value)
            else:
                expander_clear.assert_called_once_with(pin_name.value)

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
    gpio_chip=mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_gpio_pin_dir")
    exp_dir_in = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin_direction_in")
    exp_dir_out = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin_direction_out")
    dout = EdgePiDigitalOutput()
    with error:
        dout.digital_output_direction(pin_name, direction)
        if pin_name.value in [DOUTPins.DOUT1.value,DOUTPins.DOUT2.value]:
            gpio_chip.assert_called_once_with(pin_name.value, direction)
        else:
            if direction:
                exp_dir_in.assert_called_once_with(pin_name.value)
            else:
                exp_dir_out.assert_called_once_with(pin_name.value)
