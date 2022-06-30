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
def test_getPeriphConfig(config, result):
    assert getPeriphConfig(config) == result

@pytest.mark.parametrize('config, result', 
                       [(GpioConfigs.DAC.value,[GPIOAddresses.CONFIGURATION_PORT_0.value,GPIOAddresses.OUTPUT_PORT_0.value]),
                        (GpioConfigs.ADC.value,[GPIOAddresses.CONFIGURATION_PORT_1.value,GPIOAddresses.OUTPUT_PORT_1.value]),
                        (GpioConfigs.RTD.value,[GPIOAddresses.CONFIGURATION_PORT_1.value,GPIOAddresses.OUTPUT_PORT_1.value]),
                        (GpioConfigs.LED.value,[GPIOAddresses.CONFIGURATION_PORT_1.value,GPIOAddresses.OUTPUT_PORT_1.value])
                        ])
def test_getPinConfigAddress(config, result):
    pinConfig, pinOut = getPinConfigAddress(config)
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
def test_getDefaultValues(config, reg_dict, result):
    pinList = generate_pin_info(config)
    getDefaultValues(reg_dict, pinList)
    assert reg_dict == result
    
@pytest.mark.parametrize('config, result',[('adc',[0, 2]), ('dac',[8, 1]), ('rtd',[0, 1]), ('led',[8, 0])])
def test_checkMultipleDev(config, result):
    pinList_org = generate_pin_info(config)
    pinList = checkMultipleDev(pinList_org)
    assert len(pinList[0]) == result[0]
    assert len(pinList[1]) == result[1]
    

@pytest.mark.parametrize('pinConfig', 
                       [(GpioConfigs.DAC.value),
                        (GpioConfigs.ADC.value),
                        (GpioConfigs.RTD.value),
                        (GpioConfigs.LED.value)
                        ])
def test_setPinStates(pinConfig):
    pinList = generate_pin_info(pinConfig.name)
    pinList = setPinStates(pinList)
    for pin in pinList:
        assert pin.is_high == False
        assert pin.is_out == True