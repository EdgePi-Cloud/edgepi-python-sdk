'''Helper class to access on board eeprom'''
from edgepi.calibration.eeprom_constants import EEPROMAddress
from edgepi.peripherals.i2c import I2CDevice

class EdgePiEEPROM(I2CDevice):
    '''
    Helper class to read eeprom using I2C
    '''
    __dev_path = 'add/i2c/dev/path'

    def __init__(self):
        super().__init__(self.__dev_path)


    def sequential_read(self, mem_addr: int = None, length: int = None):
        '''
        Read operation reads the specified number of memory location starting from provided address.
        The address pointer will wrap around when it reaches the end of the memory.
        Args:
            mem_addr: starting memory address to read from
            len: length of data or number of data to read
        Returns:
            List of read data

        '''
        msg = self.set_read_msg(mem_addr, [0xFF]*length)
        return self.transfer(EEPROMAddress.DEV_ADDR.value, msg)

    def selective_read(self, mem_addr: int = None):
        '''
        Read operation reads a data from the specified address
        Args:
            mem_addr: starting memory address to read from
        Returns:
            List of read data
        '''
        msg = self.set_read_msg(mem_addr, [0xFF])
        return self.transfer(EEPROMAddress.DEV_ADDR.value, msg)

    def byte_write_register(self, mem_addr: int = None, data: int = None):
        '''
        Write operation writes a data to the specified address
        Args:
            mem_addr: starting memory address to read from
            data: data to write to the location
        Returns:
            N/A
        '''
        msg = self.set_write_msg(mem_addr, [data])
        self.transfer(EEPROMAddress.DEV_ADDR.value, msg)

    def page_write_register(self, mem_addr: int = None, data: int = None):
        '''
        Write operation writes a page of data to the specified address
        Args:
            mem_addr: starting memory address to read from
            data: data to write to the location
        Returns:
            N/A
        '''
        msg = self.set_write_msg(mem_addr, data)
        self.transfer(EEPROMAddress.DEV_ADDR.value, msg)
