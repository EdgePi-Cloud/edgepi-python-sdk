""" unit tests for peripherals/i2c.py """

# pylint: disable=wrong-import-order
from edgepi.peripherals.i2c import I2CDevice

import pytest
from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()

I2C_DEV_PATH = '/dev/i2c-10'

@pytest.mark.parametrize(
    "fd",
    [
        ("/dev/i2c-10"),
    ],
)
def test_i2c_init(fd):
    i2c_dev = I2CDevice(fd)
    assert i2c_dev.i2c_fd == I2C_DEV_PATH

# pylint: disable=no-member
def test_i2c_open(mocker):
    periph_i2c = mocker.patch("edgepi.peripherals.i2c.I2C")
    i2c_dev = I2CDevice(I2C_DEV_PATH)
    with i2c_dev.i2c_open():
        assert periph_i2c.called_once()
    i2c_dev.i2cdev.close.aasert_called_once()


@pytest.mark.parametrize("addrs, msg, result",
                        [( 30, [31, 32], [[30], False, [31, 32], True]),
                         ( 20, [21, 22], [[20], False, [21, 22], True]),
                         ( 10, [11, 12], [[10], False, [11, 12], True]),
                         ( 0, [1, 2], [[0], False, [1, 2], True]),
                         ( [1,2], [3, 4], [[1,2], False, [3, 4], True])
                        ])
# pylint: disable=no-member
def test_i2c_set_read_msg(mocker, addrs, msg, result):
    mocker.patch("edgepi.peripherals.i2c.I2C")
    i2c_dev = I2CDevice(I2C_DEV_PATH)
    with i2c_dev.i2c_open():
        list_msg = i2c_dev.set_read_msg(addrs, msg)
        i2c_dev.i2cdev.Message.assert_any_call(result[0], read=result[1])
        i2c_dev.i2cdev.Message.assert_any_call(result[2], read=result[3])
        assert len(list_msg) == i2c_dev.i2cdev.Message.call_count
    assert i2c_dev.i2cdev.close.called_once()

@pytest.mark.parametrize("addrs, msg, result",
                        [( 30, [31, 32], [[30, 31, 32], False]),
                         ( 20, [21, 22], [[20, 21, 22], False]),
                         ( 10, [11, 12], [[10, 11, 12], False]),
                         ( 0, [1, 2], [[0, 1, 2], False]),
                         ( [3,4], [1, 2], [[3, 4, 1, 2], False])
                        ])
# pylint: disable=no-member
def test_i2c_set_write_msg(mocker, addrs, msg, result):
    mocker.patch("edgepi.peripherals.i2c.I2C")
    i2c_dev = I2CDevice(I2C_DEV_PATH)
    with i2c_dev.i2c_open():
        list_msg = i2c_dev.set_write_msg(addrs, msg)
        i2c_dev.i2cdev.Message.assert_called_with(result[0], read=result[1])
        assert len(list_msg) == i2c_dev.i2cdev.Message.call_count
    assert i2c_dev.i2cdev.close.called_once()
