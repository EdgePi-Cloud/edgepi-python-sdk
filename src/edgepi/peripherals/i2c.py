from periphery import I2C

class I2CDevice():
    
    def __init__(self, fd: str = None):
        self.fd = fd
        self.i2cdev = I2C(fd)

    ''' 
        set Read message to be sent through I2C.
        Attributes:
            addr: Register address to read from
            Msg: list of place holder bytes
        Return:
            MsgList: list of I2C.Message() objects containing Msg to be sent
    '''
    def set_read_msg(self, addr:int = None, Msg:list = None):
        return [self.i2cdev.Message([addr], read = False), self.i2cdev.Message(Msg, read = True)]
    ''' 
        set Write message to be sent through I2C.
        Attributes:
            addr: Register address to write to
            Msg: list of Msg bytes
        Return:
            MsgList: list of I2C.Message() objects containing Msg to be sent
    '''
    def set_write_msg(self, addr:int = None, Msg:list = None):
        msgList = [self.i2cdev.Message([addr]+Msg, read = False)]
        return msgList
    
    ''' 
        Message Transfer
        Attributes:
            dev_addr: hardware device address
            Msg: list of Message class objects
        Return:
            MsgList: list of message bytes if reading flag was set
    '''
    def transfer(self, dev_addr: int = None, Msg:list = None):
        self.i2cdev.transfer(dev_addr, Msg)

    def close(self):
        self.i2cdev.close()