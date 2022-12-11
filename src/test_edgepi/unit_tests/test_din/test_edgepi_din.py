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
                         (GpioPins.DIN3, True, True),
                         (GpioPins.DIN4, True, True),
                         (GpioPins.DIN5, True, True),
                         (GpioPins.DIN6, True, True),
                         (GpioPins.DIN7, True, True),
                         (GpioPins.DIN8, True, True),
                         (GpioPins.DIN1, False, False),
                         (GpioPins.DIN2, False, False),
                         (GpioPins.DIN3, False, False),
                         (GpioPins.DIN4, False, False),
                         (GpioPins.DIN5, False, False),
                         (GpioPins.DIN6, False, False),
                         (GpioPins.DIN7, False, False),
                         (GpioPins.DIN8, False, False)])
def test_edgepi_digital_input_state(mocker, pin_name, mock_value, result, din):
    mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIOChip.read_gpio_pin_state",
                 return_value = mock_value)
    assert din.digital_input_state(pin_name) == result
    