""" unit tests for peripherals/i2c.py """


from unittest import mock
from unittest.mock import patch
import pytest
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from edgepi.peripherals.i2c import I2CDevice

if sys.platform != 'linux':
    @pytest.mark.parametrize("fd, mock_expects",
                            [( '/dev/i2c-10', ['/dev/i2c-10']),
                             ( '/dev/i2c-11', ['/dev/i2c-11']),
                             ( '/dev/i2c-12', ['/dev/i2c-12']),
                             ( '/dev/i2c-13', ['/dev/i2c-13'])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_init_param(I2C_mock, fd, mock_expects):
        I2C_mock.fd = mock_expects[0]
        i2cDevice = I2CDevice(fd)
        assert i2cDevice.fd == fd

    @pytest.mark.parametrize("addrs, Msg, result",
                            [( 30, [31, 32], [[30], False, [31, 32], True]),
                             ( 20, [21, 22], [[20], False, [21, 22], True]),
                             ( 10, [11, 12], [[10], False, [11, 12], True]),
                             ( 0, [1, 2], [[0], False, [1, 2], True])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_read_msg(i2c_mock, addrs, Msg, result):
        i2cDev = I2CDevice('/dev/i2c-10')
        i2cDev.i2cdev.Message.return_value.data = i2cDev.i2cdev.Message
        MsgList = i2cDev.set_read_msg(addrs, Msg)
        i2cDev.i2cdev.Message.assert_any_call(result[0], read=result[1])
        i2cDev.i2cdev.Message.assert_any_call(result[2], read=result[3])
        assert len(MsgList) == i2cDev.i2cdev.Message.call_count


    # Get Read Message
    # Set Write Message
    @pytest.mark.parametrize("addrs, Msg, result",
                            [( 30, [31, 32], [[30, 31, 32], False]),
                             ( 20, [21, 22], [[20, 21, 22], False]),
                             ( 10, [11, 12], [[10, 11, 12], False]),
                             ( 0, [1, 2], [[0, 1, 2], False])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_write_msg(i2c_mock, addrs, Msg, result):
        i2cDevice = I2CDevice('/dev/i2c-10')
        i2cDevice.i2cdev.Message.return_value.data = i2cDevice.i2cdev.Message
        MsgList = i2cDevice.set_write_msg(addrs, Msg)
        i2cDevice.i2cdev.Message.assert_called_with(result[0], read=result[1])
        assert len(MsgList) == i2cDevice.i2cdev.Message.call_count
    
else:
    @pytest.mark.parametrize("fd, result",
                            [( '/dev/i2c-10', ['/dev/i2c-10'])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_init_param(i2c_mock,fd, result):
        i2cDevice = I2CDevice(fd)
        assert i2cDevice.fd == result[0]
    

    @pytest.mark.parametrize("addrs, Msg, result",
                            [( 30, [31, 32], [[30], False, [31, 32], True]),
                             ( 20, [21, 22], [[20], False, [21, 22], True]),
                             ( 10, [11, 12], [[10], False, [11, 12], True]),
                             ( 0, [1, 2], [[0], False, [1, 2], True])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_read_msg(i2c_mock, addrs, Msg, result):
        i2cDev = I2CDevice('/dev/i2c-10')
        i2cDev.i2cdev.Message.return_value.data = i2cDev.i2cdev.Message
        MsgList = i2cDev.set_read_msg(addrs, Msg)
        i2cDev.i2cdev.Message.assert_any_call(result[0], read=result[1])
        i2cDev.i2cdev.Message.assert_any_call(result[2], read=result[3])
        assert len(MsgList) == i2cDev.i2cdev.Message.call_count


    # Get Read Message
    # Set Write Message
    @pytest.mark.parametrize("addrs, Msg, result",
                            [( 30, [31, 32], [[30, 31, 32], False]),
                             ( 20, [21, 22], [[20, 21, 22], False]),
                             ( 10, [11, 12], [[10, 11, 12], False]),
                             ( 0, [1, 2], [[0, 1, 2], False])
                            ])
    @patch('edgepi.peripherals.i2c.I2C')
    def test_i2c_set_write_msg(i2c_mock, addrs, Msg, result):
        i2cDevice = I2CDevice('/dev/i2c-10')
        i2cDevice.i2cdev.Message.return_value.data = i2cDevice.i2cdev.Message
        MsgList = i2cDevice.set_write_msg(addrs, Msg)
        i2cDevice.i2cdev.Message.assert_called_with(result[0], read=result[1])
        assert len(MsgList) == i2cDevice.i2cdev.Message.call_count

    #Transfer Read
    @pytest.mark.parametrize("devAddress, msg, result",
                            [( 33, [2,False,[0, 0],True], [255, 255]),
                             ( 32, [2,False,[0, 0],True], [255, 255])
                            ])
    def test_i2c_transfer_read(devAddress, msg, result):
        i2cDevice = I2CDevice('/dev/i2c-10')
        MsgList = i2cDevice.set_read_msg(msg[0], msg[2])
        MsgList = i2cDevice.transfer(devAddress, MsgList)
        assert MsgList == result

    @pytest.mark.parametrize("devAddress, msg, result",
                            [( 33, [2,False,[0, 0],True], [255, 255]),
                             ( 32, [2,False,[0, 0],True], [255, 255])
                            ])
    def test_i2c_transfer_read(devAddress, msg, result):
        i2cDevice = I2CDevice('/dev/i2c-10')
        MsgList = i2cDevice.set_read_msg(msg[0], msg[2])
        MsgList = i2cDevice.transfer(devAddress, MsgList)
        assert MsgList == result