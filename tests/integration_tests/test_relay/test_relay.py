"relay module integration test"

import pytest
from edgepi.relay.edgepi_relay import EdgePiRelay

@pytest.mark.parametrize("normally_open, expected",
                         [(True, False),
                          (False, True)])
def test_relay_init(normally_open, expected):
    edge_relay=EdgePiRelay(normally_open)
    relay_state = edge_relay.get_state_relay()
    assert relay_state == expected

def test_relay_close():
    edge_relay=EdgePiRelay(True)
    edge_relay.close_relay()
    relay_state = edge_relay.get_state_relay()
    assert relay_state is True

def test_relay_open():
    edge_relay=EdgePiRelay(False)
    edge_relay.open_relay()
    relay_state = edge_relay.get_state_relay()
    assert relay_state is False

def test_relay_toggle():
    edge_relay=EdgePiRelay(False)
    relay_state_pre = edge_relay.get_state_relay()
    edge_relay.toggle_relay()
    relay_state_post = edge_relay.get_state_relay()
    assert relay_state_pre != relay_state_post
