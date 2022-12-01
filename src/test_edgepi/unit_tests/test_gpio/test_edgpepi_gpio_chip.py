"""unit tests for edgepi_gpio_chip module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.gpio.gpio_configs import GpioConfigs, generate_pin_info
from edgepi.gpio.edgepi_gpio_chip import EdgePiGPIOChip


@pytest.fixture(name='mock_gpio')
def fixture_mock_i2c_lib(mocker):
    yield mocker.patch('edgepi.peripherals.gpio.GPIO')

@pytest.mark.parametrize("config", [(GpioConfigs.DAC.value)])
def test_edgepi_gpio_init(config):
    gpio = EdgePiGPIOChip(config=config)
    assert gpio.dict_gpiochip_pins == generate_pin_info(config)
    