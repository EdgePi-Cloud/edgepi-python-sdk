"""unit tests for edgepi_gpio module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from copy import deepcopy

import pytest
from edgepi.gpio.gpio_configs import GpioConfigs
from edgepi.gpio.edgepi_gpio_expander import EdgePiGPIOExpander
from edgepi.gpio.edgepi_gpio_chip import EdgePiGPIOChip

@pytest.fixture(name='mock_perph')
def fixture_mock_i2c_lib(mocker):
    mocker.patch('edgepi.peripherals.i2c.I2C')
    mocker.patch('edgepi.peripherals.i2c.I2C')
