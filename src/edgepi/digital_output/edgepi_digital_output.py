
"""Digital Output Module"""

import time

from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi.dac.dac_constants import DACChannel as Ch
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_output.digital_output_constants import DoutPins, DoutTriState
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

class InvalidPinName(Exception):
    """Raised invalid pin name"""

class EdgePiDigitalOutput():
    """handling digital output"""

    _dout_aout_pair = {
        DoutPins.DOUT1 : GpioPins.AO_EN1,
        DoutPins.DOUT2 : GpioPins.AO_EN2,
        DoutPins.DOUT3 : GpioPins.AO_EN3,
        DoutPins.DOUT4 : GpioPins.AO_EN4,
        DoutPins.DOUT5 : GpioPins.AO_EN5,
        DoutPins.DOUT6 : GpioPins.AO_EN6,
        DoutPins.DOUT7 : GpioPins.AO_EN7,
        DoutPins.DOUT8 : GpioPins.AO_EN8,
    }
    _dout_dac_pair = {
        DoutPins.DOUT1 : Ch.AOUT1,
        DoutPins.DOUT2 : Ch.AOUT2,
        DoutPins.DOUT3 : Ch.AOUT3,
        DoutPins.DOUT4 : Ch.AOUT4,
        DoutPins.DOUT5 : Ch.AOUT5,
        DoutPins.DOUT6 : Ch.AOUT6,
        DoutPins.DOUT7 : Ch.AOUT7,
        DoutPins.DOUT8 : Ch.AOUT8,
    }
    def __init__(self):
        # To limit access to input functionality, using composition rather than inheritance
        self.gpio = EdgePiGPIO()
        self.dac = EdgePiDAC()

    def set_dout_state(self, pin_name: DoutPins = None, state: DoutTriState = None):
        """
        change the output state of the pin to the state passed as argument
        Args:
            pin_name (DoutPins): DoutPins enums
            state (bool): True = output high, False, output low
        """
        if pin_name is None or pin_name.value not in [pins.value for pins in DoutPins]:
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')
        if state == DoutTriState.HIGH:
            # Clear AO_EN pin to disable the AnalogOut first before switching the DOUT high
            self.gpio.set_pin_state(self._dout_aout_pair[pin_name].value)
            self.gpio.set_pin_state(pin_name.value)
            self.gpio.clear_pin_state(self._dout_aout_pair[pin_name].value)
        elif state == DoutTriState.LOW:
            # In order to safely switch internal MUX circuit, Analog enable pin must be set and
            # cleared with a small time delay. This allows overriding AOUT with DOUT
            self.gpio.set_pin_state(self._dout_aout_pair[pin_name].value)
            self.gpio.clear_pin_state(pin_name.value)
            time.sleep(0.05)
            self.gpio.clear_pin_state(self._dout_aout_pair[pin_name].value)
        elif state == DoutTriState.HI_Z:
            # very similar to LOW state, set analog_enable, clear dout and set direction to input
            # set dac to 0V
            self.dac.write_voltage(self._dout_dac_pair[pin_name],0)
            self.gpio.set_pin_state(self._dout_aout_pair[pin_name].value)
            self.gpio.clear_pin_state(pin_name.value)
            self.gpio.set_pin_direction_in(pin_name.value)
        else:
            raise ValueError(f'Invalid state passed: {state}')

    def get_state(self, pin_name: DoutPins = None):
        """
        Get the current state of the specified pin
        Args:
            pin_name (DoutPins): DoutPins enums
        Returns:
            state (Bool): True High, False, Low
            direction (Bool): True Input, False Output
        """
        if pin_name is None or pin_name.value not in [pins.value for pins in DoutPins]:
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')
        state = self.gpio.read_pin_state(pin_name.value)
        direction = self.gpio.get_pin_direction(pin_name.value)
        if not direction and state:
            return DoutTriState.HIGH
        if not direction and not state:
            return DoutTriState.LOW
        return DoutTriState.HI_Z
