'''Helper class to access on board eeprom'''

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

import logging
import math
import json
import time

from edgepi.utilities.crc_8_atm import (
    CRC_BYTE_SIZE,
    get_crc
)
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
        self.data_list = []
        self.used_size = 0
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
        self.log.debug(f"__byte_address_generation: Page address = {page_addr},"
                       f"byte Address = {byte_addr}")
        return page_addr, byte_addr

    def __allocated_memory(self, offset):
        '''
        The first two bytes represenst the allocated memory in Edgepi reserved memory space. This
        function returns the length of memory to read.
        Args:
            offset: memory offset,
                    - reserved offset = EdgePiMemoryInfo.USED_SPACE.value
                    - userspace offset = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value
        Return:
            length (int): size of memory to read
        '''
        length = self.__sequential_read(offset, 2)
        return (length[0]<<8)| length[1]

    def __generate_data_list(self, data_b: bytes):
        """
        Transform data bytes to list with 255 filling the remainder of the last page. The remainder
        is calculated with the page size of PAGE_SIZE-CRC_BYTE_SIZE because we want to insert CRC
        byte at the end of each page later
        Args:
            data_b (bytes): data in bytes format
        Return:
            data_l (list): data in list type if following format
            [len(data)1, len(data)2, data .... data, 255, 255, ...255]
        """
        data_l = list(data_b)
        data_l = [(len(data_l)>>8)&0xFF, len(data_l)&0xFF] + data_l
        # calculate the remainder of last page
        page_size = EEPROMInfo.PAGE_SIZE.value-CRC_BYTE_SIZE
        remainder = page_size - len(data_l)%(page_size)
        # list of data with 255 appended in the last page
        data_l = data_l+[255]*remainder
        return data_l
        


    def __write_edgepi_reserved_memory(self, pb_serial_list: bytes):
        """
        Write Edgepi reserved memory space.
        Args:
            pb_serial_list (list): serialized data converted into list
        Return:
            N/A
        """
        # calculated the used memsize
        data = self.__generate_data_list(pb_serial_list)


        self.__parameter_sanity_check(mem_start, len(data_serialized), True)
        self.log.debug(f"write_memory: length of data {data_serialized}\n{used_mem}")

        # time sleep of 0.002 sec need for consecutive i2c writes/read
        self.__byte_write_register(EdgePiMemoryInfo.USER_SPACE_START_BYTE.value, used_mem[0])
        time.sleep(0.002)
        self.__byte_write_register(EdgePiMemoryInfo.USER_SPACE_START_BYTE.value+1, used_mem[1])
        time.sleep(0.002)

        pages_list = self.__generate_list_of_pages(mem_start, list(data_serialized))
        mem_offset = mem_start
        for page in pages_list:
            self.__page_write_register(mem_offset, page)
            mem_offset = mem_offset+len(page)
            time.sleep(0.002)

    def __read_edgepi_reserved_memory(self):
        '''
        Read Edgepi reserved memory space to retreive parameters. This function will return byte
        strings, that can be converted into protocol buffer message format
        Args:
            N/A
        Return:
            Byte_string (bytes): strings of bytes read from the eeprom
        '''
        mem_size = self.__allocated_memory(EdgePiMemoryInfo.USED_SPACE.value)
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
        self.log.debug(f'__sequential_read: Reading Address {mem_addr}, {length} bytes')
        read_result = self.transfer(EEPROMInfo.DEV_ADDR.value, msg)
        self.log.debug(f'__sequential_read: Read data: {len(msg[1].data)}')
        return read_result

    # TODO: delete candidate when module implementation is complete
    # pylint: disable=unused-private-member
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

    # pylint: disable=unused-private-member
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
        self.log.debug(f"__byte_write_register: writing {data} to memory address of {mem_addr},"
                       f"{msg[0].data}")
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
        self.log.debug(f"__page_write_register: writing {data} to memory address of {mem_addr},"
                       f"{len(msg[0].data)}")
        self.transfer(EEPROMInfo.DEV_ADDR.value, msg)

    def __parameter_sanity_check(self, mem_addr: int = None,
                                 length: int = None,
                                 user_space: bool = True):
        """
        Generic check function for target memory address and length of data to read/write
        Args:
            mem_addr (int): starting memory address to read from
            length (int): length of data to read
            user_space (bool): True if mem_addr is in user space
        """
        #select last address of a memory space
        last_mem_address = EdgePiMemoryInfo.USER_SPACE_END_BYTE.value if user_space \
                           else EdgePiMemoryInfo.PRIVATE_SPACE_END_BYTE.value

        # Checks whether proper values are passed
        if mem_addr is None or length is None or mem_addr < 0 or length <= 0:
            raise ValueError(f'Invalid Value passed: {mem_addr}, {length}')
        # Checks whether starting address and length of data to read/write are within memory bound
        if mem_addr+length > (last_mem_address + 1):
            raise MemoryOutOfBound(f"Operation range is over the size of the memory by "
                                   f"{mem_addr+length-last_mem_address}")
    
    # TODO: to be deleted afte crc implementation
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
            self.log.debug(f"__generate_list_of_pages: {len(page_n)} pages generated")
        return page_n

    def __generate_list_of_pages_crc(self, data: list = None):
        """
        Generate a two dimensional structured list with length of a page. This is method is used for
        read/write by page
        Args:
            mem_addr (int): starting memory address to read from
            data (list): list of data already prepared to insert crc at 64th element
        Return:
            page_writable_list (list): [[Page_N], [Page_N+1]...]]
        """
        pages = []
        # data is always populates full page, each page = 63 data bytes + crc byte
        page_size = EEPROMInfo.PAGE_SIZE.value-CRC_BYTE_SIZE
        number_of_pages = int(len(data)/page_size)
        # generate list of pages with size of page_size
        for page in range(number_of_pages):
            page_start = page*page_size
            page_end = page_start+page_size
            pages.append(data[page_start:page_end])

        # insert the crc at the end of each page
        for indx, page in enumerate(pages):
            pages[indx] = get_crc(page)

        self.log.debug(f"__generate_list_of_pages: {number_of_pages} pages generated")
        return pages

    def read_memory(self, start_addrx: int = 0, length: int = None):
        """
        Read user space memory starting from 0 to 16383
        Args:
            mem_addr (int): starting memory address to read from
            length (int): length of data to read
        Return:
            data (list): list of data read from the specified memory and length
        """
        start_addrx = start_addrx + EdgePiMemoryInfo.USER_SPACE_START_BYTE.value
        self.__parameter_sanity_check(start_addrx, length, True)
        dummy_data = self.__generate_list_of_pages(start_addrx, [0]*length)
        data_read = []
        mem_offset = start_addrx
        for data in dummy_data:
            data_read = data_read + self.__sequential_read(mem_offset, len(data))
            mem_offset = mem_offset+len(data)
        return data_read

    def write_memory(self, data: bytes):
        """
        Writes data to the eeprom
        Args:
            data (bytes): serialized json data
        Return:
            N/A
        """
        data_serialized = list(data)
        used_mem = [(len(data_serialized)>>8)&0xFF, len(data_serialized)&0xFF]

        mem_start = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value +\
                    EdgePiMemoryInfo.BUFF_START.value

        self.__parameter_sanity_check(mem_start, len(data_serialized), True)
        self.log.debug(f"write_memory: length of data {data_serialized}\n{used_mem}")

        # time sleep of 0.002 sec need for consecutive i2c writes/read
        self.__byte_write_register(EdgePiMemoryInfo.USER_SPACE_START_BYTE.value, used_mem[0])
        time.sleep(0.002)
        self.__byte_write_register(EdgePiMemoryInfo.USER_SPACE_START_BYTE.value+1, used_mem[1])
        time.sleep(0.002)

        pages_list = self.__generate_list_of_pages(mem_start, list(data_serialized))
        mem_offset = mem_start
        for page in pages_list:
            self.__page_write_register(mem_offset, page)
            mem_offset = mem_offset+len(page)
            time.sleep(0.002)

