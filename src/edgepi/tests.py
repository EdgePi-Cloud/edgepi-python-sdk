import logging
import time
from tc.edgepi_tc import *
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    edgepi_tc = EdgePiTC()
    # edgepi_tc._EdgePiTC__read_registers()
    # edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE, fault_mask=FaultMasks.OVUV_MASK_OFF)
    # values = [0,3,255,127,192,127,255,128,0,0,0,0]
    # print('cr1 value before transfer')
    # tc_dev.read_registers()
    # tc_dev.set_average_mode(AvgMode.AVG_4)
    # print('cr1 value after transfer')
    # edgepi_tc._EdgePiTC__read_register(TCAddresses.MASK_R.value)
    # edgepi_tc.single_sample()

    # set thermocouple to measure temperature continuously
    # edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)

    # # stop_condition = False

    # while True:
    #     time.sleep(1)                             # wait 1 second between measurements
    #     temps = edgepi_tc.read_temperatures()     # read cold junction and linearized thermocouple temperatures
    #     print(temps)

    #     # stop continuous measurements if some condition is met
    #     if stop_condition:
    #         edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)
    #         break
    faults = edgepi_tc.read_faults()
    print('\n\n')
    pprint(faults)