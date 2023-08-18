"""integration tests for spi.py module"""

from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.peripherals.spi import SpiDevice


@pytest.mark.parametrize(
    "dev_id, bus_num, result",
    [
        (0, 6, None),
        (1, 6, None),
        (2, 6, None),
        (3, 6, None),
    ],
)
def test_check_spi_none(dev_id, bus_num, result):
    spi = SpiDevice(bus_num, dev_id)
    assert spi.spi is result

@pytest.mark.parametrize(
    "dev_id, bus_num, result",
    [
        (0, 6, "/dev/spidev6.0"),
        (1, 6, "/dev/spidev6.1"),
        (2, 6, "/dev/spidev6.2"),
        (3, 6, "/dev/spidev6.3"),
    ],
)
def test_check_spi(dev_id, bus_num, result):
    spi = SpiDevice(bus_num, dev_id)
    with spi.spi_open():
        assert spi.spi.devpath == result

def test_file_descriptor_open():
    with does_not_raise():
        spidevs_0 = [0]*2048
        spidevs_1 = [0]*2048
        spidevs_2 = [0]*2048
        spidevs_3 = [0]*2048
        for indx, _ in enumerate(spidevs_0):
            spidevs_0[indx] = SpiDevice(6,0)
            spidevs_1[indx] = SpiDevice(6,1)
            spidevs_2[indx] = SpiDevice(6,2)
            spidevs_3[indx] = SpiDevice(6,3)
            with spidevs_0[indx].spi_open():
                pass
            with spidevs_1[indx].spi_open():
                pass
            with spidevs_2[indx].spi_open():
                pass
            with spidevs_3[indx].spi_open():
                pass
