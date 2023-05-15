# EdgePi LED Module

# Hardware

The EdgePi has an array of eight programmable LED lights. The LED module allows users to interact with each LED individually.

# Example Code
This code example demonstrates how to use the LED module to turn an LED on and off:
```python
from edgepi.led.edgepi_leds import EdgePiLED
from edgepi.led.led_constants import LEDPins

leds = EdgePiLED()

leds.turn_on(LEDPins.LED_OVR1)

leds.turn_off(LEDPins.LED_OVR1)
```

# Functionalities

Currently, the LED module offers the following functionalities:
1. Turn an LED on or off.
2. Toggle an LED to the opposite state.
3. Read an LED's on/off state.

# User Guide

## Turn an LED on/off
```python
leds.turn_on(LEDPins.LED_OVR1)

leds.turn_off(LEDPins.LED_OVR1)
```

## Toggle an LED to the opposite state
```python
leds.toggle_led(LEDPins.LED_OVR1)
```

## Read an LED's on/off state
```python
state = leds.get_led_state(LEDPins.LED_OVR1)
```

# Limitations
