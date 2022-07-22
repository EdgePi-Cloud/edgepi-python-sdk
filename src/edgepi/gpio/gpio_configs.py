""" Utility module for GPIO configuration """


from enum import Enum, unique
from typing import Union
from dataclasses import dataclass
from edgepi.gpio.gpio_constants import (
    GpioAOutputClear,
    GpioAOutputSet,
    GpioBOutputClear,
    GpioBOutputSet,
    GpioExpanderAddress,
    GpioAPinDir,
    GpioBPinDir
)


@dataclass(frozen=True)
class GpioExpanderConfig:
    """Represents peripheral information for GPIOs used DAC

    Attributes:
        name (str): name of config

        device (str): peripheral device

        num_pins (int): number of pins used for this configuration

        address (GpioExpanderAdreess): addresses of i2c device

        dev_path (str): device path to the peripheral device file
    """

    name: str = None
    device: str = None
    num_pins: int = None
    dir: str = None
    port: str = None
    address: Union[GpioExpanderAddress, int] = None
    dev_path: str = None


@unique
class GpioConfigs(Enum):
    '''Enum Class for GPIO configurations dataclasses'''
    DAC = GpioExpanderConfig(name = 'dac',
                             device='i2c',
                             num_pins=9,
                             dir='out',
                             port='A',
                             address=GpioExpanderAddress,
                             dev_path='/dev/i2c-10')
    ADC = GpioExpanderConfig(name = 'adc',
                             device='i2c',
                             num_pins=2,
                             dir='out',
                             port='B',
                             address=GpioExpanderAddress.EXP_TWO.value,
                             dev_path='/dev/i2c-10')
    RTD = GpioExpanderConfig(name = 'rtd',
                             device='i2c',
                             num_pins=1,
                             dir='out',
                             port='B',
                             address=GpioExpanderAddress.EXP_TWO.value,
                             dev_path='/dev/i2c-10')
    LED = GpioExpanderConfig(name = 'led',
                             device='i2c',
                             num_pins=8,
                             dir='in',
                             port='B',
                             address=GpioExpanderAddress.EXP_ONE.value,
                             dev_path='/dev/i2c-10')

@dataclass
class I2cPinInfo:
    '''
    Represents I2C pin information

        Attributes:

            set_code (GpioAOutputSet, GpioBOutputSet): Output set code

            clear_code (GpioAOutputClear, GpioBOutputClear): Output clear code

            address (int): address of i2c device
    '''
    set_code: Union[GpioAOutputSet, GpioBOutputSet] = None
    clear_code: Union[GpioAOutputClear, GpioBOutputClear] = None
    dir_code: Union[GpioAPinDir, GpioBPinDir] = None
    address: int = None
    is_high: bool = None
    is_out: bool = None

_list_of_DAC_gpios = ['AO_EN1', 'AO_EN4', 'AO_EN3', 'AO_EN2',
                      'AO_EN5', 'AO_EN6', 'AO_EN7', 'AO_EN8', 'DAC_GAIN']
_list_of_ADC_gpios = ['GNDSW_IN1', 'GNDSW_IN2']
_list_of_RTD_gpios = ['RTD_EN']
_list_of_LED_gpios = ['LED_OVR1', 'LED_OVR2', 'LED_OVR3', 'LED_OVR4',
                      'LED_OVR5','LED_OVR6', 'LED_OVR7', 'LED_OVR8']
_list_of_DIN_gpios =  ['DIN1', 'DIN2', 'DIN3', 'DIN4',
                       'DIN5', 'DIN6', 'DIN7', 'DIN8']
_list_of_DOUT_gpios = {'DOUT1', 'DOUT2', 'DOUT3', 'DOUT4',
                       'DOUT5', 'DOUT6', 'DOUT7', 'DOUT8'}


def _generate_DAC_pins(): #pylint: disable=C0103
    ''' Generates a list I2cPinInfo dataclasses for DAC pins
        Args:
            N/A
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''
    pin_dict = {}
    for pin, set_code, clear_code, dir_code in \
        zip(_list_of_DAC_gpios, GpioAOutputSet, GpioAOutputClear, GpioAPinDir):

        pin_dict.update({pin : I2cPinInfo(set_code.value,
                                          clear_code.value,
                                          dir_code.value,
                                          GpioExpanderAddress.EXP_ONE.value)
                        })
    pin_dict['DAC_GAIN'] =\
        I2cPinInfo(GpioAOutputSet.SET_OUTPUT_1.value,
                   GpioAOutputClear.CLEAR_OUTPUT_1.value,
                   GpioAPinDir.PIN1_DIR_OUT.value,
                   GpioExpanderAddress.EXP_TWO.value)
    return pin_dict

def _generate_LED_pins(): #pylint: disable=C0103
    '''
        Args:
            N/A
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''
    pin_dict = {}
    for pin, set_code, clear_code, dir_code in\
        zip(_list_of_LED_gpios, GpioBOutputSet, GpioBOutputClear, GpioBPinDir):

        pin_dict.update({pin : I2cPinInfo(set_code.value,
                                          clear_code.value,
                                          dir_code.value,
                                          GpioExpanderAddress.EXP_ONE.value)})
    return pin_dict

def _generate_ADC_pins(): #pylint: disable=C0103
    '''
        Args:
            N/A
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''
    pin_dict = {}
    pin_dict.update({_list_of_ADC_gpios[0] : I2cPinInfo(GpioBOutputSet.SET_OUTPUT_2.value,
                                                        GpioBOutputClear.CLEAR_OUTPUT_2.value,
                                                        GpioBPinDir.PIN2_DIR_OUT.value,
                                                        GpioExpanderAddress.EXP_TWO.value)})
    pin_dict.update({_list_of_ADC_gpios[1] : I2cPinInfo(GpioBOutputSet.SET_OUTPUT_3.value,
                                                        GpioBOutputClear.CLEAR_OUTPUT_3.value,
                                                        GpioBPinDir.PIN3_DIR_OUT.value,
                                                        GpioExpanderAddress.EXP_TWO.value)})
    return pin_dict

def _generate_RTD_pins(): #pylint: disable=C0103
    '''
        Args:
            N/A
        Returns:
        a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''
    pin_dict = {}
    pin_dict.update({_list_of_RTD_gpios[0] : I2cPinInfo(GpioBOutputSet.SET_OUTPUT_1.value,
                                                        GpioBOutputClear.CLEAR_OUTPUT_1.value,
                                                        GpioBPinDir.PIN1_DIR_OUT.value,
                                                        GpioExpanderAddress.EXP_TWO.value)})
    return pin_dict

def generate_pin_info(config:GpioExpanderConfig = None):
    ''' Generates a dictionary of pin info dataclasses
        Args:
            config (GpioExpanderConfig): name of the module to configure the gpio pins fors
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''

    if config.name == 'dac':
        pin_dict =  _generate_DAC_pins()
    elif config.name == 'led':
        pin_dict =  _generate_LED_pins()
    elif config.name == 'adc':
        pin_dict =  _generate_ADC_pins()
    elif config.name == 'rtd':
        pin_dict =  _generate_RTD_pins()

    return pin_dict
