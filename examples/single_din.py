"""Example reading from individual DIN pins"""

import time

from edgepi.digital_input.digital_input_constants import DinPins
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput

ITER = 250

def run_test():
    """
    This test performs 2000 Digital input reads, with a total of 250 per DIN pin.
    """
    digital_input = EdgePiDigitalInput()

    state_list = []
    choices = [
        DinPins.DIN1, DinPins.DIN2, DinPins.DIN3, DinPins.DIN4,
        DinPins.DIN5, DinPins.DIN6, DinPins.DIN7, DinPins.DIN8,
    ]

    start = time.time()
    for _ in range(ITER):
        for din in choices:
            pin_state = digital_input.digital_input_state(din)
            state_list += [pin_state]

    elapsed = time.time() - start

    print(state_list[-9:-1])
    print(f"Time elapsed {elapsed/ITER:.6f} s")
    print(f"Frequency {ITER/elapsed:.4f} hz")

if __name__ == "__main__":
    run_test()
