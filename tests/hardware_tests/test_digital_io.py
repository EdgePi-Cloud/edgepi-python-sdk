'''Hardware tests for verifying digital input and output module'''

import pytest
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput
from edgepi.gpio.gpio_constants import GpioPins

@pytest.mark.parametrize("din, dout", [
    (GpioPins.DIN1, GpioPins.DOUT1),
    (GpioPins.DIN2, GpioPins.DOUT2),
    (GpioPins.DIN3, GpioPins.DOUT3),
    (GpioPins.DIN4, GpioPins.DOUT4),
    (GpioPins.DIN5, GpioPins.DOUT5),
    (GpioPins.DIN6, GpioPins.DOUT6),
    (GpioPins.DIN7, GpioPins.DOUT7),
    (GpioPins.DIN8, GpioPins.DOUT8),
])
def test_input_state(pin_name):
    din=EdgePiDigitalInput()
    dout = EdgePiDigitalOutput()
    initial_state = din.digital_input_state(pin_name)
    dout.digital_output_state(pin_name, True)
    changed_state = din.digital_input_state(pin_name)
    assert initial_state is not changed_state
    dout.digital_output_state(pin_name, True)
    changed_state = din.digital_input_state(pin_name)
    assert initial_state is changed_state
    