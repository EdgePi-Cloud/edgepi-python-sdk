"""
Module for SPI devices

Classes:
    SpiDevice
"""
#pylint:disable=too-many-instance-attributes
import logging
import threading
from contextlib import contextmanager
from periphery import SPI


_logger = logging.getLogger(__name__)

class SpiDevice:
    """Class representing an I2C device"""
    lock_spi = {
        0:threading.Lock(),
        1:threading.Lock(),
        2:threading.Lock(),
        3:threading.Lock()
    }
    _devPath = "/dev/spidev"
    def __init__(
        self,
        bus_num: int = None,
        dev_id: int = None,
        mode: int = 1,
        max_speed: int = 1000000,
        bit_order: str = "msb",
        bits_per_word: int = 8,
        extra_flags: int = 0,
    ):
        self.devpath = f"/dev/spidev{bus_num}.{dev_id}"
        self.dev_id = dev_id
        self.mode = mode
        self.max_speed = max_speed
        self.bit_order = bit_order
        self.bits_per_word = bits_per_word
        self.extra_flags = extra_flags
        self.spi = None

    @contextmanager
    def spi_open(self):
        """
        Open SPI device file
        """
        try:
            SpiDevice.lock_spi[self.dev_id].acquire()
            self.spi = SPI(
                self.devpath,
                self.mode,
                self.max_speed,
                self.bit_order,
                self.bits_per_word,
                self.extra_flags,
            )
            _logger.debug(f"Open SPI device with path '{self.devpath}'")
            yield self.spi
        finally:
            try:
                self.spi.close()
            except Exception as exc:
                raise OSError(f"Failed to close {self.devpath}") from exc
            finally:
                SpiDevice.lock_spi[self.dev_id].release()

    def transfer(self, data: list) -> list:
        """Conduct an SPI data transfer"""
        out = self.spi.transfer(data)
        return out
