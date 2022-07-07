"""
Module for SPI devices

Classes:
    SpiDevice
"""


from periphery import SPI


# pylint: disable=fixme
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
        self.spi = SPI(
            f"/dev/spidev{bus_num}.{dev_id}",
            mode,
            max_speed,
            bit_order,
            bits_per_word,
            extra_flags,
        )

    def transfer(self, data: list) -> list:
        """Conduct an SPI data transfer"""
        out = self.spi.transfer(data)
        return out

    def close(self):
        """Close SPI connection"""
        self.spi.close()
