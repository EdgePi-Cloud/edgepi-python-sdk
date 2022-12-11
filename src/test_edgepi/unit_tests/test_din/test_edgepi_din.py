"""unit tests for edgepi_gpio module"""

# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.din.edgepi_din import EdgePiDIN

@pytest.fixture(name="din")
def fixture_test_dac(mocker):
    mocker.patch('edgepi.gpio.edgepi_gpio.EdgePiGPIO')
    # mocker.patch('edgepi.din.EdgePiDIN.EdgePiGPIO.EdgePiGPIOChip')
    yield EdgePiDIN()

@pytest.mark.parametrize("pin_name, mock_value, result",
                        [(GpioPins.DIN1, True, True),
                         (GpioPins.DIN2, True, True),
                         (GpioPins.DIN3, True, True)])
def test_edgepi_digital_input_state(mocker, pin_name, mock_value, result, din):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.read_gpio_pin_state",
                 return_value = mock_value)
    assert din.digital_input_state(pin_name) == result
    