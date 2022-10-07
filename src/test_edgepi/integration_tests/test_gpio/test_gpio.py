'''Integration tests for edgepi_gpio.py module'''


import pytest
from edgepi.gpio.gpio_configs import GpioConfigs, _list_of_LED_gpios
from edgepi.gpio.edgepi_gpio import EdgePiGPIO


@pytest.mark.parametrize("gpio_config, pin_name", [
    (GpioConfigs.LED, "LED_OVR1"),
    (GpioConfigs.LED, "LED_OVR2"),
    (GpioConfigs.LED, "LED_OVR3"),
    (GpioConfigs.LED, "LED_OVR4"),
    (GpioConfigs.LED, "LED_OVR5"),
    (GpioConfigs.LED, "LED_OVR6"),
    (GpioConfigs.LED, "LED_OVR7"),
    (GpioConfigs.LED, "LED_OVR8"),
])
def test_read_expander_pin(gpio_config, pin_name):
    gpio = EdgePiGPIO(gpio_config.value)
    pin_val = gpio.read_expander_pin(pin_name)
    print(pin_val)


@pytest.mark.parametrize("gpio_config, pin_name", [
    (GpioConfigs.LED, "LED_OVR1"),
    (GpioConfigs.LED, "LED_OVR2"),
    (GpioConfigs.LED, "LED_OVR3"),
    (GpioConfigs.LED, "LED_OVR4"),
    (GpioConfigs.LED, "LED_OVR5"),
    (GpioConfigs.LED, "LED_OVR6"),
    (GpioConfigs.LED, "LED_OVR7"),
    (GpioConfigs.LED, "LED_OVR8"),
])
def test_get_pin_direction(gpio_config, pin_name):
    gpio = EdgePiGPIO(gpio_config.value)
    pin_val = gpio.get_pin_direction(pin_name)
    print(pin_val)
