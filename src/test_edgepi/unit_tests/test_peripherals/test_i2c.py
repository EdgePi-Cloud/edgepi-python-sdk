""" unit tests for peripherals/i2c.py """

# pylint: disable=C0413
from unittest import mock
from unittest.mock import patch
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
import pytest
from edgepi.peripherals.i2c import I2CDevice

# pylint: disable=E1101
if sys.platform != 'linux':
    @pytest.mark.parametrize("fd, mock_expects",
                            [( '/dev/i2c-10', ['/dev/i2c-10']),
                             ( '/dev/i2c-11', ['/dev/i2c-11']),
                             ( '/dev/i2c-12', ['/dev/i2c-12']),
                             ( '/dev/i2c-13', ['/dev/i2c-13'])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_init_param(i2c_mock, fd, mock_expects):
        i2c_mock.fd = '/dev/i2c-10'
        i2c_mock.fd = mock_expects[0]
        i2c_device = I2CDevice(fd)
        assert i2c_device.fd == fd

    @pytest.mark.parametrize("addrs, msg, result",
                            [( 30, [31, 32], [[30], False, [31, 32], True]),
                             ( 20, [21, 22], [[20], False, [21, 22], True]),
                             ( 10, [11, 12], [[10], False, [11, 12], True]),
                             ( 0, [1, 2], [[0], False, [1, 2], True]),
                             ( [1,2], [3, 4], [[1,2], False, [3, 4], True])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_read_msg(i2c_mock, addrs, msg, result):
        i2c_mock.fd = '/dev/i2c-10'
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
                             ( 0, [1, 2], [[0, 1, 2], False]),
                             ( [3,4], [1, 2], [[3, 4, 1, 2], False])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_write_msg(i2c_mock, addrs, msg, result):
        i2c_mock.fd = '/dev/i2c-10'
        i2c_device = I2CDevice('/dev/i2c-10')
        i2c_device.i2cdev.Message.return_value.data = i2c_device.i2cdev.Message
        list_msg = i2c_device.set_write_msg(addrs, msg)
        i2c_device.i2cdev.Message.assert_called_with(result[0], read=result[1])
        assert len(list_msg) == i2c_device.i2cdev.Message.call_count

else:
    @pytest.mark.parametrize("fd, result",
                            [( '/dev/i2c-10', ['/dev/i2c-10'])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_init_param(i2c_mock,fd, result):
        i2c_mock.fd = '/dev/i2c-10'
        i2c_device = I2CDevice(fd)
        assert i2c_device.fd == result[0]


    @pytest.mark.parametrize("addrs, msg, result",
                            [( 30, [31, 32], [[30], False, [31, 32], True]),
                             ( 20, [21, 22], [[20], False, [21, 22], True]),
                             ( 10, [11, 12], [[10], False, [11, 12], True]),
                             ( 0, [1, 2], [[0], False, [1, 2], True])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_read_msg(i2c_mock, addrs, msg, result):
        i2c_mock.fd = '/dev/i2c-10'
        i2c_device = I2CDevice('/dev/i2c-10')
        i2c_device.i2cdev.Message.return_value.data = i2c_device.i2cdev.Message
        list_msg = i2c_device.set_read_msg(addrs, msg)
        i2c_device.i2cdev.Message.assert_any_call(result[0], read=result[1])
        i2c_device.i2cdev.Message.assert_any_call(result[2], read=result[3])
        assert len(list_msg) == i2c_device.i2cdev.Message.call_count


    # Get Read Message
    # Set Write Message
    @pytest.mark.parametrize("addrs, msg, result",
                            [( 30, [31, 32], [[30, 31, 32], False]),
                             ( 20, [21, 22], [[20, 21, 22], False]),
                             ( 10, [11, 12], [[10, 11, 12], False]),
                             ( 0, [1, 2], [[0, 1, 2], False])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_write_msg(i2c_mock, addrs, msg, result):
        i2c_mock.fd = '/dev/i2c-10'
        i2c_device = I2CDevice('/dev/i2c-10')
        i2c_device.i2cdev.Message.return_value.data = i2c_device.i2cdev.Message
        list_msg = i2c_device.set_write_msg(addrs, msg)
        i2c_device.i2cdev.Message.assert_called_with(result[0], read=result[1])
        assert len(list_msg) == i2c_device.i2cdev.Message.call_count

    #Transfer Read
    @pytest.mark.parametrize("dev_address, msg, result",
                            [( 33, [2,False,[0],True], [255]),
                             ( 32, [3,False,[0],True], [255]),
                             ( 32, [6,False,[0],True], [255]),
                             ( 33, [7,False,[0],True], [255]),
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    @patch('edgepi.peripherals.i2c.I2CDevice.transfer')
    def test_i2c_transfer_read(i2c_transfer_mock, i2c_mock, dev_address, msg, result):
        i2c_mock.fd = '/dev/i2c-10'
        i2c_device = I2CDevice('/dev/i2c-10')
        i2c_transfer_mock.return_value = 255
        list_msg = i2c_device.set_read_msg(msg[0], msg[2])
        list_msg = i2c_device.transfer(dev_address, list_msg)
        assert list_msg == result[0]
