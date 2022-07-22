"""unit tests for gpio_config module"""


import pytest
from edgepi.reg_helper.reg_helper import OpCode
from edgepi.gpio.gpio_constants import (
    GpioAOutputClear,
    GpioAOutputSet,
    GpioBOutputClear,
    GpioBOutputSet,
    GpioExpanderAddress,
    GpioAPinDir,
    GpioBPinDir
)
from edgepi.gpio.gpio_configs import GpioConfigs, I2cPinInfo, generate_pin_info


@pytest.mark.parametrize('config, result',
                        [(GpioConfigs.DAC.value,
                          ['dac', 'i2c', 9, 'out', 'A', GpioExpanderAddress, '/dev/i2c-10']),
                         (GpioConfigs.ADC.value,
                          ['adc', 'i2c', 2, 'out', 'B', 33, '/dev/i2c-10']),
                         (GpioConfigs.RTD.value,
                          ['rtd', 'i2c', 1, 'out', 'B', 33, '/dev/i2c-10']),
                         (GpioConfigs.LED.value,
                          ['led', 'i2c', 8, 'in', 'B', 32, '/dev/i2c-10'])
                        ])
def test_gpio_module_config(config, result):
    assert config.name == result[0]
    assert config.device == result[1]
    assert config.num_pins == result[2]
    assert config.dir == result[3]
    assert config.port == result[4]
    assert config.address == result[5]
    assert config.dev_path == result[6]

@pytest.mark.parametrize('set_output, clear_output, pin_dir, address, result',
                        [(GpioAOutputSet.SET_OUTPUT_1.value,
                          GpioAOutputClear.CLEAR_OUTPUT_1.value,
                          GpioAPinDir.ALL_DIR_IN.value,
                          GpioExpanderAddress.EXP_ONE.value,
                          ['AO_EN1',
                           OpCode(1, 2, 0xFE),
                           OpCode(0, 2, 0xFE),
                           OpCode(0xFF, 6, 0),
                           32]),
                         (GpioAOutputSet.SET_OUTPUT_2.value,
                          GpioBOutputClear.CLEAR_OUTPUT_2.value,
                          GpioBPinDir.ALL_DIR_OUT.value,
                          GpioExpanderAddress.EXP_ONE.value,
                          ['AO_EN1',
                           OpCode(2, 2, 0xFD),
                           OpCode(0, 3, 0xFD),
                           OpCode(0, 7, 0),
                           32]),
                         (GpioBOutputSet.SET_OUTPUT_3.value,
                          GpioAOutputClear.CLEAR_OUTPUT_3.value,
                          GpioAPinDir.ALL_DIR_IN.value,
                          GpioExpanderAddress.EXP_ONE.value,
                          ['AO_EN1',
                           OpCode(4, 3, 0xFB),
                           OpCode(0, 2, 0xFB),
                           OpCode(0xFF, 6, 0),
                           32]),
                         (GpioBOutputSet.SET_OUTPUT_4.value,
                          GpioBOutputClear.CLEAR_OUTPUT_4.value,
                          GpioBPinDir.ALL_DIR_OUT.value,
                          GpioExpanderAddress.EXP_TWO.value,
                          ['AO_EN1',
                           OpCode(8, 3, 0xF7),
                           OpCode(0, 3, 0xF7),
                           OpCode(0, 7, 0),
                           33])
                        ])
def test_i2c_pin_info(set_output, clear_output, pin_dir, address, result):
    pin = I2cPinInfo(set_output, clear_output, pin_dir, address)
    assert pin.set_code == result[1]
    assert pin.clear_code == result[2]
    assert pin.dir_code == result[3]
    assert pin.address == result[4]
    assert pin.is_high is None
    assert pin.is_out is None



def test_generate_pin_info_dac(config = GpioConfigs.DAC.value):
    pin_list = generate_pin_info(config)
    for pin, output_set, output_clear, output_dir in\
    zip(pin_list.items(), GpioAOutputSet, GpioAOutputClear, GpioAPinDir):

        if pin[0] != 'DAC_GAIN':
            assert pin[1].set_code == output_set.value
            assert pin[1].clear_code == output_clear.value
            assert pin[1].dir_code == output_dir.value
            assert pin[1].address == GpioExpanderAddress.EXP_ONE.value
    assert pin_list['DAC_GAIN'].set_code == GpioAOutputSet.SET_OUTPUT_1.value
    assert pin_list['DAC_GAIN'].clear_code == GpioAOutputClear.CLEAR_OUTPUT_1.value
    assert pin_list['DAC_GAIN'].dir_code == GpioAPinDir.PIN1_DIR_OUT.value
    assert pin_list['DAC_GAIN'].address == GpioExpanderAddress.EXP_TWO.value

def test_generate_pin_info_led(config = GpioConfigs.LED.value):
    pin_list = generate_pin_info(config)
    for pin, output_set, output_clear, output_dir in\
    zip(pin_list.items(), GpioBOutputSet, GpioBOutputClear, GpioBPinDir):

        assert pin[1].set_code == output_set.value
        assert pin[1].clear_code == output_clear.value
        assert pin[1].dir_code == output_dir.value
        assert pin[1].address == GpioExpanderAddress.EXP_ONE.value

def test_generate_pin_info_rtd(config = GpioConfigs.RTD.value):
    pin_list = generate_pin_info(config)
    for pin, output_set, output_clear, output_dir in\
    zip(pin_list.items(), GpioBOutputSet, GpioBOutputClear, GpioBPinDir):

        assert pin[1].set_code == output_set.value
        assert pin[1].clear_code == output_clear.value
        assert pin[1].dir_code == output_dir.value
        assert pin[1].address == GpioExpanderAddress.EXP_TWO.value

def test_generate_pin_info_adc(config = GpioConfigs.ADC.value):
    pin_list = generate_pin_info(config)
    pin_keys = list(pin_list.keys())
    assert pin_list[pin_keys[0]].set_code == GpioBOutputSet.SET_OUTPUT_2.value
    assert pin_list[pin_keys[0]].clear_code == GpioBOutputClear.CLEAR_OUTPUT_2.value
    assert pin_list[pin_keys[0]].dir_code == GpioBPinDir.PIN2_DIR_OUT.value
    assert pin_list[pin_keys[0]].address == GpioExpanderAddress.EXP_TWO.value

    assert pin_list[pin_keys[1]].set_code == GpioBOutputSet.SET_OUTPUT_3.value
    assert pin_list[pin_keys[1]].clear_code == GpioBOutputClear.CLEAR_OUTPUT_3.value
    assert pin_list[pin_keys[1]].dir_code == GpioBPinDir.PIN3_DIR_OUT.value
    assert pin_list[pin_keys[1]].address == GpioExpanderAddress.EXP_TWO.value
