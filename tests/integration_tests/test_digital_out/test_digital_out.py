'''Integration tests for edgepi_digital_output.py module'''

import time
import pytest
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput
from edgepi.gpio.gpio_constants import GpioPins

@pytest.mark.parametrize("pin_name", [
    (GpioPins.DOUT1),
    (GpioPins.DOUT2),
    (GpioPins.DOUT3),
    (GpioPins.DOUT4),
    (GpioPins.DOUT5),
    (GpioPins.DOUT6),
    (GpioPins.DOUT7),
    (GpioPins.DOUT8),
])
def test_output_high(pin_name):
    dout=EdgePiDigitalOutput()
    dout.digital_output_state(pin_name, True)
    time.sleep(1)

@pytest.mark.parametrize("pin_name", [
    (GpioPins.DOUT1),
    (GpioPins.DOUT2),
    (GpioPins.DOUT3),
    (GpioPins.DOUT4),
    (GpioPins.DOUT5),
    (GpioPins.DOUT6),
    (GpioPins.DOUT7),
    (GpioPins.DOUT8),
])
def test_output_low(pin_name):
    dout=EdgePiDigitalOutput()
    dout.digital_output_state(pin_name, False)
    time.sleep(1)
