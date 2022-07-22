""" integration tests for peripherals/i2c.py """

# pylint: disable=C0413

import pytest
from edgepi.peripherals.i2c import I2CDevice

# pylint: disable=E1101
@pytest.mark.parametrize("fd, mock_expects",
                        [( '/dev/i2c-10', ['/dev/i2c-10']),
                         ( '/dev/i2c-11', ['/dev/i2c-11']),
                         ( '/dev/i2c-12', ['/dev/i2c-12']),
                         ( '/dev/i2c-13', ['/dev/i2c-13'])
                        ])
def test_i2c_init_param(fd, mock_expects):
    i2c_device = I2CDevice(fd)
    assert i2c_device.fd == fd

@pytest.mark.parametrize("addrs, msg, result",
                        [( 30, [31, 32], [[30], False, [31, 32], True]),
                         ( 20, [21, 22], [[20], False, [21, 22], True]),
                         ( 10, [11, 12], [[10], False, [11, 12], True]),
                         ( 0, [1, 2], [[0], False, [1, 2], True])
                        ])
def test_i2c_set_read_msg(addrs, msg, result):
    i2c_dev = I2CDevice('/dev/i2c-10')
    i2c_dev.i2cdev.Message.return_value.data = i2c_dev.i2cdev.Message
    list_msg = i2c_dev.set_read_msg(addrs, msg)
    i2c_dev.i2cdev.Message.assert_any_call(result[0], read=result[1])
    i2c_dev.i2cdev.Message.assert_any_call(result[2], read=result[3])
    assert len(list_msg) == i2c_dev.i2cdev.Message.call_count


# Get Read Message
# Set Write Message
@pytest.mark.parametrize("addrs, msg, result",
                        [( 30, [31, 32], [[30, 31, 32], False]),
                         ( 20, [21, 22], [[20, 21, 22], False]),
                         ( 10, [11, 12], [[10, 11, 12], False]),
                         ( 0, [1, 2], [[0, 1, 2], False])
                        ])
def test_i2c_set_write_msg(addrs, msg, result):
    i2c_device = I2CDevice('/dev/i2c-10')
    i2c_device.i2cdev.Message.return_value.data = i2c_device.i2cdev.Message
    list_msg = i2c_device.set_write_msg(addrs, msg)
    i2c_device.i2cdev.Message.assert_called_with(result[0], read=result[1])
    assert len(list_msg) == i2c_device.i2cdev.Message.call_count
