from periphery import SPI


# TODO: This class needs to be changed as the SPI library changes
class SpiDevice():
    _devPath = '/dev/spidev'

    def __init__ (self, dev_ID:int = None, bus_num:int = None, mode:int = 1, max_speed:int = 1000000, bit_order:str='msb', bits_per_word:int = 8, extra_flags:int = 0):
        self.devPath = SpiDevice._devPath +str(bus_num) + '.' + str(dev_ID)
        self.spi = SPI(self.devPath,  mode, max_speed, bit_order, bits_per_word, extra_flags)
    
    def transfer (self, data:list) -> list:
        return self.spi.transfer(data)

    def close(self):
        self.spi.close()