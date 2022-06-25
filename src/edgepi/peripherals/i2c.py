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
    def setReadMsg(self, addr:int = None, Msg:list = None):
        return [self.i2cdev.Message([addr]), self.i2cdev.Message(Msg, read=True)]
    
    ''' 
        set Write message to be sent through I2C.
        Attributes:
            addr: Register address to write to
            Msg: list of Msg bytes
        Return:
            MsgList: list of I2C.Message() objects containing Msg to be sent
    '''
    def setWriteMsg(self, addr:int = None, Msg:list = None):
        return [self.i2cdev.Message([addr]+Msg)]
        
    def close(self):
        self.i2cdev.close()