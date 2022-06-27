from enum import Enum, unique
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

@dataclass(frozen = True)
class GpioADCConfig:
    ''' Represents peripheral information for GPIOs used ADC

        Attributes:
            name (str): name of config

            device (str): peripheral device

            num_pins (int): number of pins used for this configuration

            address (GpioExpanderAdreess): addresses of i2c device

            dev_path (str): device path to the peripheral device file
    '''

    name: str = 'adc'
    device: str = 'i2c'
    num_pins: int = 2
    address: GpioExpanderAddress = GpioExpanderAddress
    dev_path: str = '/dev/i2c-10'

@dataclass(frozen = True)
class GpioRTDConfig:
    ''' Represents peripheral information for GPIOs used RTD

        Attributes:
            name (str): name of config

            device (str): peripheral device

            num_pins (int): number of pins used for this configuration

            address (GpioExpanderAdreess): addresses of i2c device

            dev_path (str): device path to the peripheral device file
    '''

    name: str = 'rtd'
    device: str = 'i2c'
    num_pins: int = 1
    address: GpioExpanderAddress = GpioExpanderAddress
    dev_path: str = '/dev/i2c-10'

@dataclass(frozen = True)
class GpioLEDConfig:
    ''' Represents peripheral information for GPIOs used LED array

        Attributes:
            name (str): name of config

            device (str): peripheral device

            num_pins (int): number of pins used for this configuration

            address (GpioExpanderAdreess): addresses of i2c device

            dev_path (str): device path to the peripheral device file
    '''

    name: str = 'led'
    device: str = 'i2c'
    num_pins: int = 8
    address: GpioExpanderAddress = GpioExpanderAddress
    dev_path: str = '/dev/i2c-10'

@unique
class GpioConfigs(Enum):
    DAC = GpioDACConfig
    ADC = GpioADCConfig
    RTD = GpioRTDConfig
    LED = GpioLEDConfig

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
_list_of_ADC_gpios = ['GNDSW_IN1', 'GNDSW_IN2']
_list_of_RTD_gpios = ['RTD_EN']
_list_of_LED_gpios = ['LED_OVR1', 'LED_OVR2' 'LED_OVR3' 'LED_OVR4''LED_OVR5''LED_OVR6', 'LED_OVR7', 'LED_OVR8']



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

def _generate_LED_pins():
    ''' Generates a list I2cPinInfo dataclasses for LED pins

        Args:
            N/A
        
        Returns:
            a list of dataclass with gpio information
    '''
    pin_list = []
    for pin, set, clear in zip(_list_of_LED_gpios, GpioBOutputSet, GpioBOutputClear):
        pin_list.append(I2cPinInfo(pin, set.value, clear.value, GpioExpanderAddress.EXP_ONE.value))
    return pin_list

def _generate_ADC_pins():
    ''' Generates a list I2cPinInfo dataclasses for ADC pins

        Args:
            N/A
        
        Returns:
            a list of dataclass with gpio information
    '''
    pin_list = []
    pin_list.append(I2cPinInfo(_list_of_ADC_gpios[0], GpioBOutputSet.SET_OUTPUT_2.value, GpioBOutputClear.CLEAR_OUTPUT_2.value, GpioExpanderAddress.EXP_TWO.value))
    pin_list.append(I2cPinInfo(_list_of_ADC_gpios[1], GpioBOutputSet.SET_OUTPUT_3.value, GpioBOutputClear.CLEAR_OUTPUT_3.value, GpioExpanderAddress.EXP_TWO.value))
    return pin_list

def _generate_RTD_pins():
    ''' Generates a list I2cPinInfo dataclasses for RTD pins

        Args:
            N/A
        
        Returns:
            a list of dataclass with gpio information
    '''
    pin_list = []
    pin_list.append(I2cPinInfo(_list_of_RTD_gpios[0], GpioBOutputSet.SET_OUTPUT_1.value, GpioBOutputClear.CLEAR_OUTPUT_1.value, GpioExpanderAddress.EXP_TWO.value))
    return pin_list


def generate_pin_info(config:str):
    ''' Generates a list pin info dataclasses

        Args:
            config (str): name of the module to configure the gpio pins fors
        
        Returns:
            a list of dataclass with gpio information
    '''
    pin_list=[]

    if config == 'dac':
       pin_list =  _generate_dac_pins()
    if config == 'led':
       pin_list =  _generate_LED_pins()
    if config == 'adc':
       pin_list =  _generate_ADC_pins()
    if config == 'rtd':
       pin_list =  _generate_RTD_pins()

    return pin_list