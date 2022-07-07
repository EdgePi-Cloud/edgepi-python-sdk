import pytest
from edgepi.gpio.gpio_commands import get_periph_config
from edgepi.gpio.gpio_configs import GpioConfigs


@pytest.mark.parametrize(
    "config, result",
    [
        ("dac", GpioConfigs.DAC.value),
        ("adc", GpioConfigs.ADC.value),
        ("rtd", GpioConfigs.RTD.value),
        ("din", None),
        ("dout", None),
        ("led", GpioConfigs.LED.value),
        (None, None),
    ],
)
def test_get_periph_config(config, result):
    assert get_periph_config(config) == result
