'''Helper class to access on board eeprom'''

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

import logging
import math

from edgepi.calibration.eeprom_constants import (
    EEPROMInfo,
    EdgePiMemoryInfo,
    MessageFieldNumber
    )
from edgepi.calibration.protobuf_mapping import EdgePiEEPROMData
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout
from edgepi.peripherals.i2c import I2CDevice

class MemoryOutOfBound(Exception):
    """Raised memory out-of-bound error"""

class EdgePiEEPROM(I2CDevice):
    '''
    Helper class to read eeprom using I2C
    '''
    __dev_path = '/dev/i2c-10'

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing EEPROM Access")
        self.eeprom_layout = EepromLayout()
        super().__init__(self.__dev_path)

    def __pack_mem_address(self, page_addr: int = None, byte_addr: int = None):
        """
        Pack page address and byte address to generate address message. The address message will
        let the EEPROM memory address point to know at which address the read/write operation to
        take in place
        Args:
            page_addr (int): page address (0~511)
            byte_addr (int): byte address in the page(0~63)
        return:
            (list): 2-byte address message
        """
        address = page_addr<<6 | byte_addr
        return [(address>>8)&0xFF, address&0xFF]

    def __byte_address_generation(self, memory_address: int = None):
        """
        Generates page address and bytes address from the memory address provided.
        Args:
            memory_address (int): memory address to start read/write operation. This is in bytes
            from 0 - 32768
        """
        page_addr  = math.floor(memory_address/EEPROMInfo.PAGE_SIZE.value)
        byte_addr = memory_address%EEPROMInfo.PAGE_SIZE.value
        self.log.debug(f'Page address = {page_addr}, byte Address = {byte_addr}')
        return page_addr, byte_addr

    def __allocated_memory(self):
        '''
        The first two bytes represenst the allocated memory in Edgepi reserved memory space. This
        function returns the length of memory to read.
        Args:
            N/A
        Return:
            length (int): size of memory to read
        '''
        length = self.__sequential_read(EdgePiMemoryInfo.USED_SPACE.value, 2)
        return (length[0]<<8)| length[1]

    def __read_edgepi_reserved_memory(self):
        '''
        Read Edgepi reserved memory space to retreive parameters. This function will return byte
        strings, that can be converted into protocol buffer message format
        Args:
            N/A
        Return:
            Byte_string (bytes): strings of bytes read from the eeprom
        '''
        mem_size = self.__allocated_memory()
        buff_list = self.__sequential_read(EdgePiMemoryInfo.BUFF_START.value, mem_size)
        return bytes(buff_list)

    def get_message_of_interest(self, msg: MessageFieldNumber = None):
        """
        This function filters out the message according to the specified field number passed as
        parameter.
        Args:
            msg (MessageFieldNumber): protocol buffer message field index number for ListFields()
            function
        Return:
            pb message specified by the message field number. ex) if message field of DAC is passed,
            the dac message will be returned
        """
        self.eeprom_layout.ParseFromString(self.__read_edgepi_reserved_memory())
        return self.eeprom_layout.ListFields()[msg.value - 1][1]

    def get_edgepi_reserved_data(self):
        """
        Read Edgepi reserved memory space and populate dataclass
        Args:
            N/A
        Return:
            eeprom_data (EdgePiEEPROMData): dataclass containing eeprom values
        """
        # pylint: disable=no-member
        self.eeprom_layout.ParseFromString(self.__read_edgepi_reserved_memory())
        eeprom_data = EdgePiEEPROMData(self.eeprom_layout)
        return eeprom_data

    def __sequential_read(self, mem_addr: int = None, length: int = None):
        '''
        Read operation reads the specified number of memory location starting from provided address.
        The address pointer will wrap around when it reaches the end of the memory.
        Args:
            mem_addr: starting memory address to read from
            len: length of data or number of data to read
        Returns:
            List of read data

        '''
        page_addr, byte_addr = self.__byte_address_generation(mem_addr)
        mem_addr_list = self.__pack_mem_address(page_addr, byte_addr)
        msg = self.set_read_msg(mem_addr_list, [0x00]*length)
        self.log.debug(f'Reading Address {mem_addr}, {length} bytes')
        read_result = self.transfer(EEPROMInfo.DEV_ADDR.value, msg)
        self.log.debug(f'Read data: {len(msg[1].data)}')
        return read_result


    def __selective_read(self, mem_addr: int = None):
        '''
        Read operation reads a data from the specified address
        Args:
            mem_addr: starting memory address to read from
        Returns:
            List of read data
        '''
        page_addr, byte_addr = self.__byte_address_generation(mem_addr)
        mem_addr_list = self.__pack_mem_address(page_addr, byte_addr)
        msg = self.set_read_msg(mem_addr, [0x00])
        self.log.debug(f'Reading Address {mem_addr_list}, {msg[1].data}')
        read_result = self.transfer(EEPROMInfo.DEV_ADDR.value, msg)
        self.log.debug(f'Read data: {msg[1].data}')
        return read_result

    def __byte_write_register(self, mem_addr: int = None, data: int = None):
        '''
        Write operation writes a data to the specified address
        Args:
            mem_addr: starting memory address to read from
            data: data to write to the location
        Returns:
            N/A
        '''
        page_addr, byte_addr = self.__byte_address_generation(mem_addr)
        mem_addr_list = self.__pack_mem_address(page_addr, byte_addr)
        msg = self.set_write_msg(mem_addr_list, [data])
        self.log.debug(f'Writing {data} to memory address of {mem_addr}, {msg[0].data}')
        self.transfer(EEPROMInfo.DEV_ADDR.value, msg)

    def __page_write_register(self, mem_addr: int = None, data: list = None):
        '''
        Write operation writes a page of data to the specified address
        Args:
            mem_addr: starting memory address to read from
            data: data to write to the location
        Returns:
            N/A
        '''
        page_addr, byte_addr = self.__byte_address_generation(mem_addr)
        mem_addr_list = self.__pack_mem_address(page_addr, byte_addr)
        msg = self.set_write_msg(mem_addr_list, data)
        self.log.debug(f'Writing {data} to memory address of {mem_addr}, {msg[0].data}')
        self.transfer(EEPROMInfo.DEV_ADDR.value, msg)
    
    def __parameter_sanity_chekc(self, mem_addr: int = None,
                                 length: int = None,
                                 user_space: bool = True):
        """
        Generic check function for target memory address and length of data to read/write
        Args:
            mem_addr (int): starting memory address to read from
            length (int): length of data to read
            user_space (bool): True if mem_addr is in user space
        """
        # End address depending on the user_space flag
        end_address = EdgePiMemoryInfo.USER_SPACE_END_BYTE.value if user_space \
                      else (EdgePiMemoryInfo.USER_SPACE_START_BYTE.value - 1)
        # Checks whether proper values are passed
        if mem_addr is None or length is None or mem_addr < 0 or length <= 0:
            raise ValueError(f'Invalid Value passed: {mem_addr}, {length}')
        # Checks whether starting address and length of data to read/write are within memory bound
        if mem_addr+length > end_address:
            raise MemoryOutOfBound(f'Operation range is over the size of the memory')

    def __generate_list_of_pages(self, mem_addr: int = None, data: list = None):
        """
        Generate a two dimensional structured list with length of a page. This is method is used for
        read/write by page
        Args:
            mem_addr (int): starting memory address to read from
            data (list): data to write
        Return:
            page_writable_list (list): [[Page_N], [Page_N+1]...]]
        """
        # starting memory address can be anywhere from 0~63, check whether the length of data fits
        # within the range.
        if (mem_addr%EEPROMInfo.PAGE_SIZE.value + len(data)) < EEPROMInfo.PAGE_SIZE.value:
            page_n = [data]
        else:
            curr_page_remainder = EEPROMInfo.PAGE_SIZE.value - mem_addr%EEPROMInfo.PAGE_SIZE.value
            page_1 = [data[val] for val in range(curr_page_remainder)]
            data_remainder = data[curr_page_remainder:]
            page_n = [data_remainder[byte:byte+EEPROMInfo.PAGE_SIZE.value] \
                      for byte in range(0,len(data_remainder), EEPROMInfo.PAGE_SIZE.value)]
            page_n.insert(0, page_1)
        return page_n

# TODO: nomenclautre for mem_address for different functions
    def read_memory(self, mem_addr: int = None, length: int = None):
        """
        Read user space memory starting from 0 to 16383
        Args:
            mem_addr (int): starting memory address to read from
            length (int): length of data to read
        Return:
            data (list): list of data read from the specified memory and length
        """
        self.__parameter_sanity_chekc(mem_addr, length, True)
        start_adress = mem_addr + EdgePiMemoryInfo.USER_SPACE_START_BYTE.value
        data = self.__sequential_read(start_adress, length)
        return data

    def write_memory(self, mem_addr: int = None, data: bytes = None):
        """
        Address to write to
        Args:
            mem_addr (int): starting memory address to write to
            data (bytes): serialized data to be stoed in the EEPROM
        Return:
            N/A
        """
        if mem_addr is None or data is None:
            raise ValueError(f'Invalid Value passed: {mem_addr}, {data}')
        self.__parameter_sanity_chekc(mem_addr, len(data))
        start_adress = mem_addr + EdgePiMemoryInfo.USER_SPACE_START_BYTE.value
        self.__generate_list_of_pages(start_adress, list(data))

