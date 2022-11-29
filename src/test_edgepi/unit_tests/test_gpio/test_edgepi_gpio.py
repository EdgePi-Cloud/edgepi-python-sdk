"""unit tests for edgepi_gpio module"""

# pylint: disable=protected-access
# pylint: disable=C0413

from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.gpio.gpio_configs import GpioConfigs, generate_expander_pin_info
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

# @pytest.fixture(name='gpio_mock')
# def fixture_mock_i2c_lib(mocker):
#     mocker.patch('edgepi.peripherals.i2c.I2C')
#     mocker.patch('edgepi.peripherals.gpio.GPIO')

@pytest.mark.parametrize("config",
                        [(GpioConfigs.DAC)])
def test_edgepi_gpio_init(mocker, config):
    mocker.patch('edgepi.peripherals.i2c.I2C')
    mocker.patch('edgepi.peripherals.gpio.GPIO')
    edgepi_gpio = EdgePiGPIO(config.value)
    expander_pin_dict = generate_expander_pin_info()
    assert edgepi_gpio.expander_pin_dict == expander_pin_dict
