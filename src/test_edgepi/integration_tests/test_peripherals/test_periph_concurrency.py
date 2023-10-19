""" Integration test for peripheral concurrency """

import threading
import logging
import pytest

from edgepi.peripherals.i2c import I2CDevice
from edgepi.peripherals.spi import SpiDevice
from edgepi.peripherals.gpio import GpioDevice

_logger = logging.getLogger(__name__)

class PropagatingThread(threading.Thread):
    """Propagating thread to raise exceptions in calling function"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exc = None

    def run(self):
        self.exc = None
        try:
            super().run()
        # pylint:disable=broad-exception-caught
        except Exception as err:
            self.exc = err

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        if self.exc:
            raise self.exc

@pytest.fixture(name="i2c_dev", scope="module")
def fixture_i2c():
    i2c_dev = I2CDevice("/dev/i2c-10")
    yield i2c_dev

@pytest.fixture(name="spi_dev", scope="module")
def fixture_spi():
    spi_dev = SpiDevice(bus_num=6, dev_id=1)
    yield spi_dev

@pytest.fixture(name="gpio_dev", scope="module")
def fixture_gpio():
    gpio_dev = GpioDevice("/dev/gpiochip0")
    yield gpio_dev

def i2c_open_with(i2c):
    "i2c open call"
    with i2c.i2c_open():
        pass

def spi_open_with(spi):
    "spi open call"
    with spi.spi_open():
        pass

def gpio_open_with(gpio):
    "gpio open call"
    with gpio.open_gpio(11,"in","pull_down"):
        pass

#pylint:disable=unused-argument
@pytest.mark.parametrize("iteration", range(10))
def test_i2c_concurrency_shared(iteration, i2c_dev):
    """Test for I2C concurrency bug"""
    threads = [PropagatingThread(target=i2c_open_with(i2c_dev)) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

@pytest.mark.parametrize("iteration", range(10))
def test_spi_concurrency_shared(iteration, spi_dev):
    """Test for SPI concurrency bug"""
    threads = [PropagatingThread(target=spi_open_with(spi_dev)) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

@pytest.mark.parametrize("iteration", range(10))
def test_gpio_concurrency_shared(iteration, gpio_dev):
    """Test for GPIO concurrency bug"""
    threads = [PropagatingThread(target=gpio_open_with(gpio_dev)) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def i2c_open_with_indiv():
    "i2c open call"
    i2c_dev = I2CDevice("/dev/i2c-10")
    with i2c_dev.i2c_open():
        pass

def spi_open_with_indiv():
    "spi open call"
    spi_dev = SpiDevice(bus_num=6, dev_id=1)
    with spi_dev.spi_open():
        pass

def gpio_open_with_indiv():
    "gpio open call"
    gpio_dev = GpioDevice("/dev/gpiochip0")
    with gpio_dev.open_gpio(11,"in","pull_down"):
        pass
#pylint:disable=unused-argument
@pytest.mark.parametrize("iteration", range(10))
def test_i2c_concurrency_indiv(iteration):
    """Test for I2C concurrency bug"""
    threads = [PropagatingThread(target=i2c_open_with_indiv()) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

@pytest.mark.parametrize("iteration", range(10))
def test_spi_concurrency_indiv(iteration):
    """Test for SPI concurrency bug"""
    threads = [PropagatingThread(target=spi_open_with_indiv()) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

@pytest.mark.parametrize("iteration", range(10))
def test_gpio_concurrency_indiv(iteration):
    """Test for GPIO concurrency bug"""
    threads = [PropagatingThread(target=gpio_open_with_indiv()) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
