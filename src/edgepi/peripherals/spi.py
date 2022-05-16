from periphery import SPI


# TODO: This class needs to be changed as the SPI library changes
class SpiDevice():
    _devIDtoPath ={
            0:'/dev/spidev6.0',
            1:'/dev/spidev6.1',
            2:'/dev/spidev6.2',
            3:'/dev/spidev6.3'
            }
    def __init__ (self, devID:int = None, mode:int = 1, max_speed:int = 1000000, bit_order:str='msb', bits_per_word:int = 8, extra_flags:int = 0):
        self.spi = SPI(SpiDevice._devIDtoPath[devID], mode, max_speed, bit_order, bits_per_word, extra_flags)
    
    def transfer (self, data:list) -> list:
        return self.spi.transfer(data)