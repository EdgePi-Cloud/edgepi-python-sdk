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

# @pytest.mark.parametrize('config, pinDirList, pinOutList', 
#                        [(GpioConfigs.DAC.value,
#                         [GpioAPinDir.ALL_DIR_OUT.value.op_code, GpioAOutputClear.CLEAR_OUTPUT_ALL.value.op_code],
#                         [GpioAPinDir.PIN1_DIR_OUT.value.op_code, GpioAOutputClear.CLEAR_OUTPUT_1.value.op_code]),
#                         (GpioConfigs.ADC.value,
#                         [GpioBPinDir.PIN2_DIR_OUT.value.op_code,GpioBPinDir.PIN3_DIR_OUT.value.op_code],
#                         [GpioBOutputClear.CLEAR_OUTPUT_2.value.op_code, GpioBOutputClear.CLEAR_OUTPUT_3.value.op_code]),
#                         (GpioConfigs.RTD.value,
#                         [GpioBPinDir.PIN1_DIR_OUT.value.op_code],
#                         [GpioBOutputClear.CLEAR_OUTPUT_1.value.op_code]),
#                         (GpioConfigs.LED.value,
#                         [GpioBPinDir.ALL_DIR_OUT.value.op_code],
#                         [GpioBOutputClear.CLEAR_OUTPUT_ALL.value.op_code])
#                         ])
# def test_getDefaultValues(config, expPinconfigList, exppinOutList):
#     pinConfigList, pinOutList = getDefaultValues(config)
#     assert pinConfigList == expPinconfigList
#     assert pinOutList == exppinOutList

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