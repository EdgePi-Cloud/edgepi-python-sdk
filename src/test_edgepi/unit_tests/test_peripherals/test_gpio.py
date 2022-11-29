"""unit tests for gpio.py module"""
# pylint: disable=wrong-import-position
from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
import pytest
from edgepi.peripherals.gpio import GpioDevice


@pytest.mark.parametrize(
    "fd, pin_num, pin_dir, pin_bias",
    [
        ("/dev/gpiochip0", 27, "in", "pull_down"),
        ("/dev/gpiochip0", 6, "in", "pull_down"),
        ("/dev/gpiochip0", 6, "in", "pull_down"),
        ("/dev/gpiochip0", 13, "out", "pull_down"),
    ],
)
def test_gpio_init_param(mocker, fd, pin_num, pin_dir, pin_bias):
    mocker.patch("edgepi.peripherals.gpio.GPIO")
    gpio = GpioDevice(pin_num, pin_dir, pin_bias)
    assert gpio.fd == fd
    assert gpio.pin_num == pin_num
    assert gpio.pin_dir == pin_dir
    assert gpio.pin_bias == pin_bias

@pytest.mark.parametrize(
    "pin_num, pin_dir, pin_bias, result",
    [
        (27, "in", "pull_down", True),
        (6, "in", "pull_down", False),
        (6, "in", "pull_down",True),
        (13, "out", "pull_down", False),
    ],
)
def test_gpio_read_state(mocker, pin_num, pin_dir, pin_bias, result):
    mocker.patch("edgepi.peripherals.gpio.GpioDevice.read_state", return_value = result)
    gpio = GpioDevice(pin_num, pin_dir, pin_bias)
    assert gpio.read_state() == result
