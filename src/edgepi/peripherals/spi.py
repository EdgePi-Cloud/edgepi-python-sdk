"""
Module for SPI devices

Classes:
    SpiDevice
"""


import logging

from periphery import SPI


_logger = logging.getLogger(__name__)

# TODO: This class needs to be changed as the SPI library changes
class SpiDevice:
    """Class representing an I2C device"""

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
        _logger.debug(f"Initialized SPI device with path '{self.devpath}'")
        self.spi = SPI(
            self.devpath,
            mode,
            max_speed,
            bit_order,
            bits_per_word,
            extra_flags,
        )

    def transfer(self, data: list) -> list:
        """Conduct an SPI data transfer"""
        _logger.debug(f"Before SPI transfer: data={data}")
        out = self.spi.transfer(data)
        _logger.debug(f"After SPI transfer: data={out}")
        return out

    def close(self):
        """Close SPI connection"""
        self.spi.close()
