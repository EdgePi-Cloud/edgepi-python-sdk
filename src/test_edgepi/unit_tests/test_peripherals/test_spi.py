"""unit tests for spi.py module"""

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
def test_check_range(mocker, dev_id, bus_num, result):
    mocker.patch("edgepi.peripherals.spi.SPI")
    spidev = SpiDevice(bus_num, dev_id)
    assert spidev.devpath == result
    assert spidev.bit_order == "msb"
    assert spidev.bits_per_word == 8
    assert spidev.spi is None
    assert spidev.max_speed == 1000000
    assert spidev.mode == 1

# pylint: disable=no-member
def test_spi_open(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    spidev = SpiDevice(0, 6)
    with spidev.spi_open():
        spidev.transfer([0,1,0])
    spidev.spi.transfer.aasert_called_once()
    spidev.spi.close.aasert_called_once()
