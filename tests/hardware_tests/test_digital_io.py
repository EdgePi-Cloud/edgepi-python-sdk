'''Hardware tests for verifying digital input and output module'''

from time import sleep
import pytest
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput
from edgepi.digital_input.digital_input_constants import DinPins
from edgepi.digital_output.digital_output_constants import DoutPins

@pytest.mark.parametrize("din_pin, dout_pin", [
    (DinPins.DIN1, DoutPins.DOUT1),
    (DinPins.DIN2, DoutPins.DOUT2),
    (DinPins.DIN3, DoutPins.DOUT3),
    (DinPins.DIN4, DoutPins.DOUT4),
    (DinPins.DIN5, DoutPins.DOUT5),
    (DinPins.DIN6, DoutPins.DOUT6),
    (DinPins.DIN7, DoutPins.DOUT7),
    (DinPins.DIN8, DoutPins.DOUT8),
])
def test_input_state(din_pin, dout_pin):
    din=EdgePiDigitalInput()
    dout = EdgePiDigitalOutput()
    initial_state = din.digital_input_state(din_pin)
    dout.set_dout_state(dout_pin, True)
    sleep(0.1)
    changed_state = din.digital_input_state(din_pin)
    assert initial_state is not changed_state
    dout.set_dout_state(dout_pin, False)
    sleep(0.1)
    changed_state = din.digital_input_state(din_pin)
    assert initial_state is changed_state
