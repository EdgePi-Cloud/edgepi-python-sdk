from dataclasses import dataclass
from edgepi.gpio.gpio_constants import * 

@dataclass(frozen = True)
class GpioDACConfig:
    ''' Represents peripheral information for GPIOs used DAC

        Attributes:
            name (str): name of config

            device (str): peripheral device

            num_pins (int): number of pins used for this configuration

            address (GpioExpanderAdreess): addresses of i2c device

            dev_path (str): device path to the peripheral device file
    '''

    name: str = 'dac'
    device: str = 'i2c'
    num_pins: int = 9
    address: GpioExpanderAddress = GpioExpanderAddress
    dev_path: str = '/dev/i2c-10'

@dataclass
class I2cPinInfo:
    ''' Represents I2C pin information

        Attributes:
            name (str): name of the pin

            dir (str): direction of the pin in or out

            port (str): port group A or B

            address (int): address of i2c device
    '''
    name: str = None
    setCode: GpioAOutputSet = None
    clearCode: GpioAOutputClear = None
    address: int = None

# TODO: add more configs and list of pins for different modules

_list_of_DAC_gpios = ['AO_EN1','AO_EN4','AO_EN3','AO_EN2','AO_EN5','AO_EN6','AO_EN7','AO_EN8', 'DAC_GAIN']

def _generate_dac_pins():
    ''' Generates a list I2cPinInfo dataclasses for DAC pins

        Args:
            N/A
        
        Returns:
            a list of dataclass with gpio information
    '''
    pin_list = []
    for pin, set, clear in zip(_list_of_DAC_gpios, GpioAOutputSet, GpioAOutputClear):
        pin_list.append(I2cPinInfo(pin, set.value, clear.value, GpioExpanderAddress.EXP_ONE.value))
    pin_list[8] = I2cPinInfo(_list_of_DAC_gpios[8], GpioAOutputSet.SET_OUTPUT_1.value, GpioAOutputClear.CLEAR_OUTPUT_1.value, GpioExpanderAddress.EXP_TWO.value)
    return pin_list

def generate_pin_info(config:str):
    ''' Generates a list pin info dataclasses

        Args:
            config (str): name of the module to configure the gpio pins for
        
        Returns:
            a list of dataclass with gpio information
    '''
    pin_list=[]

    if config == 'dac':
       pin_list =  _generate_dac_pins()

    return pin_list