'''unit tests for gpio_commands module'''


import pytest
from edgepi.gpio.gpio_commands import (
    get_periph_config,
    get_pin_config_address,
    break_pin_info_dict,
    get_default_values,
    check_multiple_dev,
    set_pin_states)
from edgepi.gpio.gpio_constants import GPIOAddresses
from edgepi.gpio.gpio_configs import GpioConfigs, generate_pin_info

@pytest.mark.parametrize('config, result',
                       [('dac', GpioConfigs.DAC.value),
                        ('adc', GpioConfigs.ADC.value),
                        ('rtd', GpioConfigs.RTD.value),
                        ('din', None),
                        ('dout', None),
                        ('led', GpioConfigs.LED.value),
                        ( None, None)])
def test_get_periph_config(config, result):
    assert get_periph_config(config) == result

@pytest.mark.parametrize('config, result',
                       [(GpioConfigs.DAC.value,
                         [GPIOAddresses.CONFIGURATION_PORT_0.value,
                          GPIOAddresses.OUTPUT_PORT_0.value]),
                        (GpioConfigs.ADC.value,
                         [GPIOAddresses.CONFIGURATION_PORT_1.value,
                         GPIOAddresses.OUTPUT_PORT_1.value]),
                        (GpioConfigs.RTD.value,
                         [GPIOAddresses.CONFIGURATION_PORT_1.value,
                         GPIOAddresses.OUTPUT_PORT_1.value]),
                        (GpioConfigs.LED.value,
                         [GPIOAddresses.CONFIGURATION_PORT_1.value,
                         GPIOAddresses.OUTPUT_PORT_1.value])
                        ])
def test_get_pin_config_address(config, result):
    pin_config, pin_out = get_pin_config_address(config)
    assert pin_config == result[0]
    assert pin_out == result[1]

@pytest.mark.parametrize('config, reg_dict, result',
                       [(GpioConfigs.ADC.value,
                         {3 : 255, 7 : 255},
                         {3: {'value': 249, 'is_changed': True},
                          7: {'value': 249, 'is_changed': True}}),
                        (GpioConfigs.LED.value,
                         {3 : 255, 7 : 255},
                         {3: {'value': 0, 'is_changed': True},
                          7: {'value': 0, 'is_changed': True}}),
                        (GpioConfigs.RTD.value,
                         {3 : 255, 7 : 255},
                         {3: {'value': 254, 'is_changed': True},
                          7: {'value': 254, 'is_changed': True}})
                        ])
def test_get_default_values(config, reg_dict, result):
    pin_dict_list = break_pin_info_dict(generate_pin_info(config))
    for pin_dict in pin_dict_list:
        get_default_values(reg_dict, list(pin_dict.values()))
        assert reg_dict == result

@pytest.mark.parametrize('config, result',[(GpioConfigs.ADC.value, [33]),
                                           (GpioConfigs.DAC.value, [32, 33]),
                                           (GpioConfigs.RTD.value, [33]),
                                           (GpioConfigs.LED.value, [32])])
def test_check_multiple_dev(config, result):
    pin_dict_org = generate_pin_info(config)
    list_of_address = check_multiple_dev(pin_dict_org)
    assert list_of_address == result

@pytest.mark.parametrize('config, result',[(GpioConfigs.ADC.value,
                                            generate_pin_info(GpioConfigs.ADC.value)),
                                           (GpioConfigs.DAC.value,
                                            generate_pin_info(GpioConfigs.DAC.value)),
                                           (GpioConfigs.RTD.value,
                                            generate_pin_info(GpioConfigs.RTD.value)),
                                           (GpioConfigs.LED.value,
                                            generate_pin_info(GpioConfigs.LED.value))])
def test_break_pin_info_dict(config, result):
    pin_dict = generate_pin_info(config)
    list_pin_dict = break_pin_info_dict(pin_dict)
    for element in list_pin_dict:
        for key in element.keys():
            assert element[key] == result[key]


@pytest.mark.parametrize('pin_config',
                       [(GpioConfigs.DAC.value),
                        (GpioConfigs.ADC.value),
                        (GpioConfigs.RTD.value),
                        (GpioConfigs.LED.value)
                        ])
def test_set_pin_states(pin_config):
    pin_dict = generate_pin_info(pin_config)
    pin_dict = set_pin_states(pin_dict)
    for key in pin_dict:
        assert pin_dict[key].is_high is False
        assert pin_dict[key].is_out is True
