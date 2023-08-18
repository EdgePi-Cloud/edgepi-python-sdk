""" integration tests for peripherals/i2c.py """

from contextlib import nullcontext as does_not_raise
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
    assert i2c_device.i2c_fd == fd


@pytest.mark.parametrize(
    "addrx, data",
    [
        (32, [46]),
        ([32,24], [46]),
        ([64, 2], [2,3,4,5,6,7,8,9,10])
    ]
)
def test_i2c_set_write_msg(addrx, data):
    i2c_device = I2CDevice("/dev/i2c-0")
    with i2c_device.i2c_open():
        msg = i2c_device.set_write_msg(addrx, data)
        if isinstance(addrx, int):
            assert msg[0].data == [addrx]+data
        else:
            assert msg[0].data == addrx+data

def test_file_descriptor_open():
    with does_not_raise():
        i2c_devices = [0]*2048
        for i2cdev in i2c_devices:
            i2cdev = I2CDevice("/dev/i2c-10")
            with i2cdev.i2c_open():
                pass
