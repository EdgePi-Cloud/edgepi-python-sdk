from periphery import GPIO

class GpioDevice():
    _dev_path = "/dev/gpiochip0"

    def __init__(self, pin_num: int = None, pin_dir: str = None, pin_bias: str = None):
        self.fd = GpioDevice._dev_path
        self.pin_num = pin_num
        self.pin_dir = pin_dir
        self.pin_bias = pin_bias
        self.gpio = GPIO(self.fd, self.pin_num, self.pin_dir, 'none', self.pin_bias, "default" , False, None)

    def close(self):
        self.gpio.close()