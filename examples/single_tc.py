"""Example reading from the thermocouple (tc)"""

import time

from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import ConvMode

ITER = 25

def run_test():
    """
    This test 
    """
    edgepi_tc = EdgePiTC()
    edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)

    cj_temperatures = []
    lin_temperatures = []

    start = time.time()
    for _ in range(ITER):
        iter_start = time.time()

        # make a single temperature measurement
        cold_junction, linearized = edgepi_tc.read_temperatures()
        cj_temperatures += [cold_junction]
        lin_temperatures += [linearized]

        # It doesn't make sense to read thermocoupler values faster than 10hz as they
        # won't be updated. You can try it here if you'd like!
        sleep_time = 0.1 - (time.time() - iter_start)
        time.sleep(0.0 if sleep_time < 0.0 else sleep_time)

    elapsed = time.time() - start

    print(f"TC Reads: {lin_temperatures}")
    print(f"Time elapsed {elapsed/ITER:.6f} s")
    print(f"Frequency {ITER/elapsed:.4f} hz")

if __name__ == "__main__":
    run_test()
