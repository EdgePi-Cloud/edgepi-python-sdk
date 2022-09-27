'''Helper class to access on board eeprom'''

def sequential_read(bus, reg_addr: int = None, length: int = None, dev_addr: int = None):
    '''
    Read operation reads the specified number of memory location starting from provided address. The
    address pointer will wrap around when it reaches the end of the memory.
    Args:
        bus: i2c bus
        reg_addr: starting address to read from
        len: length of data or number of data to read
        dev_addr: device address
    Returns:
        List of read data

    '''
    msg = bus.set_read_msg(reg_addr, [0xFF]*length)
    return bus.transfer(dev_addr, msg)

def selective_read(bus, reg_addr: int = None, dev_addr: int = None):
    '''
    Read operation reads a data from the specified address
    Args:
        bus: i2c bus
        reg_addr: starting address to read from
        dev_addr: device address
    Returns:
        List of read data
    '''
    msg = bus.set_read_msg(reg_addr, [0xFF])
    return bus.transfer(dev_addr, msg)

def byte_write_register(bus, reg_addr: int = None, data: int = None, dev_addr: int = None):
    '''
    Write operation writes a data to the specified address
    Args:
        bus: i2c bus
        reg_addr: starting address to read from
        data: data to write to the location
        dev_addr: device address
    Returns:
        N/A
    '''
    msg = bus.set_write_msg(reg_addr, [data])
    bus.transfer(dev_addr, msg)

def page_write_register(bus, reg_addr: int = None, data: int = None, dev_addr: int = None):
    '''
    Write operation writes a page of data to the specified address
    Args:
        bus: i2c bus
        reg_addr: starting address to read from
        data: data to write to the location
        dev_addr: device address
    Returns:
        N/A
    '''
    msg = [bus.Message([reg_addr, data])]
    bus.transfer(dev_addr, msg)
