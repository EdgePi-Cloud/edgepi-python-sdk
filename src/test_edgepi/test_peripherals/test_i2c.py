""" unit tests for peripherals/i2c.py """


import sys
from unittest import mock
from unittest.mock import patch
import pytest
from edgepi.peripherals.i2c import I2CDevice

if sys.platform != "linux":
    sys.modules["periphery"] = mock.MagicMock()


if sys.platform != "linux":

    @pytest.mark.parametrize(
        "fd, mock_expects",
        [
            ("/dev/i2c-10", ["/dev/i2c-10"]),
            ("/dev/i2c-11", ["/dev/i2c-11"]),
            ("/dev/i2c-12", ["/dev/i2c-12"]),
            ("/dev/i2c-13", ["/dev/i2c-13"]),
        ],
    )
    @patch("edgepi.peripherals.i2c.I2C")
    def test_i2c_init_param(i2c_mock, fd, mock_expects):
        i2c_mock.fd = mock_expects[0]
        i2c_device = I2CDevice(fd)
        assert i2c_device.fd == fd

    @pytest.mark.parametrize(
        "addrs, msg, result",
        [
            (30, [31, 32], [[30], [31, 32], False, True]),
            (20, [21, 22], [[20], [21, 22], False, True]),
            (10, [11, 12], [[10], [11, 12], False, True]),
            (0, [1, 2], [[0], [1, 2], False, True]),
        ],
    )
    @patch("edgepi.peripherals.i2c.I2C")
    # pylint: disable=no-member
    def test_i2c_set_read_msg(i2c_mock, addrs, msg, result):
        i2c_device = I2CDevice("/dev/i2c-10")
        i2c_mock.Message.return_value.data1 = result[0]
        i2c_mock.Message.return_value.data2 = result[1]
        i2c_mock.Message.return_value.read1 = result[2]
        i2c_mock.Message.return_value.read2 = result[3]
        msg_list = i2c_device.set_read_msg(addrs, msg)
        assert msg_list[0].data1 == result[0]
        assert msg_list[1].data2 == result[1]
        assert msg_list[0].read1 == result[2]
        assert msg_list[1].read2 == result[3]

    # Get Read Message
    # Set Write Message
    @pytest.mark.parametrize(
        "addrs, msg, result",
        [
            (30, [31, 32], [[30, 31, 32], False]),
            (20, [21, 22], [[20, 21, 22], False]),
            (10, [11, 12], [[10, 11, 12], False]),
            (0, [1, 2], [[0, 1, 2], False]),
        ],
    )
    @patch("edgepi.peripherals.i2c.I2C")
    def test_i2c_set_write_msg(i2c_mock, addrs, msg, result):
        i2c_device = I2CDevice("/dev/i2c-10")
        i2c_mock.Message.return_value.data = result[0]
        i2c_mock.Message.return_value.read = result[1]
        msg_list = i2c_device.set_write_msg(addrs, msg)
        assert msg_list[0].data == result[0]
        assert msg_list[0].read == result[1]

else:

    @pytest.mark.parametrize("fd, result", [("/dev/i2c-10", ["/dev/i2c-10"])])
    def test_i2c_init_param(mocker, fd, result):
        mocker.patch("edgepi.peripherals.i2c.I2C")
        i2c_device = I2CDevice(fd)
        assert i2c_device.fd == result[0]

    @pytest.mark.parametrize(
        "addrs, msg, result",
        [
            (30, [31, 32], [[30], [31, 32], False, True]),
            (20, [21, 22], [[20], [21, 22], False, True]),
            (10, [11, 12], [[10], [11, 12], False, True]),
            (0, [1, 2], [[0], [1, 2], False, True]),
        ],
    )
    @patch("edgepi.peripherals.i2c.I2C")
    # pylint: disable=no-member
    def test_i2c_set_read_msg(i2c_mock, addrs, msg, result):
        i2c_device = I2CDevice("/dev/i2c-10")
        i2c_mock.Message.return_value.data1 = result[0]
        i2c_mock.Message.return_value.data2 = result[1]
        i2c_mock.Message.return_value.read1 = result[2]
        i2c_mock.Message.return_value.read2 = result[3]
        msg_list = i2c_device.set_read_msg(addrs, msg)
        assert msg_list[0].data1 == result[0]
        assert msg_list[1].data2 == result[1]
        assert msg_list[0].read1 == result[2]
        assert msg_list[1].read2 == result[3]

    # Get Read Message
    # Set Write Message
    @pytest.mark.parametrize(
        "addrs, msg, result",
        [
            (30, [31, 32], [[30, 31, 32], False]),
            (20, [21, 22], [[20, 21, 22], False]),
            (10, [11, 12], [[10, 11, 12], False]),
            (0, [1, 2], [[0, 1, 2], False]),
        ],
    )
    @patch("edgepi.peripherals.i2c.I2C")
    def test_i2c_set_write_msg(i2c_mock, addrs, msg, result):
        i2c_device = I2CDevice("/dev/i2c-10")
        i2c_mock.Message.return_value.data = result[0]
        i2c_mock.Message.return_value.read = result[1]
        msg_list = i2c_device.set_write_msg(addrs, msg)
        assert msg_list[0].data == result[0]
        assert msg_list[0].read == result[1]
