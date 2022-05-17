import pytest
from edgepi.peripherals.spi import SpiDevice

@pytest.mark.parametrize("dev_ID, bus_num, result",[(0, 6, '/dev/spidev6.0'), 
                                                    (1, 6, '/dev/spidev6.1'), 
                                                    (2, 6, '/dev/spidev6.2'), 
                                                    (3, 6, '/dev/spidev6.3')])
def test_check_range(dev_ID, bus_num, result):
    spi = SpiDevice(bus_num, dev_ID)
    assert spi.spi.devpath == result