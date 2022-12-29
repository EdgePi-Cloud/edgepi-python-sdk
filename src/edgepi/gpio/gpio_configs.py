""" Utility module for GPIO configuration """

from enum import Enum, unique
from typing import Union
from dataclasses import dataclass
from edgepi.gpio.gpio_constants import (
    GpioAOutputClear,
    GpioAOutputSet,
    GpioAPinDirIn,
    GpioAPinDirOut,
    GpioBOutputClear,
    GpioBOutputSet,
    GpioBPinDirIn,
    GpioBPinDirOut,
    GpioExpanderAddress,

)


@dataclass(frozen=True)
class GpioExpanderConfig:
    """Represents peripheral information for GPIOs attached on the expander

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
    address: int = None
    dev_path: str = None

@dataclass(frozen=True)
class GpioChipConfig:
    """
    Represents peripheral information for GPIOs
    Attributes:
        name (str): name of config

        device (str): peripheral device

        num_pins (int): number of pins used for this configuration

        dev_path (str): device path to the peripheral device file
    """
    name:str = None
    device: str = None
    num_pins: int = None
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
    DIN = GpioChipConfig(name = 'din',
                         device = 'gpiochip0',
                         num_pins = 8,
                         dev_path = "/dev/gpiochip0")
    DOUT1 = GpioChipConfig(name = 'dout1',
                          device = 'gpiochip0',
                          num_pins = 2,
                          dev_path = "/dev/gpiochip0")
    DOUT2 = GpioExpanderConfig(name = 'dout2',
                               device='i2c',
                               num_pins=6,
                               dir='out',
                               port='A',
                               address=GpioExpanderAddress.EXP_TWO.value,
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
    dir_out_code: Union[GpioAPinDirOut, GpioBPinDirOut] = None
    dir_in_code: Union[GpioAPinDirIn, GpioBPinDirIn] = None
    address: int = None
    is_high: bool = None
    is_out: bool = None

@dataclass
class GpioChipPinInfo:
    """
    Represents Gpiochip Pin information
    Attributes:
        dir (str): direction of the pin, high, low, in or out
        bias (str): pull_up or pull_down
    """
    dir: str = None
    bias: str = None

class DACPins(Enum):
    "DAC GPIO Pin Names"
    AO_EN1 = 'AO_EN1'
    AO_EN2 = 'AO_EN2'
    AO_EN3 = 'AO_EN3'
    AO_EN4 = 'AO_EN4'
    AO_EN5 = 'AO_EN5'
    AO_EN6 = 'AO_EN6'
    AO_EN7 = 'AO_EN7'
    AO_EN8 = 'AO_EN8'
    DAC_GAIN = 'DAC_GAIN'


_list_of_DAC_gpios = [
    DACPins.AO_EN8.value, DACPins.AO_EN7.value, DACPins.AO_EN6.value,
    DACPins.AO_EN5.value, DACPins.AO_EN2.value, DACPins.AO_EN3.value,
    DACPins.AO_EN4.value, DACPins.AO_EN1.value, DACPins.DAC_GAIN.value,
    ]


class ADCPins(Enum):
    "ADC GPIO Pin Names"
    GNDSW_IN1 = 'GNDSW_IN1'
    GNDSW_IN2 = 'GNDSW_IN2'


_list_of_ADC_gpios = [ADCPins.GNDSW_IN1.value, ADCPins.GNDSW_IN2.value]


class RTDPins(Enum):
    "RTD GPIO Pin Names"
    RTD_EN = 'RTD_EN'


_list_of_RTD_gpios = [RTDPins.RTD_EN.value]


class LEDPins(Enum):
    "LED GPIO Pin Names"
    LED_OVR1 = 'LED_OVR1'
    LED_OVR2 = 'LED_OVR2'
    LED_OVR3 = 'LED_OVR3'
    LED_OVR4 = 'LED_OVR4'
    LED_OVR5 = 'LED_OVR5'
    LED_OVR6 = 'LED_OVR6'
    LED_OVR7 = 'LED_OVR7'
    LED_OVR8 = 'LED_OVR8'


_list_of_LED_gpios = [
    LEDPins.LED_OVR1.value, LEDPins.LED_OVR2.value,
    LEDPins.LED_OVR3.value, LEDPins.LED_OVR4.value,
    LEDPins.LED_OVR5.value, LEDPins.LED_OVR6.value,
    LEDPins.LED_OVR7.value, LEDPins.LED_OVR8.value,
]


class DINPins(Enum):
    "DIN GPIO Pin Names"
    DIN1 = 'DIN1'
    DIN2 = 'DIN2'
    DIN3 = 'DIN3'
    DIN4 = 'DIN4'
    DIN5 = 'DIN5'
    DIN6 = 'DIN6'
    DIN7 = 'DIN7'
    DIN8 = 'DIN8'


_list_of_DIN_gpios =  [
    DINPins.DIN1.value, DINPins.DIN2.value,
    DINPins.DIN3.value, DINPins.DIN4.value,
    DINPins.DIN5.value, DINPins.DIN6.value,
    DINPins.DIN7.value, DINPins.DIN8.value,
]


class DOUTPins(Enum):
    "DOUT GPIO Pin Names"
    DOUT1 = 'DOUT1'
    DOUT2 = 'DOUT2'
    DOUT3 = 'DOUT3'
    DOUT4 = 'DOUT4'
    DOUT5 = 'DOUT5'
    DOUT6 = 'DOUT6'
    DOUT7 = 'DOUT7'
    DOUT8 = 'DOUT8'


_list_of_DOUT_cpu_gpios =  [
    DOUTPins.DOUT1.value, DOUTPins.DOUT2.value
]

_list_of_DOUT_expander_gpios =[
    None, None,
    DOUTPins.DOUT8.value, DOUTPins.DOUT7.value,
    DOUTPins.DOUT6.value, DOUTPins.DOUT5.value,
    DOUTPins.DOUT4.value, DOUTPins.DOUT3.value]


def _generate_DAC_pins(): #pylint: disable=C0103
    ''' Generates a list I2cPinInfo dataclasses for DAC pins
        Args:
            N/A
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''
    pin_dict = {}
    for pin, set_code, clear_code, dir_out_code, dir_in_code in \
        zip(_list_of_DAC_gpios, GpioAOutputSet, GpioAOutputClear, GpioAPinDirOut, GpioAPinDirIn):

        pin_dict.update({pin : I2cPinInfo(set_code.value,
                                          clear_code.value,
                                          dir_out_code.value,
                                          dir_in_code.value,
                                          GpioExpanderAddress.EXP_ONE.value)
                        })
    pin_dict['DAC_GAIN'] =\
        I2cPinInfo(GpioAOutputSet.SET_OUTPUT_1.value,
                   GpioAOutputClear.CLEAR_OUTPUT_1.value,
                   GpioAPinDirOut.PIN1_DIR_OUT.value,
                   GpioAPinDirIn.PIN1_DIR_IN.value,
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
    for pin, set_code, clear_code, dir_out_code, dir_in_code in\
        zip(_list_of_LED_gpios, GpioBOutputSet, GpioBOutputClear, GpioBPinDirOut, GpioBPinDirIn):

        pin_dict.update({pin : I2cPinInfo(set_code.value,
                                          clear_code.value,
                                          dir_out_code.value,
                                          dir_in_code.value,
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
                                                        GpioBPinDirOut.PIN2_DIR_OUT.value,
                                                        GpioBPinDirIn.PIN2_DIR_IN.value,
                                                        GpioExpanderAddress.EXP_TWO.value)})
    pin_dict.update({_list_of_ADC_gpios[1] : I2cPinInfo(GpioBOutputSet.SET_OUTPUT_3.value,
                                                        GpioBOutputClear.CLEAR_OUTPUT_3.value,
                                                        GpioBPinDirOut.PIN3_DIR_OUT.value,
                                                        GpioBPinDirIn.PIN3_DIR_IN.value,
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
                                                        GpioBPinDirOut.PIN1_DIR_OUT.value,
                                                        GpioBPinDirIn.PIN1_DIR_IN.value,
                                                        GpioExpanderAddress.EXP_TWO.value)})
    return pin_dict

def _generate_DIN_pins(): #pylint: disable=C0103
    """
        Args:
            N/A
        Returns:
        a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    """
    pin_dict = {}
    for pin in _list_of_DIN_gpios:
        pin_dict[pin] = GpioChipPinInfo(dir = "in", bias = "pull_down")
    return pin_dict

def _generate_DOUT_cpu_pins(): #pylint: disable=C0103
    """
        Args:
            N/A
        Returns:
        a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    """
    pin_dict = {}
    for pin in _list_of_DOUT_cpu_gpios:
        pin_dict[pin] = GpioChipPinInfo(dir = "out", bias = "pull_down")
    return pin_dict

def _generate_DOUT_expander_pins(): #pylint: disable=C0103
    """
        Args:
            N/A
        Returns:
        a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    """
    pin_dict = {}
    for pin, set_code, clear_code, dir_out_code, dir_in_code in \
    zip(_list_of_DOUT_expander_gpios,GpioAOutputSet,GpioAOutputClear,GpioAPinDirOut,GpioAPinDirIn):
        if pin is None:
            continue
        pin_dict.update({pin : I2cPinInfo(set_code.value,
                                          clear_code.value,
                                          dir_out_code.value,
                                          dir_in_code.value,
                                          GpioExpanderAddress.EXP_TWO.value)})
    return pin_dict


# This function is used inside unit testing
def generate_pin_info(config: Union[GpioExpanderConfig, GpioChipConfig] = None):
    ''' Generates a dictionary of pin info dataclasses
        Args:
            config (GpioExpanderConfig): name of the module to configure the gpio pins fors
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''

    if config.name == GpioConfigs.DAC.value.name:
        pin_dict =  _generate_DAC_pins()
    elif config.name == GpioConfigs.LED.value.name:
        pin_dict =  _generate_LED_pins()
    elif config.name == GpioConfigs.ADC.value.name:
        pin_dict =  _generate_ADC_pins()
    elif config.name == GpioConfigs.RTD.value.name:
        pin_dict =  _generate_RTD_pins()
    elif config.name == GpioConfigs.DIN.value.name:
        pin_dict = _generate_DIN_pins()
    elif config.name == GpioConfigs.DOUT1.value.name:
        pin_dict = _generate_DOUT_cpu_pins()
    elif config.name == GpioConfigs.DOUT2.value.name:
        pin_dict = _generate_DOUT_expander_pins()
    return pin_dict

def generate_expander_pin_info():
    ''' Generates a dictionary of pin info dataclasses
        Args:
            N/A
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''
    pin_dict = {}
    pin_dict.update(_generate_DAC_pins())
    pin_dict.update(_generate_ADC_pins())
    pin_dict.update(_generate_RTD_pins())
    pin_dict.update(_generate_LED_pins())
    pin_dict.update(_generate_DOUT_expander_pins())
    return pin_dict

def generate_gpiochip_pin_info():
    ''' Generates a dictionary of pin info dataclasses
        Args:
            N/A
        Returns:
            a dictionary of dataclass with gpio information, {'pin_name' : pin_info_dataclass}
    '''
    pin_dict = {}
    pin_dict.update(_generate_DIN_pins())
    pin_dict.update(_generate_DOUT_cpu_pins())
    return pin_dict
