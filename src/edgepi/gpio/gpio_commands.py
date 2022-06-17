from edgepi.peripherals.gpio import GpioDevice
from edgepi.peripherals.i2c import I2CDevice
from edgepi.gpio.gpio_constants import *

class GPIOCommands(I2CDevice):
    _gpioSettings = {'DIN1':      ['gpio',26, 'in', 'pull_down'],
                     'DIN2':      ['gpio',6,  'in', 'pull_down'],
                     'DIN3':      ['gpio',11, 'in', 'pull_down'],
                     'DIN4':      ['gpio',9,  'in', 'pull_down'],
                     'DIN5':      ['gpio',22, 'in', 'pull_down'],
                     'DIN6':      ['gpio',27, 'in', 'pull_down'],
                     'DIN7':      ['gpio',3,  'in', 'pull_down'],
                     'DIN8':      ['gpio',2,  'in', 'pull_down'],
                     'DOUT1':     ['gpio',13,  'out', 'pull_down'],
                     'DOUT2':     ['gpio',12,  'out', 'pull_down'],
                     'LED_OVR1' : ['i2c', GpioBPinDir.PIN1_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_1.value, 32, 'PORTB'], # TODO: double check the default conditions
                     'LED_OVR2' : ['i2c', GpioBPinDir.PIN2_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_2.value, 32, 'PORTB'],
                     'LED_OVR3' : ['i2c', GpioBPinDir.PIN3_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_3.value, 32, 'PORTB'],
                     'LED_OVR4' : ['i2c', GpioBPinDir.PIN4_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_4.value, 32, 'PORTB'],
                     'LED_OVR5' : ['i2c', GpioBPinDir.PIN5_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_5.value, 32, 'PORTB'],
                     'LED_OVR6' : ['i2c', GpioBPinDir.PIN6_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_6.value, 32, 'PORTB'],
                     'LED_OVR7' : ['i2c', GpioBPinDir.PIN7_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_7.value, 32, 'PORTB'],
                     'LED_OVR8' : ['i2c', GpioBPinDir.PIN8_DIR_OUT.value, GpioBOutputClear.CLEAR_OUTPUT_8.value, 32, 'PORTB'],
                     'AO_EN1' :   ['i2c', GpioAPinDir.PIN8_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_8.value, 32, 'PORTA'], #TODO: double check the pin numbering
                     'AO_EN2' :   ['i2c', GpioAPinDir.PIN5_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_5.value, 32, 'PORTA'],
                     'AO_EN3' :   ['i2c', GpioAPinDir.PIN6_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_6.value, 32, 'PORTA'],
                     'AO_EN4' :   ['i2c', GpioAPinDir.PIN7_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_7.value, 32, 'PORTA'],
                     'AO_EN5' :   ['i2c', GpioAPinDir.PIN4_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_4.value, 32, 'PORTA'],
                     'AO_EN6' :   ['i2c', GpioAPinDir.PIN3_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_3.value, 32, 'PORTA'],
                     'AO_EN7' :   ['i2c', GpioAPinDir.PIN2_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_2.value, 32, 'PORTA'],
                     'AO_EN8' :   ['i2c', GpioAPinDir.PIN1_DIR_OUT.value, GpioAOutputClear.CLEAR_OUTPUT_1.value, 32, 'PORTA'],
                     'DOUT3' :    ['i2c',0, 'out', 'pull_down', 33, 'PORTA'], #TODO: double check the pin numbering
                     'DOUT4' :    ['i2c',1, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT5' :    ['i2c',2, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT6' :    ['i2c',3, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT7' :    ['i2c',4, 'out', 'pull_down', 33, 'PORTA'],
                     'DOUT8' :    ['i2c',5, 'out', 'pull_down', 33, 'PORTA'],
                     'RTD_EN' :   ['i2c',0, 'out', 'pull_down', 33, 'PORTB'],
                     'GND_SW1' :  ['i2c',1, 'out', 'pull_down', 33, 'PORTB'],
                     'GND_SW2' :  ['i2c',2, 'out', 'pull_down', 33, 'PORTB'],
                    }
    def __init__(self, pinList: list = None):
        self.gpioPinDict = {}
        self.i2cPinList  = {}
        for pin in pinList:
            if GPIOCommands._gpioSettings[pin][0] == 'gpio':
                self.gpioPinList[pin] = GpioDevice(pin_num=GPIOCommands._gpioSettings[pin][1], 
                                                   pin_dir=GPIOCommands._gpioSettings[pin][2],
                                                   pin_bias=GPIOCommands._gpioSettings[pin][3])
            else:
                self.i2cPinList[pin] = GPIOCommands._gpioSettings[pin]
        self.i2cDev = super().__init__(fd='/dev/i2c-10') if self.i2cPinList else None