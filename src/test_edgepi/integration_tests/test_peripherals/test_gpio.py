"""integration tests for gpio.py module"""

import pytest
from edgepi.peripherals.gpio import GpioDevice


@pytest.mark.parametrize(
    "fd",
    [
        ("/dev/gpiochip0"),
        ("/dev/gpiochip0"),
        ("/dev/gpiochip0"),
        ("/dev/gpiochip0"),
    ],
)
def test_gpio_init_param(fd):
    gpio = GpioDevice(fd)
    assert gpio.gpio_fd == fd
