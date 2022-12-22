"""
Module for I2C devices

Classes:
    I2CDevice
"""
import logging

from typing import Union
from periphery import I2C

_logger = logging.getLogger(__name__)

class I2CDevice():
    '''
    I2C Device class
    '''
    def __init__(self, fd: str = None):
        self.fd = fd
        _logger.debug(f"Initialized I2C device with path '{self.fd}'")
        self.i2cdev = I2C(devpath=fd)

    def set_read_msg(self, addr:Union[int,list] = None, msg:list = None):
        '''
        set Read message to be sent through I2C.
        Attributes:
            addr(int or list): Register address to read from
            Msg: list of place holder bytes
        Return:
            MsgList: list of I2C.Message() objects containing msg to be sent
        '''
        list_msg = [self.i2cdev.Message([addr], read = False),
                    self.i2cdev.Message(msg, read = True)] \
                   if isinstance(addr, int) else \
                   [self.i2cdev.Message(addr, read = False),
                    self.i2cdev.Message(msg, read = True)]
        return list_msg

    def set_write_msg(self, addr:Union[int,list] = None, msg:list = None):
        '''
        set Write message to be sent through I2C.
        Attributes:
            addr(int or list): Register address to write to
            Msg: list of Msg bytes
        Return:
            MsgList: list of I2C.Message() objects containing msg to be sent
        '''
        list_msg = [self.i2cdev.Message([addr]+msg, read = False)] if isinstance(addr, int) else \
                   [self.i2cdev.Message(addr+msg, read = False)]
        return list_msg

    def transfer(self, dev_addr: int = None, msg:list = None):
        '''
        Message Transfer
        Attributes:
            dev_addr: hardware device address
            Msg: list of Message class objects
        Return:
            MsgList: list of message bytes if reading flag was set
        '''
        self.i2cdev.transfer(dev_addr, msg)
        if len(msg)>1:
            return msg[1].data
        return None

    def close(self):
        '''
        Close I2C device
        '''
        self.i2cdev.close()
