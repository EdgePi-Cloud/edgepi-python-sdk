import pytest
from unittest import mock
from unittest.mock import patch
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
                            [( '/dev/i2c-10', ['/dev/i2c-10']),
                             ( '/dev/i2c-11', ['/dev/i2c-11']),
                             ( '/dev/i2c-12', ['/dev/i2c-12']),
                             ( '/dev/i2c-13', ['/dev/i2c-13'])
                            ])
    def test_i2c_init_param(fd, result):
        i2cDevice = I2CDevice(fd)
        assert i2cDevice.fd == result[0]
    # Set Read Message
    # Get Read Message
    # Set Write Message
    # Get Write Message