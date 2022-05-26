import pytest
from dataclasses import FrozenInstanceError
from edgepi.adc.adc_configs import *
from edgepi.adc.adc_constants import EDGEPI_ADC_REG as regs

@pytest.fixture(name='adc_configs')
def fixture_test_ADC_ops():
    adc_configs = [AdcRegID(), AdcRegPower()]
    return adc_configs

    with pytest.raises(Exception) as e:
        adc_ops.read_register_command(address, num_of_regs)
        assert e.type is error

def test_id_register_value(adc_configs):
    assert adc_configs[regs.REG_ID.value].get_value() == 0x20

@pytest.mark.parametrize("dev_id, rev_id, error", [(1, 1, FrozenInstanceError),
                                                    (0, 1, FrozenInstanceError)])
def test_id_register_value_exception(dev_id, rev_id, error, adc_configs):
    with pytest.raises(Exception) as e:
        adc_configs[regs.REG_ID.value].dev_id = dev_id
        adc_configs[regs.REG_ID.value].rev_id = rev_id
        assert adc_configs[regs.REG_ID.value].get_value() == error

@pytest.mark.parametrize("reset, vbias, intref, result", [(1, 0, 1, 0x11),
                                                          (0, 0, 1, 0x01)])
def test_power_register_value(reset, vbias, intref, result, adc_configs):
    adc_configs[regs.REG_POWER.value].reset = reset
    adc_configs[regs.REG_POWER.value].vbias = vbias
    adc_configs[regs.REG_POWER.value].intref = intref
    assert adc_configs[regs.REG_POWER.value].get_value() == result