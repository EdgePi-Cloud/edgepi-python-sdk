'''Integration tests for edgepi_gpio.py module'''


import pytest
from edgepi.gpio.gpio_configs import GpioConfigs
from edgepi.gpio.edgepi_gpio import EdgePiGPIO


@pytest.mark.parametrize("gpio_config, pin_name", [
    (GpioConfigs.LED, "LED_OVR1"),
    (GpioConfigs.LED, "LED_OVR2"),
    (GpioConfigs.LED, "LED_OVR3"),
    (GpioConfigs.LED, "LED_OVR4"),
    # (GpioConfigs.LED, "LED_OVR5"),
    # (GpioConfigs.LED, "LED_OVR6"),
    # (GpioConfigs.LED, "LED_OVR7"),
    # (GpioConfigs.LED, "LED_OVR8"),
])
def test_read_expander_pin(gpio_config, pin_name):
    gpio = EdgePiGPIO(gpio_config.value)
    gpio.read_expander_pin_state(pin_name)
    gpio.clear_expander_pin(pin_name)
    pin_val = gpio.read_expander_pin_state(pin_name)
    # TODO: setting pins 5-8 to high causes crash
    assert pin_val is False
    gpio.set_expander_pin(pin_name)
    pin_val = gpio.read_expander_pin_state(pin_name)
    assert pin_val is True


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
    gpio.set_pin_direction_out(pin_name)
    pin_dir = gpio.get_pin_direction(pin_name)
    assert pin_dir is False


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
def test_set_pin_direction_out(gpio_config, pin_name):
    gpio = EdgePiGPIO(gpio_config.value)
    gpio.set_pin_direction_out(pin_name)
    pin_dir = gpio.get_pin_direction(pin_name)
    pin_val = gpio.read_expander_pin_state(pin_name)
    assert pin_dir is False
    assert pin_val is False


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
def test_set_pin_direction_in(gpio_config, pin_name):
    gpio = EdgePiGPIO(gpio_config.value)
    gpio.set_pin_direction_in(pin_name)
    pin_dir = gpio.get_pin_direction(pin_name)
    assert pin_dir is True


@pytest.mark.parametrize("gpio_config, pin_name", [
    (GpioConfigs.LED, "LED_OVR1"),
    (GpioConfigs.LED, "LED_OVR2"),
    (GpioConfigs.LED, "LED_OVR3"),
    (GpioConfigs.LED, "LED_OVR4"),
    # (GpioConfigs.LED, "LED_OVR5"),
    # (GpioConfigs.LED, "LED_OVR6"),
    # (GpioConfigs.LED, "LED_OVR7"),
    # (GpioConfigs.LED, "LED_OVR8"),
])
def test_set_expander_pin(gpio_config, pin_name):
    gpio = EdgePiGPIO(gpio_config.value)
    # TODO: setting pins 5-8 to high causes crash
    gpio.set_expander_pin(pin_name)
    pin_val = gpio.read_expander_pin_state(pin_name)
    assert pin_val is True


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
def test_clear_expander_pin(gpio_config, pin_name):
    gpio = EdgePiGPIO(gpio_config.value)
    gpio.clear_expander_pin(pin_name)
    pin_val = gpio.read_expander_pin_state(pin_name)
    assert pin_val is False
