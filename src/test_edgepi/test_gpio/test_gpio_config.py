import pytest
from edgepi.reg_helper.reg_helper import OpCode
from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *


@pytest.mark.parametrize('config, result', 
                        [(GpioConfigs.DAC.value, ['dac', 'i2c', 9, 32, '/dev/i2c-10']),
                         (GpioConfigs.ADC.value, ['adc', 'i2c', 2, 33, '/dev/i2c-10']),
                         (GpioConfigs.RTD.value, ['rtd', 'i2c', 1, 33, '/dev/i2c-10']),
                         (GpioConfigs.LED.value, ['led', 'i2c', 8, 32, '/dev/i2c-10'])
                        ])
def test_Gpio_module_config(config, result):
    assert config.name == result[0]
    assert config.device == result[1]
    assert config.num_pins == result[2]
    assert config.address.value == result[3]
    assert config.dev_path == result[4]

@pytest.mark.parametrize('name, setoutput, clearoutput, address, result', 
                        [('AO_EN1', GpioAOutputSet.SET_OUTPUT_1.value, GpioAOutputClear.CLEAR_OUTPUT_1.value, GpioExpanderAddress.EXP_ONE.value, ['AO_EN1', OpCode(1, 2, 0xFE), OpCode(0, 2, 0xFE), 32]),
                         ('AO_EN1', GpioAOutputSet.SET_OUTPUT_2.value, GpioAOutputClear.CLEAR_OUTPUT_2.value, GpioExpanderAddress.EXP_ONE.value, ['AO_EN1',OpCode(2, 2, 0xFD), OpCode(0, 2, 0xFD), 32]),
                         ('AO_EN1', GpioAOutputSet.SET_OUTPUT_3.value, GpioAOutputClear.CLEAR_OUTPUT_3.value, GpioExpanderAddress.EXP_ONE.value, ['AO_EN1', OpCode(4, 2, 0xFB), OpCode(0, 2, 0xFB), 32]),
                         ('AO_EN1', GpioAOutputSet.SET_OUTPUT_4.value, GpioAOutputClear.CLEAR_OUTPUT_4.value, GpioExpanderAddress.EXP_TWO.value, ['AO_EN1', OpCode(8, 2, 0xF7), OpCode(0, 2, 0xF7), 33])
                        ])
def test_i2c_pin_info_init(name, setoutput, clearoutput, address, result):
    pin = I2cPinInfo(name, setoutput, clearoutput, address)
    assert pin.name == result[0]
    assert pin.set_code == result[1]
    assert pin.clear_code == result[2]
    assert pin.address == result[3]


def test_generate_pin_info_dac(config = 'dac', pin_name_list = ['AO_EN1','AO_EN4','AO_EN3','AO_EN2','AO_EN5','AO_EN6','AO_EN7','AO_EN8', 'DAC_GAIN']):
    pin_list = generate_pin_info(config)
    for pin, outputset, outputclear, pin_name in zip(pin_list[:-1], GpioAOutputSet, GpioAOutputClear, pin_name_list):
        assert pin.name == pin_name
        assert pin.set_code == outputset.value
        assert pin.clear_code == outputclear.value
        assert pin.address == GpioExpanderAddress.EXP_ONE.value
    assert pin_list[8].name == pin_name_list[8]
    assert pin_list[8].set_code == GpioAOutputSet.SET_OUTPUT_1.value
    assert pin_list[8].clear_code == GpioAOutputClear.CLEAR_OUTPUT_1.value
    assert pin_list[8].address == GpioExpanderAddress.EXP_TWO.value
    
def test_generate_pin_info_led(config = 'led', pin_name_list = ['LED_OVR1', 'LED_OVR2' 'LED_OVR3' 'LED_OVR4''LED_OVR5''LED_OVR6', 'LED_OVR7', 'LED_OVR8']):
    pin_list = generate_pin_info(config)
    for pin, outputset, outputclear, pin_name in zip(pin_list, GpioBOutputSet, GpioBOutputClear, pin_name_list):
        assert pin.name == pin_name
        assert pin.set_code == outputset.value
        assert pin.clear_code == outputclear.value
        assert pin.address == GpioExpanderAddress.EXP_ONE.value

def test_generate_pin_info_RTD(config = 'rtd', pin_name_list = ['RTD_EN']):
    pin_list = generate_pin_info(config)
    for pin, outputset, outputclear, pin_name in zip(pin_list, GpioBOutputSet, GpioBOutputClear, pin_name_list):
        assert pin.name == pin_name
        assert pin.set_code == outputset.value
        assert pin.clear_code == outputclear.value
        assert pin.address == GpioExpanderAddress.EXP_TWO.value

def test_generate_pin_info_ADC(config = 'adc', pin_name_list = ['GNDSW_IN1', 'GNDSW_IN2']):
    pin_list = generate_pin_info(config)
    assert pin_list[0].name == pin_name_list[0]
    assert pin_list[0].set_code == GpioBOutputSet.SET_OUTPUT_2.value
    assert pin_list[0].clear_code == GpioBOutputClear.CLEAR_OUTPUT_2.value
    assert pin_list[0].address == GpioExpanderAddress.EXP_TWO.value
    assert pin_list[1].name == pin_name_list[1]
    assert pin_list[1].set_code == GpioBOutputSet.SET_OUTPUT_3.value
    assert pin_list[1].clear_code == GpioBOutputClear.CLEAR_OUTPUT_3.value
    assert pin_list[1].address == GpioExpanderAddress.EXP_TWO.value