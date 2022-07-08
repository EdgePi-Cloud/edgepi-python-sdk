"""unit tests for edgepi_gpio module"""

import sys
from unittest import mock
from unittest.mock import patch

import pytest
from edgepi.gpio.gpio_configs import GpioConfigs
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

if sys.platform != "linux":
    sys.modules["periphery"] = mock.MagicMock()


@pytest.mark.parametrize(
    "mock_expect,config, result",
    [
        (["/dev/i2c-10"], "dac", [GpioConfigs.DAC.value]),
        (["/dev/i2c-10"], "adc", [GpioConfigs.ADC.value]),
        (["/dev/i2c-10"], "rtd", [GpioConfigs.RTD.value]),
        (["/dev/i2c-10"], "led", [GpioConfigs.LED.value]),
    ],
)
@patch("edgepi.peripherals.i2c.I2C")
def test_edgepi_gpio_init(i2c_mock, mock_expect, config, result):
    i2c_mock.fd = mock_expect[0]
    gpio_ctrl = EdgePiGPIO(config)
    assert gpio_ctrl.config == result[0]
