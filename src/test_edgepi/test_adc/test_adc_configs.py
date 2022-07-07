import pytest
from dataclasses import FrozenInstanceError
from edgepi.adc.adc_configs import *
from edgepi.adc.adc_constants import EdgePiADCReg as regs

@pytest.fixture(name='adc_configs')
def fixture_test_ADC_ops():
    adc_configs = [AdcRegID(), AdcRegPower(), AdcRegInterface(), AdcRegMode0(), AdcRegMode1(), AdcRegMode2()]
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

@pytest.mark.parametrize("timeout, status, crc, result", [(0, 1, 1, 0x5),
                                                          (0, 0, 3, 0x03),
                                                          (1, 1, 3, 0x0F)])
def test_interface_register_value(timeout, status, crc, result, adc_configs):
    adc_configs[regs.REG_INTERFACE.value].timeout = timeout
    adc_configs[regs.REG_INTERFACE.value].status = status
    adc_configs[regs.REG_INTERFACE.value].crc = crc
    assert adc_configs[regs.REG_INTERFACE.value].get_value() == result

@pytest.mark.parametrize("refrev, runmode, chop, delay, result", [(0, 0, 0, 0, 0x0),
                                                                  (1, 1, 1, 1, 0xD1),
                                                                  (0, 0, 3, 0, 0x30)])
def test_mode0_register_value(refrev, runmode, chop, delay, result, adc_configs):
    adc_configs[regs.REG_MODE0.value].refrev = refrev
    adc_configs[regs.REG_MODE0.value].runmode = runmode
    adc_configs[regs.REG_MODE0.value].chop = chop
    adc_configs[regs.REG_MODE0.value].delay = delay
    assert adc_configs[regs.REG_MODE0.value].get_value() == result

@pytest.mark.parametrize("filter, sbadc, sbpol, sbmag, result", [(4, 0, 0, 0, 0x80),
                                                                  (4, 1, 1, 7, 0x9F),
                                                                  (7, 0, 0, 7, 0xE7)])
def test_mode1_register_value(filter, sbadc, sbpol, sbmag, result, adc_configs):
    adc_configs[regs.REG_MODE1.value].filter = filter
    adc_configs[regs.REG_MODE1.value].sbadc = sbadc
    adc_configs[regs.REG_MODE1.value].sbpol = sbpol
    adc_configs[regs.REG_MODE1.value].sbmag = sbmag
    assert adc_configs[regs.REG_MODE1.value].get_value() == result

@pytest.mark.parametrize("bypass, gain, dr, result", [(0, 0, 4, 0x04),
                                                             (1, 7, 15, 0xFF),
                                                             (1, 1, 3, 0x93)])
def test_mode2_register_value(bypass, gain, dr, result, adc_configs):
    adc_configs[regs.REG_MODE2.value].bypass = bypass
    adc_configs[regs.REG_MODE2.value].gain = gain
    adc_configs[regs.REG_MODE2.value].dr = dr
    assert adc_configs[regs.REG_MODE2.value].get_value() == result

