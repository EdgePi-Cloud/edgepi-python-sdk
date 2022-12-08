"""integration tests for spi.py module"""

import pytest
from edgepi.peripherals.spi import SpiDevice


@pytest.mark.parametrize(
    "dev_id, bus_num, result",
    [
        (0, 6, "/dev/spidev6.0"),
        (1, 6, "/dev/spidev6.1"),
        (2, 6, "/dev/spidev6.2"),
        (3, 6, "/dev/spidev6.3"),
    ],
)
def test_check_range(dev_id, bus_num, result):
    spi = SpiDevice(bus_num, dev_id)
    assert spi.spi.devpath == result
