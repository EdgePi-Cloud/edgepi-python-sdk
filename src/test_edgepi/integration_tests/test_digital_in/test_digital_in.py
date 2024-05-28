'''Integration tests for edgepi_digital_input.py module'''

import time
import pytest

from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput
from edgepi.digital_input.digital_input_constants import DinPins

@pytest.mark.parametrize("pin_name", [
    (DinPins.DIN1),
    (DinPins.DIN2),
    (DinPins.DIN3),
    (DinPins.DIN4),
    (DinPins.DIN5),
    (DinPins.DIN6),
    (DinPins.DIN7),
    (DinPins.DIN8),
])
def test_input_state(pin_name):
    din = EdgePiDigitalInput()
    pin_state = din.digital_input_state(pin_name)
    assert pin_state is False

@pytest.mark.parametrize("pin_names", [
    ([
        DinPins.DIN1, DinPins.DIN2, DinPins.DIN3, DinPins.DIN4, 
        DinPins.DIN5, DinPins.DIN6, DinPins.DIN7, DinPins.DIN8
    ]),
])
def test_input_state_speed(pin_names):
    TARGET_MS = 1
    
    din = EdgePiDigitalInput()
    
    start = time.time()
    
    pin_states = []
    for _ in range(500):
        tmp = din.digital_input_state_batch(pin_names)
        pin_states += tmp
        
    avg = 1000.0 * (time.time() - start) / 500
    #print(avg)
    assert avg < TARGET_MS