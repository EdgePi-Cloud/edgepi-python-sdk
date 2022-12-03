"""unit tests for gpio.py module"""
# pylint: disable=wrong-import-position
from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
import pytest
from edgepi.peripherals.gpio import GpioDevice


@pytest.mark.parametrize(
    "fd",
    [
        ("/dev/gpiochip0", 27, "in", "pull_down"),
    ],
)
def test_gpio_init_param(mocker, fd):
    mocker.patch("edgepi.peripherals.gpio.GPIO")
    gpio = GpioDevice(fd)
    assert gpio.fd == fd
    assert gpio.gpio is None

@pytest.mark.parametrize(
    "fd, result",
    [
        ("/dev/gpiochip0", True),
        ("/dev/gpiochip0", False),
        ("/dev/gpiochip0",True),
        ("/dev/gpiochip0", False),
    ],
)
def test_gpio_read_state(mocker, fd, result):
    mocker.patch("edgepi.peripherals.gpio.GpioDevice.read_state", return_value = result)
    gpio = GpioDevice(fd)
    assert gpio.read_state() == result
