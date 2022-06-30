import pytest
from edgepi.reg_helper.reg_helper import OpCode
from edgepi.gpio.gpio_constants import *
from edgepi.gpio.gpio_configs import *


@pytest.mark.parametrize('config, result', 
                        [(GpioConfigs.DAC.value, ['dac', 'i2c', 9, 'out', 'A', GpioExpanderAddress, '/dev/i2c-10']),
                         (GpioConfigs.ADC.value, ['adc', 'i2c', 2, 'out', 'B', 33, '/dev/i2c-10']),
                         (GpioConfigs.RTD.value, ['rtd', 'i2c', 1, 'out', 'B', 33, '/dev/i2c-10']),
                         (GpioConfigs.LED.value, ['led', 'i2c', 8, 'in', 'B', 32, '/dev/i2c-10'])
                        ])
def test_GpioModuleConfig(config, result):
    assert config.name == result[0]
    assert config.device == result[1]
    assert config.num_pins == result[2]
    assert config.dir == result[3]
    assert config.port == result[4]
    assert config.address == result[5]
    assert config.dev_path == result[6]

@pytest.mark.parametrize('name, setoutput, clearoutput, pinDir, address, result', 
                        [('AO_EN1', GpioAOutputSet.SET_OUTPUT_1.value, GpioAOutputClear.CLEAR_OUTPUT_1.value, GpioAPinDir.ALL_DIR_IN.value, GpioExpanderAddress.EXP_ONE.value, ['AO_EN1', OpCode(1, 2, 0xFE), OpCode(0, 2, 0xFE), OpCode(0xFF, 6, 0), 32]),
                         ('AO_EN1', GpioAOutputSet.SET_OUTPUT_2.value, GpioBOutputClear.CLEAR_OUTPUT_2.value, GpioBPinDir.ALL_DIR_OUT.value, GpioExpanderAddress.EXP_ONE.value, ['AO_EN1',OpCode(2, 2, 0xFD), OpCode(0, 3, 0xFD), OpCode(0, 7, 0), 32]),
                         ('AO_EN1', GpioBOutputSet.SET_OUTPUT_3.value, GpioAOutputClear.CLEAR_OUTPUT_3.value, GpioAPinDir.ALL_DIR_IN.value, GpioExpanderAddress.EXP_ONE.value, ['AO_EN1', OpCode(4, 3, 0xFB), OpCode(0, 2, 0xFB), OpCode(0xFF, 6, 0), 32]),
                         ('AO_EN1', GpioBOutputSet.SET_OUTPUT_4.value, GpioBOutputClear.CLEAR_OUTPUT_4.value, GpioBPinDir.ALL_DIR_OUT.value, GpioExpanderAddress.EXP_TWO.value, ['AO_EN1', OpCode(8, 3, 0xF7), OpCode(0, 3, 0xF7), OpCode(0, 7, 0), 33])
                        ])
def test_I2cPinInfo(name, setoutput, clearoutput, pinDir, address, result):
    pin = I2cPinInfo(name, setoutput, clearoutput, pinDir, address)
    assert pin.name == result[0]
    assert pin.setCode == result[1]
    assert pin.clearCode == result[2]
    assert pin.dirCode == result[3]
    assert pin.address == result[4]
    assert pin.is_high == None
    assert pin.is_out == None



def test_generate_pin_info_dac(config = 'dac', pin_name_list = ['AO_EN1','AO_EN4','AO_EN3','AO_EN2','AO_EN5','AO_EN6','AO_EN7','AO_EN8', 'DAC_GAIN']):
    pin_list = generate_pin_info(config)
    for pin, outputset, outputclear, outputDir, pin_name in zip(pin_list[:-1], GpioAOutputSet, GpioAOutputClear, GpioAPinDir, pin_name_list):
        assert pin.name == pin_name
        assert pin.setCode == outputset.value
        assert pin.clearCode == outputclear.value
        assert pin.dirCode == outputDir.value
        assert pin.address == GpioExpanderAddress.EXP_ONE.value
    assert pin_list[8].name == pin_name_list[8]
    assert pin_list[8].setCode == GpioAOutputSet.SET_OUTPUT_1.value
    assert pin_list[8].clearCode == GpioAOutputClear.CLEAR_OUTPUT_1.value
    assert pin_list[8].dirCode == GpioAPinDir.PIN1_DIR_OUT.value
    assert pin_list[8].address == GpioExpanderAddress.EXP_TWO.value
    
def test_generate_pin_info_led(config = 'led', pin_name_list = ['LED_OVR1', 'LED_OVR2', 'LED_OVR3', 'LED_OVR4','LED_OVR5','LED_OVR6', 'LED_OVR7', 'LED_OVR8']):
    pin_list = generate_pin_info(config)
    for pin, outputset, outputclear, outputDir, pin_name in zip(pin_list, GpioBOutputSet, GpioBOutputClear, GpioBPinDir, pin_name_list):
        assert pin.name == pin_name
        assert pin.setCode == outputset.value
        assert pin.clearCode == outputclear.value
        assert pin.dirCode == outputDir.value
        assert pin.address == GpioExpanderAddress.EXP_ONE.value

def test_generate_pin_info_RTD(config = 'rtd', pin_name_list = ['RTD_EN']):
    pin_list = generate_pin_info(config)
    for pin, outputset, outputclear, outputDir, pin_name in zip(pin_list, GpioBOutputSet, GpioBOutputClear, GpioBPinDir, pin_name_list):
        assert pin.name == pin_name
        assert pin.setCode == outputset.value
        assert pin.clearCode == outputclear.value
        assert pin.dirCode == outputDir.value
        assert pin.address == GpioExpanderAddress.EXP_TWO.value

def test_generate_pin_info_ADC(config = 'adc', pin_name_list = ['GNDSW_IN1', 'GNDSW_IN2']):
    pin_list = generate_pin_info(config)
    assert pin_list[0].name == pin_name_list[0]
    assert pin_list[0].setCode == GpioBOutputSet.SET_OUTPUT_2.value
    assert pin_list[0].clearCode == GpioBOutputClear.CLEAR_OUTPUT_2.value
    assert pin_list[0].dirCode == GpioBPinDir.PIN2_DIR_OUT.value
    assert pin_list[0].address == GpioExpanderAddress.EXP_TWO.value
    assert pin_list[1].name == pin_name_list[1]
    assert pin_list[1].setCode == GpioBOutputSet.SET_OUTPUT_3.value
    assert pin_list[1].clearCode == GpioBOutputClear.CLEAR_OUTPUT_3.value
    assert pin_list[1].dirCode == GpioBPinDir.PIN3_DIR_OUT.value
    assert pin_list[1].address == GpioExpanderAddress.EXP_TWO.value