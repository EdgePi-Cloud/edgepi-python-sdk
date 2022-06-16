import pytest
from edgepi.peripherals.gpio import GpioDevice

@pytest.mark.parametrize("pin_name, fd, pin_num, pin_dir, pin_bias, dev_address, port_num",
                        [('DIN6', 'gpiochip0', 27, 'in', 'pull_down', None, None),
                         ('DIN2', 'gpiochip0', 6, 'in', 'pull_down', None, None),
                         ('DIN2', 'gpiochip0', 6, 'in', 'pull_down', None, None),
                         ('DOUT1', 'gpiochip0', 13, 'out', 'pull_down', None, None),
                         ('DOUT5', 'i2c-10', 2, 'out', 'pull_down', 33, 'PORTA')
                        ])
def test_init_param(pin_name, fd, pin_num, pin_dir, pin_bias, dev_address, port_num,):
    gpio = GpioDevice(pin_name)
    assert gpio.fd == fd
    assert gpio.pin_num == pin_num
    assert gpio.pin_dir == pin_dir
    assert gpio.pin_bias == pin_bias
    assert gpio.dev_address == dev_address
    assert gpio.port_num == port_num