"""Integration tests for LED module"""

import pytest

from edgepi.gpio.gpio_configs import LEDPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.led.edgepi_leds import EdgePiLED

@pytest.fixture(name='led')
def fixture_led():
    return EdgePiLED()

@pytest.fixture(name='gpio')
def fixture_gpio():
    return EdgePiGPIO()

@pytest.mark.parametrize('led_name', [
    (LEDPins.LED_OVR1),
    (LEDPins.LED_OVR2),
    (LEDPins.LED_OVR3),
    (LEDPins.LED_OVR4),
    (LEDPins.LED_OVR5),
    (LEDPins.LED_OVR6),
    (LEDPins.LED_OVR7),
    (LEDPins.LED_OVR8),
])
def test_turn_led_on(led_name, led, gpio):
    led.turn_led_on(led_name)
    state = gpio.read_pin_state(led_name.value)
    assert state is True


@pytest.mark.parametrize('led_name', [
    (LEDPins.LED_OVR1),
    (LEDPins.LED_OVR2),
    (LEDPins.LED_OVR3),
    (LEDPins.LED_OVR4),
    (LEDPins.LED_OVR5),
    (LEDPins.LED_OVR6),
    (LEDPins.LED_OVR7),
    (LEDPins.LED_OVR8),
])
def test_turn_led_off(led_name, led, gpio):
    led.turn_led_off(led_name)
    state = gpio.read_pin_state(led_name.value)
    assert state is False


@pytest.mark.parametrize('led_name', [
    (LEDPins.LED_OVR1),
    (LEDPins.LED_OVR2),
    (LEDPins.LED_OVR3),
    (LEDPins.LED_OVR4),
    (LEDPins.LED_OVR5),
    (LEDPins.LED_OVR6),
    (LEDPins.LED_OVR7),
    (LEDPins.LED_OVR8),
])
def test_get_led_state(led_name, led):
    led.turn_led_on(led_name)
    state = led.get_led_state(led_name)
    assert state is True
    led.turn_led_off(led_name)
    state = led.get_led_state(led_name)
    assert state is False


@pytest.mark.parametrize('led_name', [
    (LEDPins.LED_OVR1),
    (LEDPins.LED_OVR2),
    (LEDPins.LED_OVR3),
    (LEDPins.LED_OVR4),
    (LEDPins.LED_OVR5),
    (LEDPins.LED_OVR6),
    (LEDPins.LED_OVR7),
    (LEDPins.LED_OVR8),
])
def test_toggle_led(led_name, led):
    led.turn_led_on(led_name)
    led.toggle_led(led_name)
    state = led.get_led_state(led_name)
    assert state is False
    led.toggle_led(led_name)
    state = led.get_led_state(led_name)
    assert state is True
    led.turn_led_off(led_name)
