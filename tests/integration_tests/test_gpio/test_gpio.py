'''Integration tests for edgepi_gpio.py module'''


import pytest
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

def reset_pins(gpio, pin_name):
    """Reset pins to power up default setting"""
    gpio.set_pin_direction_in(pin_name)
    gpio.set_pin_state(pin_name)

@pytest.mark.parametrize("pin_name", [
    ("LED_OVR1"),
    ("LED_OVR2"),
    ("LED_OVR3"),
    ("LED_OVR4"),
    ("LED_OVR5"),
    ("LED_OVR6"),
    ("LED_OVR7"),
    ("LED_OVR8"),
])
def test_read_pin_state(pin_name):
    gpio = EdgePiGPIO()
    gpio.read_pin_state(pin_name)
    gpio.clear_pin_state(pin_name)
    pin_val = gpio.read_pin_state(pin_name)
    assert pin_val is False
    gpio.set_pin_state(pin_name)
    pin_val = gpio.read_pin_state(pin_name)
    assert pin_val is True
    reset_pins(gpio, pin_name)


@pytest.mark.parametrize("pin_name", [
    ("LED_OVR1"),
    ("LED_OVR2"),
    ("LED_OVR3"),
    ("LED_OVR4"),
    ("LED_OVR5"),
    ("LED_OVR6"),
    ("LED_OVR7"),
    ("LED_OVR8"),
])
def test_get_pin_direction(pin_name):
    gpio = EdgePiGPIO()
    gpio.set_pin_direction_out(pin_name)
    pin_dir = gpio.get_pin_direction(pin_name)
    assert pin_dir is False
    reset_pins(gpio, pin_name)


@pytest.mark.parametrize("pin_name", [
    ("LED_OVR1"),
    ("LED_OVR2"),
    ("LED_OVR3"),
    ("LED_OVR4"),
    ("LED_OVR5"),
    ("LED_OVR6"),
    ("LED_OVR7"),
    ("LED_OVR8"),
])
def test_set_pin_direction_in(pin_name):
    gpio = EdgePiGPIO()
    gpio.set_pin_direction_in(pin_name)
    pin_dir = gpio.get_pin_direction(pin_name)
    assert pin_dir is True
    reset_pins(gpio, pin_name)



@pytest.mark.parametrize("pin_name", [
    ("LED_OVR1"),
    ("LED_OVR2"),
    ("LED_OVR3"),
    ("LED_OVR4"),
    ("LED_OVR5"),
    ("LED_OVR6"),
    ("LED_OVR7"),
    ("LED_OVR8"),
])
def test_set_pin_direction_out(pin_name):
    gpio = EdgePiGPIO()
    gpio.set_pin_direction_out(pin_name)
    pin_dir = gpio.get_pin_direction(pin_name)
    pin_val = gpio.read_pin_state(pin_name)
    assert pin_dir is False
    assert pin_val is True
    reset_pins(gpio, pin_name)


@pytest.mark.parametrize("pin_name", [
    ("LED_OVR1"),
    ("LED_OVR2"),
    ("LED_OVR3"),
    ("LED_OVR4"),
    ("LED_OVR5"),
    ("LED_OVR6"),
    ("LED_OVR7"),
    ("LED_OVR8"),
])
def test_set_pin_state(pin_name):
    gpio = EdgePiGPIO()
    gpio.set_pin_state(pin_name)
    pin_val = gpio.read_pin_state(pin_name)
    assert pin_val is True
    reset_pins(gpio, pin_name)



@pytest.mark.parametrize("pin_name", [
    ("LED_OVR1"),
    ("LED_OVR2"),
    ("LED_OVR3"),
    ("LED_OVR4"),
    ("LED_OVR5"),
    ("LED_OVR6"),
    ("LED_OVR7"),
    ("LED_OVR8"),
])
def test_toggle_expander_pin(pin_name):
    gpio = EdgePiGPIO()
    pin_val_1 = gpio.read_pin_state(pin_name)
    gpio.toggle_pin(pin_name)
    pin_val_2 = gpio.read_pin_state(pin_name)
    assert pin_val_2 is not pin_val_1
    reset_pins(gpio, pin_name)



@pytest.mark.parametrize("pin_name", [
    ("LED_OVR1"),
    ("LED_OVR2"),
    ("LED_OVR3"),
    ("LED_OVR4"),
    ("LED_OVR5"),
    ("LED_OVR6"),
    ("LED_OVR7"),
    ("LED_OVR8"),
])
def test_clear_pin_state(pin_name):
    gpio = EdgePiGPIO()
    gpio.clear_pin_state(pin_name)
    pin_val = gpio.read_pin_state(pin_name)
    assert pin_val is False
    reset_pins(gpio, pin_name)
