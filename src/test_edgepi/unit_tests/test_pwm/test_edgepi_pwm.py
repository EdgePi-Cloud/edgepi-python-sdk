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
from edgepi.pwm.edgepi_pwm import EdgePiPWM, PwmDeviceError

@pytest.fixture(name="pwm_dev")
def fixture_test_pwm(mocker):
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev = EdgePiPWM()
    yield pwm_dev

def test_pwm_init(mocker):
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO")
    pwm_dev = EdgePiPWM()
    assert pwm_dev._EdgePiPWM__pwm_1 == None
    assert pwm_dev._EdgePiPWM__pwm_2 == None

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
    "pwm_num, mock_vals, result, error",
    [
        (PWMPins.PWM1, [False], [GpioPins.AO_EN1.value, GpioPins.DOUT1.value],does_not_raise()),
        (PWMPins.PWM2, [False], [GpioPins.AO_EN2.value, GpioPins.DOUT2.value],does_not_raise()),
        (PWMPins.PWM1, [True], [GpioPins.AO_EN1.value, GpioPins.DOUT1.value],does_not_raise()),
        (PWMPins.PWM2, [True], [GpioPins.AO_EN2.value, GpioPins.DOUT2.value],does_not_raise()),
        (None, [True], [GpioPins.AO_EN2.value, GpioPins.DOUT2.value], pytest.raises(ValueError)),
    ],
)
def test_pwm_enable(mocker, pwm_num, mock_vals, result, error, pwm_dev):
    mock_pwmdevice = mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    mocker_gpio = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    pwm_dev.gpio = mocker_gpio
    mock_clear_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.clear_pin_state")
    mock_set_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.set_pin_state")
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM.get_enabled", return_value = mock_vals[0])
    mock_disable = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM.disable")
    with error:
        pwm_dev.enable(pwm_num)
        if mock_vals[0]:
            mock_disable.assert_called_once_with(pwm_num)
            if pwm_num == PWMPins.PWM1:
                pwm_dev._EdgePiPWM__pwm_1.enable_pwm.assert_called_once_with()
            else:
                pwm_dev._EdgePiPWM__pwm_2.enable_pwm.assert_called_once_with()
        mock_set_pin.assert_called_with(result[0])
        mock_clear_pin.assert_has_calls([mock.call(result[1]), mock.call(pwm_num.value)])

@pytest.mark.parametrize("pwm_num, error",
                         [(PWMPins.PWM1, does_not_raise()),
                          (PWMPins.PWM2, does_not_raise()),
                          (None, pytest.raises(ValueError)),
                          ])
