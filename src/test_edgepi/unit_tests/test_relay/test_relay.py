"""unit tests for edgepi_relay module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.relay.edgepi_relay import EdgePiRelay

@pytest.mark.parametrize("normally_open, pin_name", [(True, GpioPins.RELAY.value),
                                                    (False, GpioPins.RELAY.value)])
def test_edgepi_relay_init(mocker, normally_open, pin_name):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    pin_set = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.set_pin_state')
    pin_clear = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.clear_pin_state')
    EdgePiRelay(normally_open)
    if normally_open:
        pin_clear.assert_called_once_with(pin_name)
    else:
        pin_set.assert_called_once_with(pin_name)

@pytest.mark.parametrize("normally_open, result", [(True, True),
                                                    (False, False)])
def test_get_state_relay(mocker, normally_open, result):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.read_pin_state',
                  return_value = normally_open)
    relay = EdgePiRelay(normally_open)
    assert relay.get_state_relay() == result

@pytest.mark.parametrize("normally_open, pin_name", [(True, GpioPins.RELAY.value),
                                                     (False, GpioPins.RELAY.value)])
def test_toggle_relay(mocker, normally_open, pin_name):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    toggle_pin = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.toggle_pin')
    relay = EdgePiRelay(normally_open)
    relay.toggle_relay()
    toggle_pin.assert_called_once_with(pin_name)

@pytest.mark.parametrize("normally_open", [(True),
                                           (False)])
def test_close_relay(mocker, normally_open):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    set_pin = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.set_pin_state')
    relay = EdgePiRelay(normally_open)
    relay.close_relay()
    if normally_open:
        assert set_pin.call_count == 1
    else:
        assert set_pin.call_count == 2

@pytest.mark.parametrize("normally_open", [(True),
                                           (False)])
def test_open_relay(mocker, normally_open):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    clear_pin = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.clear_pin_state')
    relay = EdgePiRelay(normally_open)
    relay.open_relay()
    if normally_open:
        assert clear_pin.call_count == 2
    else:
        assert clear_pin.call_count == 1
