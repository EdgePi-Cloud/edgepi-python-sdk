"""unit tests for edgepi_relay module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.relay.edgepi_relay import EdgePiRelay

@pytest.mark.parametrize("normally_open, result", [(True, True),
                                                    (False, False)])
def test_get_state_relay(mocker, normally_open, result):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.read_pin_state',
                  return_value = normally_open)
    relay = EdgePiRelay()
    assert relay.get_state_relay() == result

@pytest.mark.parametrize("pin_name", [(GpioPins.RELAY.value),
                                                     (GpioPins.RELAY.value)])
def test_toggle_relay(mocker, pin_name):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    toggle_pin = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.toggle_pin')
    relay = EdgePiRelay()
    relay.toggle_relay()
    toggle_pin.assert_called_once_with(pin_name)

def test_close_relay(mocker):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    set_pin = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.set_pin_state')
    relay = EdgePiRelay()
    relay.close_relay()
    assert set_pin.call_count == 1

def test_open_relay(mocker):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    clear_pin = mocker.patch('edgepi.relay.edgepi_relay.EdgePiGPIO.clear_pin_state')
    relay = EdgePiRelay()
    relay.open_relay()
    assert clear_pin.call_count == 1
