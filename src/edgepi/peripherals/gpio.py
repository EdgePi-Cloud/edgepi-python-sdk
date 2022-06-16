from periphery import GPIO, I2C

class GpioDevice():
    _dev_path = '/dev/'
    _gpioSettings = {'DIN1': ['gpiochip0', 26, 'in', 'pull_down'],
                     'DIN2': ['gpiochip0', 6,  'in', 'pull_down'],
                     'DIN3': ['gpiochip0', 11, 'in', 'pull_down'],
                     'DIN4': ['gpiochip0', 9,  'in', 'pull_down'],
                     'DIN5': ['gpiochip0', 22, 'in', 'pull_down'],
                     'DIN6': ['gpiochip0', 27, 'in', 'pull_down'],
                     'DIN7': ['gpiochip0', 3,  'in', 'pull_down'],
                     'DIN8': ['gpiochip0', 2,  'in', 'pull_down'],
                     'DOUT1': ['gpiochip0', 13,  'out', 'pull_down'],
                     'DOUT2': ['gpiochip0', 12,  'out', 'pull_down'],
                     'LED_OVR1' : ['i2c-10', 0, 'out', 'pull_down', 32, 'PORTB'],
                     'LED_OVR2' : ['i2c-10', 1, 'out', 'pull_down', 32, 'PORTB'],
                     'LED_OVR3' : ['i2c-10', 2, 'out', 'pull_down', 32, 'PORTB'],
                     'LED_OVR4' : ['i2c-10', 3, 'out', 'pull_down', 32, 'PORTB'],
                     'LED_OVR5' : ['i2c-10', 4, 'out', 'pull_down', 32, 'PORTB'],
                     'LED_OVR6' : ['i2c-10', 5, 'out', 'pull_down', 32, 'PORTB'],
                     'LED_OVR7' : ['i2c-10', 6, 'out', 'pull_down', 32, 'PORTB'],
                     'LED_OVR8' : ['i2c-10', 7, 'out', 'pull_down', 32, 'PORTB'],
                     'AO_EN1' : ['i2c-10', 0, 'out', 'pull_down', 32, 'PORTA'], #TODO: double check the pin numbering
                     'AO_EN2' : ['i2c-10', 1, 'out', 'pull_down', 32, 'PORTA'],
                     'AO_EN3' : ['i2c-10', 2, 'out', 'pull_down', 32, 'PORTA'],
                     'AO_EN4' : ['i2c-10', 3, 'out', 'pull_down', 32, 'PORTA'],
                     'AO_EN5' : ['i2c-10', 4, 'out', 'pull_down', 32, 'PORTA'],
                     'AO_EN6' : ['i2c-10', 5, 'out', 'pull_down', 32, 'PORTA'],
                     'AO_EN7' : ['i2c-10', 6, 'out', 'pull_down', 32, 'PORTA'],
                     'AO_EN8' : ['i2c-10', 7, 'out', 'pull_down', 32, 'PORTA'],
                     'DOUT3' : ['i2c-10', 0, 'out', 'pull_down', 33, 'PORTA'], #TODO: double check the pin numbering
                     'DOUT4' : ['i2c-10', 1, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT5' : ['i2c-10', 2, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT6' : ['i2c-10', 3, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT7' : ['i2c-10', 4, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT8' : ['i2c-10', 5, 'out', 'pull_down', 33, 'PORTA'],
                     'RTD_EN' : ['i2c-10', 0, 'out', 'pull_down', 33, 'PORTB'],
                     'GND_SW1' : ['i2c-10', 1, 'out', 'pull_down', 33, 'PORTB'],
                     'GND_SW2' : ['i2c-10', 2, 'out', 'pull_down', 33, 'PORTB'],
                    }

    def __init__(self, pin_name: str = None):
        self.fd = GpioDevice._gpioSettings[pin_name][0]
        self.pin_num = GpioDevice._gpioSettings[pin_name][1]
        self.pin_dir = GpioDevice._gpioSettings[pin_name][2]
        self.pin_bias = GpioDevice._gpioSettings[pin_name][3]
        self.dev_address = GpioDevice._gpioSettings[pin_name][4] if self.fd == 'i2c-10' else None
        self.port_num = GpioDevice._gpioSettings[pin_name][5]if self.fd == 'i2c-10' else None