# TODO why not separate it into a class
    def init_memory(self):
        """
        Initial Memory Reading
        Args:
            N/A
        Return:
            data_struct = list of data_struct
        """
        is_full=False
        is_empty=False
        mem_content = []
        # TODO adding CRC bytes, and better naming for mem_size ex) data_size or used_memory,
        mem_size = self.__allocated_memory(EdgePiMemoryInfo.USER_SPACE_START_BYTE.value)

        # mem_size of greater than EdgePiMemoryInfo.USER_SPACE_MAX.value should never happen
        if mem_size > EdgePiMemoryInfo.USER_SPACE_MAX.value and \
           mem_size != EdgePiMemoryInfo.FACTORY_DEFAULT_VALUE.value:
            raise ValueError(f'Invalid memory size read, possible data corruption, {mem_size}')

        # Memory Empty
        if mem_size == EdgePiMemoryInfo.FACTORY_DEFAULT_VALUE.value:
            is_full=False
            is_empty=True
            self.used_size = 0
            self.log.info('User Space Memory is empty')
        # Memory Full
        elif mem_size == EdgePiMemoryInfo.USER_SPACE_MAX.value:
            is_full=True
            is_empty = False
            self.log.warning('User Space Memory is full')
            mem_start = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + \
                        EdgePiMemoryInfo.BUFF_START.value
            mem_content = bytes(self.read_memory(mem_start, mem_size))
            self.data_list = json.loads(mem_content)
            self.used_size = mem_size
        # part of memory occupied
        else:
            is_full=False
            is_empty=False
            mem_start = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + \
                        EdgePiMemoryInfo.BUFF_START.value
            # read memory content should be in json encoded bytes converted into list
            mem_content = bytes(self.read_memory(mem_start, mem_size))
            self.data_list = json.loads(mem_content)
            self.used_size = mem_size
            self.log.info(f'{mem_size}bytes of data is read from the user space')

        return is_full, is_empty

    def eeprom_reset(self):
        """
        Reset User space memory
        Args:
            N/A
        Return:
            N/A
        """
        self.log.info("EEPROM Reset: User Space Memory Reset")

        start_address_page = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value
        page_size = EEPROMInfo.PAGE_SIZE.value
        tatal_page = EdgePiMemoryInfo.USER_SPACE_END_PAGE.value - \
                     EdgePiMemoryInfo.USER_SPACE_START_PAGE.value + 1
        reset_vals = [255] * page_size

        mem_offset = start_address_page
        for _ in range(tatal_page):
            self.__page_write_register(mem_offset, reset_vals)
            mem_offset = mem_offset+page_size
            time.sleep(0.002)
       