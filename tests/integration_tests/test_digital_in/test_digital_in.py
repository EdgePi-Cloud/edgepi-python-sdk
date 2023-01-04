'''Integration tests for edgepi_digital_input.py module'''

import pytest
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput
from edgepi.gpio.gpio_constants import GpioPins

@pytest.mark.parametrize("pin_name", [
    (GpioPins.DIN1),
    (GpioPins.DIN2),
    (GpioPins.DIN3),
    (GpioPins.DIN4),
    (GpioPins.DIN5),
    (GpioPins.DIN6),
    (GpioPins.DIN7),
    (GpioPins.DIN8),
])
def test_input_state(pin_name):
    din=EdgePiDigitalInput()
    pin_state = din.digital_input_state(pin_name)
    assert pin_state == False
    