def test_pwm_disable(mocker, pwm_num, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    mocker_gpio = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev.gpio = mocker_gpio
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.disable_pwm")
    mock_set_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.set_pin_state")
    with error:
        pwm_dev.disable(pwm_num)
        if pwm_num == PWMPins.PWM1:
            pwm_dev._EdgePiPWM__pwm_1.disable_pwm.assert_called_once_with()
        else:
            pwm_dev._EdgePiPWM__pwm_2.disable_pwm.assert_called_once_with()
        mock_set_pin.assert_called_with(pwm_num.value)

@pytest.mark.parametrize("pwm_num, expected, error",
                         [(PWMPins.PWM1, True, does_not_raise()),
                          (PWMPins.PWM2, False, does_not_raise()),
                          (None, False, pytest.raises(ValueError)),
                          ])
def test_get_enabled(mocker, pwm_num, expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_enabled_pwm", return_value = expected)
    with error:
        enabled = pwm_dev.get_enabled(pwm_num)
        assert enabled == expected

@pytest.mark.parametrize("pwm_num, error",
                         [(PWMPins.PWM1, does_not_raise()),
                          (PWMPins.PWM2, does_not_raise()),
                          (None, pytest.raises(ValueError)),
                          ])
def test_pwm_close(mocker, pwm_num, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    with error:
        pwm_dev.close(pwm_num)
        if pwm_num == PWMPins.PWM1:
            pwm_dev._EdgePiPWM__pwm_1.close_pwm.assert_called_once()
        else:
            pwm_dev._EdgePiPWM__pwm_2.close_pwm.assert_called_once()

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
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
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
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_frequency_pwm", return_value = freq)
    with error:
        pwm_dev._EdgePiPWM__set_frequency(pwm_num, freq)
        result = pwm_dev.get_frequency(pwm_num)
        if pwm_num == PWMPins.PWM1:
            pwm_dev._EdgePiPWM__pwm_1.set_frequency_pwm.assert_called_once_with(freq)
        else:
            pwm_dev._EdgePiPWM__pwm_2.set_frequency_pwm.assert_called_once_with(freq)
        assert result == freq

@pytest.mark.parametrize("pwm_num ,expected, error",
                         [(PWMPins.PWM1,50,does_not_raise()),
                          (PWMPins.PWM1, 40, does_not_raise()),
                          (PWMPins.PWM1, 30, does_not_raise()),
                          (PWMPins.PWM1, 20, does_not_raise()),
                          (PWMPins.PWM1, 10, does_not_raise()),
                          (PWMPins.PWM1, 60, does_not_raise()),
                          (PWMPins.PWM1, 70, does_not_raise()),
                          (PWMPins.PWM1, 80, does_not_raise()),
                          (PWMPins.PWM1, 90, does_not_raise()),
                          (PWMPins.PWM1, 100, does_not_raise()),
                          (PWMPins.PWM2,50,does_not_raise()),
                          (PWMPins.PWM2, 40, does_not_raise()),
                          (PWMPins.PWM2, 30, does_not_raise()),
                          (PWMPins.PWM2, 20, does_not_raise()),
                          (PWMPins.PWM2, 10, does_not_raise()),
                          (PWMPins.PWM2, 60, does_not_raise()),
                          (PWMPins.PWM2, 70, does_not_raise()),
                          (PWMPins.PWM2, 80, does_not_raise()),
                          (PWMPins.PWM2, 90, does_not_raise()),
                          (PWMPins.PWM2, 100, does_not_raise()),
                          (None, 50, pytest.raises(ValueError))
                          ])
def test_get_duty_cycle_pwm(mocker, pwm_num ,expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_duty_cycle_pwm", return_value = expected/100)
    with error:
        duty_cycle = pwm_dev.get_duty_cycle(pwm_num)
        assert duty_cycle == expected

@pytest.mark.parametrize("pwm_num ,duty_cycle, error",
                         [(PWMPins.PWM1,50,does_not_raise()),
                          (PWMPins.PWM1, 40, does_not_raise()),
                          (PWMPins.PWM1, 30, does_not_raise()),
                          (PWMPins.PWM1, 20, does_not_raise()),
                          (PWMPins.PWM1, 10, does_not_raise()),
                          (PWMPins.PWM1, 60, does_not_raise()),
                          (PWMPins.PWM1, 70, does_not_raise()),
                          (PWMPins.PWM1, 80, does_not_raise()),
                          (PWMPins.PWM1, 90, does_not_raise()),
                          (PWMPins.PWM1, 100, does_not_raise()),
                          (PWMPins.PWM2,50,does_not_raise()),
                          (PWMPins.PWM2, 40, does_not_raise()),
                          (PWMPins.PWM2, 30, does_not_raise()),
                          (PWMPins.PWM2, 20, does_not_raise()),
                          (PWMPins.PWM2, 10, does_not_raise()),
                          (PWMPins.PWM2, 60, does_not_raise()),
                          (PWMPins.PWM2, 70, does_not_raise()),
                          (PWMPins.PWM2, 80, does_not_raise()),
                          (PWMPins.PWM2, 90, does_not_raise()),
                          (PWMPins.PWM2, 100, does_not_raise()),
                          (None, 60, pytest.raises(ValueError))
                          ])
def test_set_duty_cycle_pwm(mocker, pwm_num, duty_cycle, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_duty_cycle_pwm", return_value = duty_cycle/100)
    with error:
        pwm_dev._EdgePiPWM__set_duty_cycle(pwm_num, duty_cycle)
        result = pwm_dev.get_duty_cycle(pwm_num)
        if pwm_num == PWMPins.PWM1:
            pwm_dev._EdgePiPWM__pwm_1.set_duty_cycle_pwm.assert_called_once_with(duty_cycle/100)
        else:
            pwm_dev._EdgePiPWM__pwm_2.set_duty_cycle_pwm.assert_called_once_with(duty_cycle/100)
        assert result == duty_cycle

@pytest.mark.parametrize("pwm_num ,expected, error",
                         [(PWMPins.PWM1, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM1, Polarity.INVERSED,does_not_raise()),
                          (PWMPins.PWM2, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM2, Polarity.INVERSED,does_not_raise()),
                          (None, Polarity.INVERSED,pytest.raises(ValueError)),
                          ])
def test_get_polarity_pwm(mocker, pwm_num, expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_polarity_pwm", return_value = expected.value)
    with error:
        polarity = pwm_dev.get_polarity(pwm_num)
        assert polarity == expected.value

@pytest.mark.parametrize("pwm_num ,expected, error",
                         [(PWMPins.PWM1, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM1, Polarity.INVERSED,does_not_raise()),
                          (PWMPins.PWM2, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM2, Polarity.INVERSED,does_not_raise()),
                          (None, Polarity.INVERSED,pytest.raises(ValueError)),
                          ])
def test__set_polarity_pwm(mocker, pwm_num, expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_polarity_pwm", return_value = expected.value)
    with error:
        pwm_dev._EdgePiPWM__set_polarity(pwm_num, expected)
        result = pwm_dev.get_polarity(pwm_num)
        if pwm_num == PWMPins.PWM1:
            pwm_dev._EdgePiPWM__pwm_1.set_polarity_pwm.assert_called_once_with(expected.value)
        else:
            pwm_dev._EdgePiPWM__pwm_2.set_polarity_pwm.assert_called_once_with(expected.value)
        assert result == expected.value

@pytest.mark.parametrize("pwm_num, expected, error",
                         [(PWMPins.PWM1, True, does_not_raise()),
                          (PWMPins.PWM2, False, does_not_raise()),
                          (None, False, pytest.raises(ValueError)),
                          ])
def test_get_enabled(mocker, pwm_num, expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if pwm_num == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_enabled_pwm", return_value = expected)
    with error:
        enabled = pwm_dev.get_enabled(pwm_num)
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

@pytest.mark.parametrize("pwm_num, error", 
                        [(None, pytest.raises(ValueError)),
                          (PWMPins.PWM1, pytest.raises(PwmDeviceError)),
                          (PWMPins.PWM2, pytest.raises(PwmDeviceError)),
                        ])
def test_set_config_errors(pwm_num, error, pwm_dev):
    with error:
        pwm_dev.set_config(pwm_num)

@pytest.mark.parametrize("params, mock_vals", 
                        [
                          ([PWMPins.PWM1, 1000, 50, Polarity.NORMAL],[1000, 50, Polarity.NORMAL]),
                          ([PWMPins.PWM1, 1000, 50, Polarity.NORMAL],[2000, 50, Polarity.NORMAL]),
                          ([PWMPins.PWM1, 1000, 50, Polarity.NORMAL],[1000, 60, Polarity.NORMAL]),
                          ([PWMPins.PWM1, 1000, 50, Polarity.NORMAL],[1000, 50, Polarity.INVERSED]),
                          ([PWMPins.PWM2, 1000, 50, Polarity.NORMAL],[1000, 50, Polarity.NORMAL]),
                          ([PWMPins.PWM2, 1000, 50, Polarity.NORMAL],[2000, 50, Polarity.NORMAL]),
                          ([PWMPins.PWM2, 1000, 50, Polarity.NORMAL],[1000, 60, Polarity.NORMAL]),
                          ([PWMPins.PWM2, 1000, 50, Polarity.NORMAL],[1000, 50, Polarity.INVERSED]),
                        ])
def test_set_config(mocker, params, mock_vals, pwm_dev):
    # mock getter function
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM.get_frequency", return_value = mock_vals[0])
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM.get_duty_cycle", return_value = mock_vals[1]/100)
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM.get_polarity", return_value = mock_vals[2].value)
    # mock setter function
    mock_set_freq = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM._EdgePiPWM__set_frequency")
    mock_set_duty = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM._EdgePiPWM__set_duty_cycle")
    mock_set_pol = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM._EdgePiPWM__set_polarity")
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    if params[0] == PWMPins.PWM1:
        pwm_dev._EdgePiPWM__pwm_1 = mock_pwmdevice
    else:
        pwm_dev._EdgePiPWM__pwm_2 = mock_pwmdevice
    pwm_dev.set_config(params[0], params[1], params[2], params[3])
    if params[1] != mock_vals[0]:
        mock_set_freq.assert_called_once_with(params[0],params[1])
    if params[2] != mock_vals[1]:
            mock_set_duty.assert_called_once_with(params[0],params[2])
    if params[3] != mock_vals[2]:
            mock_set_pol.assert_called_once_with(params[0],params[3])
