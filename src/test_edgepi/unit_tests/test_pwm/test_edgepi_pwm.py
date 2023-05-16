"""unit tests for pwm.py module"""
# pylint: disable=wrong-import-position
from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
from contextlib import nullcontext as does_not_raise
import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.pwm.pwm_constants import PWMCh, Polarity, PWMPins
from edgepi.pwm.edgepi_pwm import EdgePiPWM

@pytest.fixture(name="pwm_dev")
def fixture_test_pwm(mocker):
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev = EdgePiPWM()
    yield pwm_dev

def test_pwm_init(mocker):
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO")
    pwm_dev = EdgePiPWM()
    assert pwm_dev._EdgePiPWM__pwm_1.channel == PWMCh.PWM_1.value.channel
    assert pwm_dev._EdgePiPWM__pwm_1.chip == PWMCh.PWM_1.value.chip
    assert pwm_dev._EdgePiPWM__pwm_2.channel == PWMCh.PWM_2.value.channel
    assert pwm_dev._EdgePiPWM__pwm_2.chip == PWMCh.PWM_2.value.chip

@pytest.mark.parametrize("target, min_range, max_range, error",
                         [(0, 0, 100, does_not_raise()),
                          (10, 0, 100, does_not_raise()),
                          (50, 0, 100, does_not_raise()),
                          (70, 0, 100, does_not_raise()),
                          (100, 0, 100, does_not_raise()),
                          (101, 0, 100, pytest.raises(ValueError)),
                          (-1, 0, 100, pytest.raises(ValueError)),
                          (1000, 1000, 10000, does_not_raise()),
                          (2000, 1000, 10000, does_not_raise()),
                          (5000, 1000, 10000, does_not_raise()),
                          (10000, 1000, 10000, does_not_raise()),
                          (999, 1000, 10000, pytest.raises(ValueError)),
                          (10001, 1000, 10000, pytest.raises(ValueError)),
                          ])
def test__check_range(target, min_range, max_range, error, pwm_dev):
    with error:
        # pylint: disable=protected-access
        assert pwm_dev._EdgePiPWM__check_range(target, min_range, max_range) is True

@pytest.mark.parametrize(
    "pwm_num, result",
    [
        (PWMPins.PWM1,[GpioPins.AO_EN1.value, GpioPins.DOUT1.value]),
        (PWMPins.PWM2, [GpioPins.AO_EN2.value, GpioPins.DOUT2.value]),
    ],
)
def test_pwm_enable(mocker, pwm_num, result):
    mocker_pwm = mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    mocker_gpio = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev = EdgePiPWM(pwm_num)
    pwm_dev.pwm = mocker_pwm
    pwm_dev.gpio = mocker_gpio
    mock_clear_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.clear_pin_state")
    mock_set_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.set_pin_state")
    pwm_dev.enable()
    pwm_dev.pwm.enable_pwm.assert_called_once()
    mock_set_pin.assert_called_with(result[0])
    mock_clear_pin.assert_has_calls([mock.call(result[1]), mock.call(pwm_num.value)])


def test_pwm_disable(pwm_dev):
    pwm_dev.disable()
    pwm_dev.pwm.disable_pwm.assert_called_once()

def test_pwm_close(pwm_dev):
    pwm_dev.close()
    pwm_dev.pwm.close_pwm.assert_called_once()

@pytest.mark.parametrize("pwm_num ,expected, error",
                         [(PWMPins.PWM1,1000, does_not_raise()),
                          (PWMPins.PWM1,5000, does_not_raise()),
                          (PWMPins.PWM1,10000, does_not_raise()),
                          (PWMPins.PWM2,1000, does_not_raise()),
                          (PWMPins.PWM2,5000, does_not_raise()),
                          (PWMPins.PWM2,10000, does_not_raise()),
                          (None,1000, pytest.raises(ValueError)),
                          (None,5000, pytest.raises(ValueError)),
                          (None,10000, pytest.raises(ValueError)),
                          ])
