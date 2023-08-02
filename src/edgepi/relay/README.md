# EdgePi Relay Module
Relay module is used to control the state of the relay. It can be setup to open/close the relay.

# Hardware
Relay_NO and Relay_COM on the terminal block can be used to setup a relay circuit.

# Example Code
```python
from edgepi.relay.edgepi_relay import EdgePiRelay

edgepi_relay = EdgePiRelay()
# Open Relay
edgepi_relay.open_relay()
# Get Relay state
state = edgepi_relay.get_state_relay()
# Close Relay
edgepi_relay.close_relay()

```
__NOTE:__ When the module is instantiated after the power down, get_state_relay() may report wrong value. A open/close **MUST be** called before calling get_state_relay() for the first time.

# Limitations 

