"""Example reading from DIN using the batched function"""

import time

from edgepi.digital_input.digital_input_constants import DinPins
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput

ITER = 250

def run_test():
    """
    This test performs 2000 Digital input reads, batched 8 reads at a time.
    """
    digital_input = EdgePiDigitalInput()

    state_list = []
    choices = [
        DinPins.DIN1, DinPins.DIN2, DinPins.DIN3, DinPins.DIN4,
        DinPins.DIN5, DinPins.DIN6, DinPins.DIN7, DinPins.DIN8,
    ]

    start = time.time()
    for i in range(ITER):
        pin_states = digital_input.digital_input_state_batch(choices)
        state_list += pin_states
        if i % 100 == 99:
            print(f"DIN Pins: {pin_states}")

    elapsed = time.time() - start
    print(f"Time elapsed {elapsed/ITER:.6f} s")
    print(f"Frequency {ITER/elapsed:.4f} hz")

if __name__ == "__main__":
    run_test()
