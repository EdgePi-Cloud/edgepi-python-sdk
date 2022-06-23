import pytest
from edgepi.reg_helper.reg_helper import OpCode
from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import GpioDACConfig, I2cPinInfo, generate_pin_info

def test_GpioDACConfig():
    assert GpioDACConfig.name == 'dac'
    assert GpioDACConfig.device == 'i2c'
    assert GpioDACConfig.num_pins == 9
    assert GpioDACConfig.address.EXP_ONE.value == 32
    assert GpioDACConfig.address.EXP_TWO.value == 33
    assert GpioDACConfig.dev_path == '/dev/i2c-10'

@pytest.mark.parametrize('name, setoutput, clearoutput, address, result', 
                        [('AO_EN1', GpioAOutputSet.SET_OUTPUT_1.value, GpioAOutputClear.CLEAR_OUTPUT_1.value, GpioExpanderAdreess.EXP_ONE.value, ['AO_EN1', OpCode(1, 2, 0xFE), OpCode(0, 2, 0xFE), 32]),
                         ('AO_EN1', GpioAOutputSet.SET_OUTPUT_2.value, GpioAOutputClear.CLEAR_OUTPUT_2.value, GpioExpanderAdreess.EXP_ONE.value, ['AO_EN1',OpCode(2, 2, 0xFD), OpCode(0, 2, 0xFD), 32]),
                         ('AO_EN1', GpioAOutputSet.SET_OUTPUT_3.value, GpioAOutputClear.CLEAR_OUTPUT_3.value, GpioExpanderAdreess.EXP_ONE.value, ['AO_EN1', OpCode(4, 2, 0xFB), OpCode(0, 2, 0xFB), 32]),
                         ('AO_EN1', GpioAOutputSet.SET_OUTPUT_4.value, GpioAOutputClear.CLEAR_OUTPUT_4.value, GpioExpanderAdreess.EXP_TWO.value, ['AO_EN1', OpCode(8, 2, 0xF7), OpCode(0, 2, 0xF7), 33])
                        ])
def test_I2cPinInfo(name, setoutput, clearoutput, address, result):
    pin = I2cPinInfo(name, setoutput, clearoutput, address)
    assert pin.name == result[0]
    assert pin.setOutput == result[1]
    assert pin.clearOutput == result[2]
    assert pin.address == result[3]

# @pytest.mark.parametrize('config, pin_name_list, address', 
#                         [('dac', ['AO_EN1','AO_EN4','AO_EN3','AO_EN2','AO_EN5','AO_EN6','AO_EN7','AO_EN8', 'DAC_GAIN'], GpioExpanderAdreess.EXP_TWO.value)
#                         ])
def test_generate_pin_info_dac(config = 'dac', pin_name_list = ['AO_EN1','AO_EN4','AO_EN3','AO_EN2','AO_EN5','AO_EN6','AO_EN7','AO_EN8', 'DAC_GAIN']):
    pin_list = generate_pin_info(config)
    for pin, outputset, outputclear, pin_name in zip(pin_list[:-1], GpioAOutputSet, GpioAOutputClear, pin_name_list):
        assert pin.name == pin_name
        assert pin.setOutput == outputset.value
        assert pin.clearOutput == outputclear.value
        assert pin.address == GpioExpanderAdreess.EXP_ONE.value
    assert pin_list[8].name == pin_name_list[8]
    assert pin_list[8].setOutput == GpioAOutputSet.SET_OUTPUT_1.value
    assert pin_list[8].clearOutput == GpioAOutputClear.CLEAR_OUTPUT_1.value
    assert pin_list[8].address == GpioExpanderAdreess.EXP_TWO.value
    
    