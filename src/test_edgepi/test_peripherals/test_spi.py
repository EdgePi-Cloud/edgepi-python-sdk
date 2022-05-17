import pytest
from edgepi.peripherals.spi import SpiDevice

@pytest.mark.parametrize("dev_ID, bus_num, result",[(0, 6, '/dev/spidev0.6'), 
                                                    (1, 6, '/dev/spidev1.6'), 
                                                    (2, 6, '/dev/spidev2.6'), 
                                                    (3, 6, '/dev/spidev3.6')])
def test_check_range(dev_ID, bus_num, result):
    spi = SpiDevice(dev_ID, bus_num)
    assert spi.devPath == result