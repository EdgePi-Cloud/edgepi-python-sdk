import pytest
from edgepi.gpio.gpio_commands import *
from edgepi.gpio.gpio_configs import *

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
                       [(GpioConfigs.DAC.value,[GPIOAddresses.CONFIGURATION_PORT_0.value,GPIOAddresses.OUTPUT_PORT_0.value]),
                        (GpioConfigs.ADC.value,[GPIOAddresses.CONFIGURATION_PORT_1.value,GPIOAddresses.OUTPUT_PORT_1.value]),
                        (GpioConfigs.RTD.value,[GPIOAddresses.CONFIGURATION_PORT_1.value,GPIOAddresses.OUTPUT_PORT_1.value]),
                        (GpioConfigs.LED.value,[GPIOAddresses.CONFIGURATION_PORT_1.value,GPIOAddresses.OUTPUT_PORT_1.value])
                        ])
def test_get_pin_config_address(config, result):
    pinConfig, pinOut = get_pin_config_address(config)
    assert pinConfig == result[0]
    assert pinOut == result[1]

@pytest.mark.parametrize('config, reg_dict, result', 
                       [('adc', {3 : 255, 7 : 255}, {3: {'value': 249, 'is_changed': True},
                                                     7: {'value': 249, 'is_changed': True}}),
                        ('led', {3 : 255, 7 : 255}, {3: {'value': 0, 'is_changed': True},
                                                     7: {'value': 0, 'is_changed': True}}),
                        ('rtd', {3 : 255, 7 : 255}, {3: {'value': 254, 'is_changed': True},
                                                     7: {'value': 254, 'is_changed': True}})
                        ])
def test_get_default_values(config, reg_dict, result):
    pin_list = generate_pin_info(config)
    get_default_values(reg_dict, pin_list)
    assert reg_dict == result
    
@pytest.mark.parametrize('config, result',[('adc',[0, 2]), ('dac',[8, 1]), ('rtd',[0, 1]), ('led',[8, 0])])
def test_check_multiple_dev(config, result):
    pin_list_org = generate_pin_info(config)
    pin_list = check_multiple_dev(pin_list_org)
    assert len(pin_list[0]) == result[0]
    assert len(pin_list[1]) == result[1]
    

@pytest.mark.parametrize('pinConfig', 
                       [(GpioConfigs.DAC.value),
                        (GpioConfigs.ADC.value),
                        (GpioConfigs.RTD.value),
                        (GpioConfigs.LED.value)
                        ])
def test_set_pin_states(pinConfig):
    pin_list = generate_pin_info(pinConfig.name)
    pin_list = set_pin_states(pin_list)
    for pin in pin_list:
        assert pin.is_high == False
        assert pin.is_out == True