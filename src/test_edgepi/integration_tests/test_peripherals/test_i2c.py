""" integration tests for peripherals/i2c.py """


import pytest
from edgepi.peripherals.i2c import I2CDevice


@pytest.mark.parametrize(
    "fd",
    [
        ("/dev/i2c-0"),
        ("/dev/i2c-1"),
        ("/dev/i2c-10"),
        ("/dev/i2c-20"),
        ("/dev/i2c-21"),
        ("/dev/i2c-22"),
    ],
)
def test_i2c_init_param(fd):
    i2c_device = I2CDevice(fd)
    assert i2c_device.fd == fd
