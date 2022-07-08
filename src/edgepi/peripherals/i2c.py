"""
Module for I2C devices

Classes:
    I2CDevice
"""


from periphery import I2C


class I2CDevice:
    """Class representing an I2C device"""

    def __init__(self, fd: str = None):
        self.fd = fd
        self.i2cdev = I2C(fd)

    def set_read_msg(self, addr: int = None, msg: list = None):
        """
        set Read message to be sent through I2C.
        Attributes:
            addr: Register address to read from
            Msg: list of place holder bytes
        Return:
            MsgList: list of I2C.Message() objects containing Msg to be sent
        """
        return [I2C.Message([addr]), I2C.Message(msg, read=True)]

    def set_write_msg(self, addr: int = None, msg: list = None):
        """
        set Write message to be sent through I2C.
        Attributes:
            addr: Register address to write to
            Msg: list of Msg bytes
        Return:
            MsgList: list of I2C.Message() objects containing Msg to be sent
        """
        return [I2C.Message([addr] + msg)]

    def close(self):
        """
        Close I2C connection
        """
        self.i2cdev.close()
