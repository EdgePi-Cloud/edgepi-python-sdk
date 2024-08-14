import time

from edgepi.digital_input.digital_input_constants import DinPins
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput

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
    for i in range(250):
        for din in choices:
            pin_state = digital_input.digital_input_state(din)
            state_list += [pin_state]
        if i % 100 == 99:
            print(f"DIN Pins: {state_list[-9:-1]}")

    print("elapsed {:.4f}s".format(time.time() - start))

if __name__ == "__main__":
    # TODO: evaluate this on the edgepi hardware
    run_test()
