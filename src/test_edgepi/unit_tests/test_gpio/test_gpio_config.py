"""unit tests for gpio_config module"""


import pytest
from edgepi.reg_helper.reg_helper import OpCode
from edgepi.gpio.gpio_constants import (
    GpioAOutputClear,
    GpioAOutputSet,
    GpioAPinDirIn,
    GpioBOutputClear,
    GpioBOutputSet,
    GpioExpanderAddress,
    GpioAPinDirOut,
    GpioBPinDirOut
)
from edgepi.gpio.gpio_configs import (
    GpioConfigs,
    I2cPinInfo,
    generate_pin_info,
    generate_expander_pin_info,
    generate_gpiochip_pin_info
)

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
                          GpioAPinDirIn.ALL_DIR_IN.value,
                          GpioExpanderAddress.EXP_ONE.value,
                          ['AO_EN1',
                           OpCode(1, 3, 0xFE),
                           OpCode(0, 3, 0xFE),
                           OpCode(0xFF, 7, 0),
                           32]),
                         (GpioAOutputSet.SET_OUTPUT_2.value,
                          GpioBOutputClear.CLEAR_OUTPUT_2.value,
                          GpioBPinDirOut.ALL_DIR_OUT.value,
                          GpioExpanderAddress.EXP_ONE.value,
                          ['AO_EN1',
                           OpCode(2, 3, 0xFD),
                           OpCode(0, 2, 0xFD),
                           OpCode(0, 6, 0),
                           32]),
                         (GpioBOutputSet.SET_OUTPUT_3.value,
                          GpioAOutputClear.CLEAR_OUTPUT_3.value,
                          GpioAPinDirIn.ALL_DIR_IN.value,
                          GpioExpanderAddress.EXP_ONE.value,
                          ['AO_EN1',
                           OpCode(4, 2, 0xFB),
                           OpCode(0, 3, 0xFB),
                           OpCode(0xFF, 7, 0),
                           32]),
                         (GpioBOutputSet.SET_OUTPUT_4.value,
                          GpioBOutputClear.CLEAR_OUTPUT_4.value,
                          GpioBPinDirOut.ALL_DIR_OUT.value,
                          GpioExpanderAddress.EXP_TWO.value,
                          ['AO_EN1',
                           OpCode(8, 2, 0xF7),
                           OpCode(0, 2, 0xF7),
                           OpCode(0, 6, 0),
                           33])
                        ])
def test_i2c_pin_info(set_output, clear_output, pin_dir, address, result):
    pin = I2cPinInfo(set_output, clear_output, pin_dir, None, address)
    assert pin.set_code == result[1]
    assert pin.clear_code == result[2]
    assert pin.dir_out_code == result[3]
    assert pin.address == result[4]
    assert pin.is_high is None
    assert pin.is_out is None



def test_generate_pin_info_dac(config = GpioConfigs.DAC.value):
    pin_list = generate_pin_info(config)
    for pin, output_set, output_clear, output_dir in\
    zip(pin_list.items(), GpioAOutputSet, GpioAOutputClear, GpioAPinDirOut):

        if pin[0] != 'DAC_GAIN':
            assert pin[1].set_code == output_set.value
            assert pin[1].clear_code == output_clear.value
            assert pin[1].dir_out_code == output_dir.value
            assert pin[1].address == GpioExpanderAddress.EXP_ONE.value
    assert pin_list['DAC_GAIN'].set_code == GpioAOutputSet.SET_OUTPUT_1.value
    assert pin_list['DAC_GAIN'].clear_code == GpioAOutputClear.CLEAR_OUTPUT_1.value
    assert pin_list['DAC_GAIN'].dir_out_code == GpioAPinDirOut.PIN1_DIR_OUT.value
    assert pin_list['DAC_GAIN'].address == GpioExpanderAddress.EXP_TWO.value

def test_generate_pin_info_led(config = GpioConfigs.LED.value):
    pin_list = generate_pin_info(config)
    for pin, output_set, output_clear, output_dir in\
    zip(pin_list.items(), GpioBOutputSet, GpioBOutputClear, GpioBPinDirOut):

        assert pin[1].set_code == output_set.value
        assert pin[1].clear_code == output_clear.value
        assert pin[1].dir_out_code == output_dir.value
        assert pin[1].address == GpioExpanderAddress.EXP_ONE.value

def test_generate_pin_info_rtd(config = GpioConfigs.RTD.value):
    pin_list = generate_pin_info(config)
    for pin, output_set, output_clear, output_dir in\
    zip(pin_list.items(), GpioBOutputSet, GpioBOutputClear, GpioBPinDirOut):

        assert pin[1].set_code == output_set.value
        assert pin[1].clear_code == output_clear.value
        assert pin[1].dir_out_code == output_dir.value
        assert pin[1].address == GpioExpanderAddress.EXP_TWO.value

def test_generate_pin_info_adc(config = GpioConfigs.ADC.value):
    pin_list = generate_pin_info(config)
    pin_keys = list(pin_list.keys())
    assert pin_list[pin_keys[0]].set_code == GpioBOutputSet.SET_OUTPUT_2.value
    assert pin_list[pin_keys[0]].clear_code == GpioBOutputClear.CLEAR_OUTPUT_2.value
    assert pin_list[pin_keys[0]].dir_out_code == GpioBPinDirOut.PIN2_DIR_OUT.value
    assert pin_list[pin_keys[0]].address == GpioExpanderAddress.EXP_TWO.value

    assert pin_list[pin_keys[1]].set_code == GpioBOutputSet.SET_OUTPUT_3.value
    assert pin_list[pin_keys[1]].clear_code == GpioBOutputClear.CLEAR_OUTPUT_3.value
    assert pin_list[pin_keys[1]].dir_out_code == GpioBPinDirOut.PIN3_DIR_OUT.value
    assert pin_list[pin_keys[1]].address == GpioExpanderAddress.EXP_TWO.value

def test_generate_pin_info_din(config = GpioConfigs.DIN.value):
    pin_dict = generate_pin_info(config)
    pin_keys = list(pin_dict.keys())
    for pin in pin_keys:
        assert pin_dict[pin].dir == 'in'
        assert pin_dict[pin].bias == 'pull_down'

def test_generate_expander_pin_info():
    pin_dict = generate_expander_pin_info()
    result_dict = {}
    result_dict.update(generate_pin_info(GpioConfigs.DAC.value))
    result_dict.update(generate_pin_info(GpioConfigs.ADC.value))
    result_dict.update(generate_pin_info(GpioConfigs.RTD.value))
    result_dict.update(generate_pin_info(GpioConfigs.LED.value))
    result_dict.update(generate_pin_info(GpioConfigs.DOUT2.value))
    assert pin_dict == result_dict

def test_generate_gpiochip_pin_info():
    pin_dict = generate_gpiochip_pin_info()
    result_dict = {}
    result_dict.update(generate_pin_info(GpioConfigs.DIN.value))
    result_dict.update(generate_pin_info(GpioConfigs.DOUT1.value))
    assert pin_dict == result_dict
