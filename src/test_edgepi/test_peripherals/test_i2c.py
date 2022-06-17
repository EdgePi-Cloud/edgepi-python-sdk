import pytest
from edgepi.peripherals.i2c import I2CDevice

@pytest.mark.parametrize("fd",
                        [( '/dev/i2c-10'),
                         ( '/dev/i2c-11'),
                         ( '/dev/i2c-12'),
                         ( '/dev/i2c-13')
                        ])
def test_i2c_init_param(fd):
    i2cDevice = I2CDevice(fd)
    assert i2cDevice.fd == fd
    assert i2cDevice.i2cdev.devpath == fd