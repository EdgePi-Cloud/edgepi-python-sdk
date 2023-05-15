'''Integration tests for edgepi_digital_output.py module'''

import time
import pytest
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput
from edgepi.digital_output.digital_output_constants import DoutPins


@pytest.mark.parametrize("pin_name", [
    (DoutPins.DOUT1),
    (DoutPins.DOUT2),
    (DoutPins.DOUT3),
    (DoutPins.DOUT4),
    (DoutPins.DOUT5),
    (DoutPins.DOUT6),
    (DoutPins.DOUT7),
    (DoutPins.DOUT8),
])
def test_output_high(pin_name):
    dout=EdgePiDigitalOutput()
    dout.digital_output_state(pin_name, True)
    time.sleep(1)
    gpio_stat, _ = dout.get_state(pin_name)
    assert gpio_stat is True

@pytest.mark.parametrize("pin_name", [
    (DoutPins.DOUT1),
    (DoutPins.DOUT2),
    (DoutPins.DOUT3),
    (DoutPins.DOUT4),
    (DoutPins.DOUT5),
    (DoutPins.DOUT6),
    (DoutPins.DOUT7),
    (DoutPins.DOUT8),
])
def test_output_low(pin_name):
    dout=EdgePiDigitalOutput()
    dout.digital_output_state(pin_name, False)
    time.sleep(1)
    gpio_stat, _ = dout.get_state(pin_name)
    assert gpio_stat is False

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
def test_direction_in(pin_name):
    dout=EdgePiDigitalOutput()
    dout.digital_output_direction(pin_name, True)
    time.sleep(1)
    _, gpio_dir = dout.get_state(pin_name)
    assert gpio_dir is True

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
def test_direction_out(pin_name):
    dout=EdgePiDigitalOutput()
    dout.digital_output_direction(pin_name, False)
    time.sleep(1)
    _, gpio_dir = dout.get_state(pin_name)
    assert gpio_dir is False