def test_get_frequency_pwm(mocker, pwm_num,expected, error, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_frequency_pwm", return_value = expected)
    with error:
        freq = pwm_dev.get_frequency(pwm_num)
        assert freq == expected
    

@pytest.mark.parametrize("pwm_num ,freq, error",
                         [(PWMPins.PWM1,1000, does_not_raise()),
                          (PWMPins.PWM1,5000, does_not_raise()),
                          (PWMPins.PWM1,10000, does_not_raise()),
                          (PWMPins.PWM2,1000, does_not_raise()),
                          (PWMPins.PWM2,5000, does_not_raise()),
                          (PWMPins.PWM2,10000, does_not_raise()),
                          (None,1000, pytest.raises(ValueError)),
                          (None,5000, pytest.raises(ValueError)),
                          (None,10000, pytest.raises(ValueError)),
                          ])
def test_set_frequency_pwm(mocker, pwm_num, freq, error, pwm_dev):
    set_freq_mock = mocker.patch("edgepi.peripherals.pwm.PwmDevice.set_frequency_pwm")
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_frequency_pwm", return_value = freq)
    with error:
        pwm_dev._EdgePiPWM__set_frequency(pwm_num, freq)
        result = pwm_dev.get_frequency(pwm_num)
        set_freq_mock.assert_called_once_with(pwm_num, freq)
        assert result == freq

@pytest.mark.parametrize("expected", [(50),(40),(30),(20),(10),(60),(70),(80),(90),(100)])
def test_get_duty_cycle_pwm(mocker, expected, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_duty_cycle_pwm", return_value = expected/100)
    duty_cycle = pwm_dev.get_duty_cycle()
    assert duty_cycle == expected

@pytest.mark.parametrize("duty_cycle", [(50),(40),(30),(20),(10),(60),(70),(80),(90),(100)])
def test_set_duty_cycle_pwm(mocker, duty_cycle, pwm_dev):
    set_dc_mock = mocker.patch("edgepi.peripherals.pwm.PwmDevice.set_duty_cycle_pwm")
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_duty_cycle_pwm", return_value=duty_cycle/100)
    pwm_dev.set_duty_cycle(duty_cycle)
    result = pwm_dev.get_duty_cycle()
    set_dc_mock.assert_called_once_with(duty_cycle/100)
    assert result == duty_cycle

@pytest.mark.parametrize("expected", [(Polarity.NORMAL),(Polarity.INVERSED)])
def test_get_polarity_pwm(mocker, expected, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_polarity_pwm", return_value = expected.value)
    pol = pwm_dev.get_polarity()
    assert pol == expected.value

@pytest.mark.parametrize("polarity", [(Polarity.NORMAL),(Polarity.INVERSED)])
def test_set_polarity_pwm(mocker, polarity, pwm_dev):
    set_pol_mock = mocker.patch("edgepi.peripherals.pwm.PwmDevice.set_polarity_pwm")
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_polarity_pwm", return_value = polarity.value)
    pwm_dev.set_polarity(polarity)
    result = pwm_dev.get_polarity()
    set_pol_mock.assert_called_once_with(polarity.value)
    assert result == polarity.value

@pytest.mark.parametrize("expected", [(True),(False)])
def test_get_enabled_pwm(mocker, expected, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_enabled_pwm", return_value = expected)
    enabled = pwm_dev.get_enabled()
    assert enabled == expected

@pytest.mark.parametrize("pwm_num, result", 
                         [(PWMPins.PWM1, [PWMCh.PWM_1.value.channel, PWMCh.PWM_1.value.chip]),
                          (PWMPins.PWM2, [PWMCh.PWM_2.value.channel, PWMCh.PWM_2.value.chip]),
                        ])
def test__check_pwm_device_and_instantiate_first_time(pwm_num, result, pwm_dev):
    pwm_device = pwm_dev._EdgePiPWM__check_pwm_device_and_instantiate(pwm_num)
    assert pwm_device.channel == result[0]
    assert pwm_device.chip == result[1]

@pytest.mark.parametrize("pwm_num", 
                         [(PWMPins.PWM1),
                          (PWMPins.PWM2),
                        ])
def test__check_pwm_device_and_instantiate_not_first_time(mocker, pwm_num, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    pwm_device = pwm_dev._EdgePiPWM__check_pwm_device_and_instantiate(pwm_num)
    assert pwm_device == None

@pytest.mark.parametrize("pwm_num,error", 
                         [(PWMPins.PWM1,does_not_raise()),
                          (PWMPins.PWM2,does_not_raise()),
                          (None, pytest.raises(ValueError)),
                        ])
def test_init_pwm_first_time(mocker, pwm_num,error, pwm_dev):
    mock_open = mocker.patch("edgepi.peripherals.pwm.PwmDevice.open_pwm")
    with error:
        pwm_dev.init_pwm(pwm_num)
        if pwm_num == PWMPins.PWM1:
            assert pwm_dev._EdgePiPWM__pwm_1.channel == PWMCh.PWM_1.value.channel
            assert pwm_dev._EdgePiPWM__pwm_1.chip == PWMCh.PWM_1.value.chip
            assert pwm_dev._EdgePiPWM__pwm_2 is None
        else:
            assert pwm_dev._EdgePiPWM__pwm_2.channel == PWMCh.PWM_2.value.channel
            assert pwm_dev._EdgePiPWM__pwm_2.chip == PWMCh.PWM_2.value.chip
            assert pwm_dev._EdgePiPWM__pwm_1 is None
        mock_open.assert_called_once()

@pytest.mark.parametrize("pwm_num,error", 
                         [(PWMPins.PWM1,does_not_raise()),
                          (PWMPins.PWM2,does_not_raise()),
                          (None, pytest.raises(ValueError)),
                        ])
def test_init_pwm_first_time(mocker, pwm_num,error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    mock_open = mocker.patch("edgepi.peripherals.pwm.PwmDevice.open_pwm")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    with error:
        pwm_dev.init_pwm(pwm_num)
        assert mock_open.call_count == 0
