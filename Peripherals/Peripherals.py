from periphery import*

# TODO: add more edgepi specific functions as needed
class SpiDevice(SPI):
    def __init__ (self, dev_path:str = None, mode:int = 1, max_speed:int = 1000000, bit_order:str='msb', bits_per_word:int = 8, extra_flags:int = 0):
        super().__init__(dev_path, mode, max_speed, bit_order, bits_per_word, extra_flags)



#TODO: Add other peripherals, I2C, GPIO, etc