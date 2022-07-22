"""integration tests for gpio.py module"""

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
def test_gpio_init_param(fd, pin_num, pin_dir, pin_bias):
    gpio = GpioDevice(pin_num, pin_dir, pin_bias)
    assert gpio.fd == fd
    assert gpio.pin_num == pin_num
    assert gpio.pin_dir == pin_dir
    assert gpio.pin_bias == pin_bias
