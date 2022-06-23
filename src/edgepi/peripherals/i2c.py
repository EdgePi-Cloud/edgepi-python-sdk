from periphery import I2C

class I2CDevice():
    
    def __init__(self, fd: str = None):
        self.fd = fd
        self.i2cdev = I2C(fd)

    def close(self):
        self.i2cdev.close()