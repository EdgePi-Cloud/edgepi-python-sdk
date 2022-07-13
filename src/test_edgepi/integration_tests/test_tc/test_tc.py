"""
Hardware-dependent integration tests for thermocouple module
"""

import pytest

from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import AvgMode, TCAddresses


def test_tc_init():
    tc = EdgePiTC()
    assert tc.spi.devpath == f"/dev/spidev{6}.{2}"


@pytest.fixture(name="tc")
def fixture_test_edgepi_tc():
    return EdgePiTC()


@pytest.mark.parametrize(
    "args, updated_regs",
    [
        ({"average_mode": AvgMode.AVG_2}, {TCAddresses.CR1_W.value: 0x13}),
    ],
)
def test_set_config(tc, args, updated_regs):
    # reset registers to default values
    tc.reset_registers()

    # update registers with user args
    tc.set_config(**args)

    # read updated register values
    # pylint: disable=protected-access
    reg_values = tc._EdgePiTC__read_registers_to_map()

    # compare to expected register values
    for addx, value in reg_values.items():
        # check registers not updated have not been changed
        if addx not in updated_regs:
            assert value == tc.default_reg_values[addx]
        # check updates were applied
        else:
            assert value == updated_regs[addx]
