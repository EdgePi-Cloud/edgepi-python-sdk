from periphery import SPI
from gpiozero import LED

# TODO: This class needs to be changed as the SPI library changes
class SpiDevice():
    _devPath = '/dev/spidev'

    def __init__ (self, bus_num:int = None, dev_ID:int = None, mode:int = 1, max_speed:int = 1000000, bit_order:str='msb', bits_per_word:int = 8, extra_flags:int = 0):
        self.spi = SPI(f'/dev/spidev{bus_num}.{dev_ID}',  mode, max_speed, bit_order, bits_per_word, extra_flags)
        self.cs_line = LED(16)
        self.cs_line.on()
        print(self.spi.devpath)
    
    def transfer(self, data:list) -> list:
        self.cs_line.off()
        out = self.spi.transfer(data)
        self.cs_line.on()
        return out

    def close(self):
        self.spi.close()

if __name__ == '__main__':
   spi_dev = SpiDevice(bus_num=6, dev_ID=0)
   spi_dev.transfer([0x01, 0xFF, 0xFF])
