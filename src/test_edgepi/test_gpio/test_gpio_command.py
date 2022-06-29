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

@pytest.mark.parametrize('config, result', 
                       [(GpioConfigs.DAC.value,[GpioAPinDir.ALL_DIR_OUT.value.op_code,GpioAPinDir.ALL_DIR_OUT.value.op_code]),
                        (GpioConfigs.ADC.value,[GpioBPinDir.ALL_DIR_OUT.value.op_code,GpioBPinDir.ALL_DIR_OUT.value.op_code]),
                        (GpioConfigs.RTD.value,[GpioBPinDir.ALL_DIR_OUT.value.op_code,GpioBPinDir.ALL_DIR_OUT.value.op_code]),
                        (GpioConfigs.LED.value,[GpioBPinDir.ALL_DIR_OUT.value.op_code,GpioBPinDir.ALL_DIR_OUT.value.op_code])
                        ])
def test_getDefaultValues(config, result):
    pinConfig, pinOut = getDefaultValues(config)
    assert pinConfig == result[0]
    assert pinOut == result[1]