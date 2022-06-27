from audioop import add
import pytest
from unittest import mock
from unittest.mock import DEFAULT, patch
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

else:
    @pytest.mark.parametrize("fd, result",
                            [( '/dev/i2c-10', ['/dev/i2c-10'])
                            ])
    def test_i2c_init_param(fd, result):
        i2cDevice = I2CDevice(fd)
        assert i2cDevice.fd == result[0]
    

    @pytest.mark.parametrize("addrs, Msg, result",
                            [( 30, [31, 32], [[30], [31, 32], False, True]),
                             ( 20, [21, 22], [[20], [21, 22], False, True]),
                             ( 10, [11, 12], [[10], [11, 12], False, True]),
                             ( 0, [1, 2], [[0], [1, 2], False, True])
                            ])
    @patch('edgepi.peripherals.i2c.I2C.Message')
    def test_i2c_setReadMsg(i2c_mock, addrs, Msg, result):
        i2c_mock().data1 = result[0]
        i2c_mock().data2 = result[1]
        i2c_mock().read1 = result[2]
        i2c_mock().read2 = result[3]
        i2cDevice = I2CDevice('/dev/i2c-10')
        MsgList = i2cDevice.setReadMsg(addrs, Msg)
        assert MsgList[0].data1 == result[0]
        assert MsgList[1].data2 == result[1]
        assert MsgList[0].read1 == result[2]
        assert MsgList[1].read2 == result[3]

    # Get Read Message
    # Set Write Message
    @pytest.mark.parametrize("addrs, Msg, result",
                            [( 30, [31, 32], [[30, 31, 32], False]),
                             ( 20, [21, 22], [[20, 21, 22], False]),
                             ( 10, [11, 12], [[10, 11, 12], False]),
                             ( 0, [1, 2], [[0, 1, 2], False])
                            ])
    @patch('edgepi.peripherals.i2c.I2C.Message')
    def test_i2c_setWriteMsg(i2c_mock, addrs, Msg, result):
        i2c_mock().data = result[0]
        i2c_mock().read = result[1]
        i2cDevice = I2CDevice('/dev/i2c-10')
        MsgList = i2cDevice.setWriteMsg(addrs, Msg)
        assert MsgList[0].data == result[0]
        assert MsgList[0].read == result[1]