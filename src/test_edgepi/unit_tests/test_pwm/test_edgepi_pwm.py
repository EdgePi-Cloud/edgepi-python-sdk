"""unit tests for pwm.py module"""
# pylint: disable=wrong-import-position
# pylint: disable=protected-access
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
    assert pwm_dev._EdgePiPWM__pwm_devs[PWMPins.PWM1] is None
    assert pwm_dev._EdgePiPWM__pwm_devs[PWMPins.PWM2] is None

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
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    pwm_dev.gpio = mocker_gpio
    mock_clear_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.clear_pin_state")
    mock_set_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.set_pin_state")
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM.get_enabled", return_value = mock_vals[0])
    mock_disable = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM.disable")
    with error:
        pwm_dev.enable(pwm_num)
        if mock_vals[0]:
            mock_disable.assert_called_once_with(pwm_num)
            pwm_dev._EdgePiPWM__pwm_devs[pwm_num].enable_pwm.assert_called_once_with()
        mock_set_pin.assert_called_with(result[0])
        mock_clear_pin.assert_has_calls([mock.call(result[1]), mock.call(pwm_num.value)])

@pytest.mark.parametrize("pwm_num, pins, error",
                    [(PWMPins.PWM1,[GpioPins.AO_EN1.value, GpioPins.DOUT1.value], does_not_raise()),
                     (PWMPins.PWM2,[GpioPins.AO_EN2.value, GpioPins.DOUT2.value], does_not_raise()),
                     (None, None, pytest.raises(ValueError)),
                     ])
def test_pwm_disable(mocker, pwm_num, pins, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    mocker_gpio = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev.gpio = mocker_gpio
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.disable_pwm")
    mock_set_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.set_pin_state")
    mock_clear_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.clear_pin_state")
    with error:
        pwm_dev.disable(pwm_num)
        pwm_dev._EdgePiPWM__pwm_devs[pwm_num].disable_pwm.assert_called_once_with()
        mock_set_pin.assert_called_with(pins[0])
        mock_clear_pin.assert_has_calls([mock.call(pins[1]), mock.call(pwm_num.value)])

@pytest.mark.parametrize("pwm_num, error",
                         [(PWMPins.PWM1, does_not_raise()),
                          (PWMPins.PWM2, does_not_raise()),
                          (None, pytest.raises(ValueError)),
                          ])
def test_pwm_close(mocker, pwm_num, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    with error:
        pwm_dev.close(pwm_num)
        mock_pwmdevice.close_pwm.assert_called_once()
        assert pwm_dev._EdgePiPWM__pwm_devs[pwm_num] is None


@pytest.mark.parametrize("pwm_num ,expected, error",
                         [(PWMPins.PWM1, 1000.0, does_not_raise()),
                          (PWMPins.PWM1, 5000.0, does_not_raise()),
                          (PWMPins.PWM1, 10000.0, does_not_raise()),
                          (PWMPins.PWM2, 1000.0, does_not_raise()),
                          (PWMPins.PWM2, 5000.0, does_not_raise()),
                          (PWMPins.PWM2, 10000.0, does_not_raise()),
                          (None, 1000.0, pytest.raises(ValueError)),
                          (None, 5000.0, pytest.raises(ValueError)),
                          (None, 10000.0, pytest.raises(ValueError)),
                          ])
def test_get_frequency_pwm(mocker, pwm_num,expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_frequency_pwm", return_value = expected)
    with error:
        freq = pwm_dev.get_frequency(pwm_num)
        assert freq == expected

@pytest.mark.parametrize("pwm_num ,freq, error",
                         [(PWMPins.PWM1, 1000.0, does_not_raise()),
                          (PWMPins.PWM1, 5000.0, does_not_raise()),
                          (PWMPins.PWM1, 10000.0, does_not_raise()),
                          (PWMPins.PWM2, 1000.0, does_not_raise()),
                          (PWMPins.PWM2, 5000.0, does_not_raise()),
                          (PWMPins.PWM2, 10000.0, does_not_raise()),
                          (None, 1000.0, pytest.raises(ValueError)),
                          (None, 5000.0, pytest.raises(ValueError)),
                          (None, 10000.0, pytest.raises(ValueError)),
                          ])
def test_set_frequency_pwm(mocker, pwm_num, freq, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_frequency_pwm", return_value = freq)
    with error:
        pwm_dev._EdgePiPWM__set_frequency(pwm_num, freq)
        result = pwm_dev.get_frequency(pwm_num)
        pwm_dev._EdgePiPWM__pwm_devs[pwm_num].set_frequency_pwm.assert_called_once_with(freq)
        assert result == freq

@pytest.mark.parametrize("pwm_num ,expected, error",
                         [(PWMPins.PWM1, 0.50, does_not_raise()),
                          (PWMPins.PWM1, 0.40, does_not_raise()),
                          (PWMPins.PWM1, 0.30, does_not_raise()),
                          (PWMPins.PWM1, 0.20, does_not_raise()),
                          (PWMPins.PWM1, 0.10, does_not_raise()),
                          (PWMPins.PWM1, 0.60, does_not_raise()),
                          (PWMPins.PWM1, 0.70, does_not_raise()),
                          (PWMPins.PWM1, 0.80, does_not_raise()),
                          (PWMPins.PWM1, 0.90, does_not_raise()),
                          (PWMPins.PWM1, 1.00, does_not_raise()),
                          (PWMPins.PWM2, 0.50, does_not_raise()),
                          (PWMPins.PWM2, 0.40, does_not_raise()),
                          (PWMPins.PWM2, 0.30, does_not_raise()),
                          (PWMPins.PWM2, 0.20, does_not_raise()),
                          (PWMPins.PWM2, 0.10, does_not_raise()),
                          (PWMPins.PWM2, 0.60, does_not_raise()),
                          (PWMPins.PWM2, 0.70, does_not_raise()),
                          (PWMPins.PWM2, 0.80, does_not_raise()),
                          (PWMPins.PWM2, 0.90, does_not_raise()),
                          (PWMPins.PWM2, 1.00, does_not_raise()),
                          (None, 0.50, pytest.raises(ValueError))
                          ])
def test_get_duty_cycle_pwm(mocker, pwm_num ,expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_duty_cycle_pwm", return_value = expected)
    with error:
        duty_cycle = pwm_dev.get_duty_cycle(pwm_num)
        assert duty_cycle == expected

@pytest.mark.parametrize("pwm_num ,duty_cycle, error",
                         [(PWMPins.PWM1, 0.50, does_not_raise()),
                          (PWMPins.PWM1, 0.40, does_not_raise()),
                          (PWMPins.PWM1, 0.30, does_not_raise()),
                          (PWMPins.PWM1, 0.20, does_not_raise()),
                          (PWMPins.PWM1, 0.10, does_not_raise()),
                          (PWMPins.PWM1, 0.60, does_not_raise()),
                          (PWMPins.PWM1, 0.70, does_not_raise()),
                          (PWMPins.PWM1, 0.80, does_not_raise()),
                          (PWMPins.PWM1, 0.90, does_not_raise()),
                          (PWMPins.PWM1, 1.0, does_not_raise()),
                          (PWMPins.PWM2, 0.50, does_not_raise()),
                          (PWMPins.PWM2, 0.40, does_not_raise()),
                          (PWMPins.PWM2, 0.30, does_not_raise()),
                          (PWMPins.PWM2, 0.20, does_not_raise()),
                          (PWMPins.PWM2, 0.10, does_not_raise()),
                          (PWMPins.PWM2, 0.60, does_not_raise()),
                          (PWMPins.PWM2, 0.70, does_not_raise()),
                          (PWMPins.PWM2, 0.80, does_not_raise()),
                          (PWMPins.PWM2, 0.90, does_not_raise()),
                          (PWMPins.PWM2, 1.0, does_not_raise()),
                          (None, 0.60, pytest.raises(ValueError))
                          ])
def test_set_duty_cycle_pwm(mocker, pwm_num, duty_cycle, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_duty_cycle_pwm",
                 return_value = duty_cycle)
    with error:
        pwm_dev._EdgePiPWM__set_duty_cycle(pwm_num, duty_cycle)
        result = pwm_dev.get_duty_cycle(pwm_num)
        # pylint: disable=line-too-long
        pwm_dev._EdgePiPWM__pwm_devs[pwm_num].set_duty_cycle_pwm.assert_called_once_with(duty_cycle)
        assert result == duty_cycle

@pytest.mark.parametrize("pwm_num, expected, error",
                         [(PWMPins.PWM1, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM1, Polarity.INVERSED,does_not_raise()),
                          (PWMPins.PWM2, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM2, Polarity.INVERSED,does_not_raise()),
                          (None, Polarity.INVERSED,pytest.raises(ValueError)),
                          ])
def test_get_polarity_pwm(mocker, pwm_num, expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_polarity_pwm", return_value = expected)
    with error:
        polarity = pwm_dev.get_polarity(pwm_num)
        assert polarity == expected

@pytest.mark.parametrize("pwm_num, expected, error",
                         [(PWMPins.PWM1, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM1, Polarity.INVERSED,does_not_raise()),
                          (PWMPins.PWM2, Polarity.NORMAL,does_not_raise()),
                          (PWMPins.PWM2, Polarity.INVERSED,does_not_raise()),
                          (None, Polarity.INVERSED,pytest.raises(ValueError)),
                          ])
def test__set_polarity_pwm(mocker, pwm_num, expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_polarity_pwm", return_value = expected)
    with error:
        pwm_dev._EdgePiPWM__set_polarity(pwm_num, expected)
        result = pwm_dev.get_polarity(pwm_num)
        # pylint: disable=line-too-long
        pwm_dev._EdgePiPWM__pwm_devs[pwm_num].set_polarity_pwm.assert_called_once_with(expected)
        assert result == expected

@pytest.mark.parametrize("pwm_num, expected, error",
                         [(PWMPins.PWM1, True, does_not_raise()),
                          (PWMPins.PWM2, False, does_not_raise()),
                          (None, False, pytest.raises(ValueError)),
                          ])
def test_get_enabled(mocker, pwm_num, expected, error, pwm_dev):
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[pwm_num] = mock_pwmdevice
    mocker.patch("edgepi.peripherals.pwm.PwmDevice.get_enabled_pwm", return_value = expected)
    with error:
        enabled = pwm_dev.get_enabled(pwm_num)
        assert enabled == expected

@pytest.mark.parametrize("pwm_num, result",
                         [(PWMPins.PWM1, [PWMCh.PWM_1.value.channel, PWMCh.PWM_1.value.chip]),
                          (PWMPins.PWM2, [PWMCh.PWM_2.value.channel, PWMCh.PWM_2.value.chip]),
                        ])
def test__init_pwm_dev(mocker, pwm_num, result, pwm_dev):
    mock_open = mocker.patch("edgepi.peripherals.pwm.PwmDevice.open_pwm")
    pwm_dev._EdgePiPWM__init_pwm_dev(pwm_num)
    assert pwm_dev._EdgePiPWM__pwm_devs[pwm_num].channel == result[0]
    assert pwm_dev._EdgePiPWM__pwm_devs[pwm_num].chip == result[1]
    mock_open.assert_called_once()

@pytest.mark.parametrize("pwm_num,error",
                         [(PWMPins.PWM1,does_not_raise()),
                          (PWMPins.PWM2,does_not_raise()),
                          (None, pytest.raises(ValueError)),
                        ])
def test_init_pwm_first_time(mocker, pwm_num,error):
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev = EdgePiPWM()
    pwm_dev._EdgePiPWM__pwm_devs[PWMPins.PWM1] = None
    pwm_dev._EdgePiPWM__pwm_devs[PWMPins.PWM2] = None
    mock_open = mocker.patch("edgepi.peripherals.pwm.PwmDevice.open_pwm")
    with error:
        pwm_dev.init_pwm(pwm_num)
        if pwm_num == PWMPins.PWM1:
            assert pwm_dev._EdgePiPWM__pwm_devs[pwm_num].channel == PWMCh.PWM_1.value.channel
            assert pwm_dev._EdgePiPWM__pwm_devs[pwm_num].chip == PWMCh.PWM_1.value.chip
            assert pwm_dev._EdgePiPWM__pwm_devs[PWMPins.PWM2] is None
        if pwm_num == PWMPins.PWM2:
            assert pwm_dev._EdgePiPWM__pwm_devs[pwm_num].channel == PWMCh.PWM_2.value.channel
            assert pwm_dev._EdgePiPWM__pwm_devs[pwm_num].chip == PWMCh.PWM_2.value.chip
            assert pwm_dev._EdgePiPWM__pwm_devs[PWMPins.PWM1] is None
        mock_open.assert_called_once()


@pytest.mark.parametrize("pwm_num, error",
                        [(None, pytest.raises(ValueError)),
                          (PWMPins.PWM1, pytest.raises(PwmDeviceError)),
                          (PWMPins.PWM2, pytest.raises(PwmDeviceError)),
                        ])
def test_set_config_errors(mocker, pwm_num, error):
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev = EdgePiPWM()
    with error:
        pwm_dev.set_config(pwm_num)

@pytest.mark.parametrize("params",
                        [
                          ([PWMPins.PWM1, 1000.0, 0.5, Polarity.NORMAL]),
                          ([PWMPins.PWM1, None, 0.5, Polarity.NORMAL]),
                          ([PWMPins.PWM1, 1000.0, None, Polarity.NORMAL]),
                          ([PWMPins.PWM1, 1000.0, 0.5, None]),
                          ([PWMPins.PWM2, None, None, Polarity.NORMAL]),
                          ([PWMPins.PWM2, 1000.0, None, None]),
                          ([PWMPins.PWM2, None, None, None]),
                          ([PWMPins.PWM2, 1000.0, 0.5, Polarity.NORMAL]),
                        ])
def test_set_config(mocker, params, pwm_dev):
    # mock setter function
    mock_set_freq = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM._EdgePiPWM__set_frequency")
    mock_set_duty = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM._EdgePiPWM__set_duty_cycle")
    mock_set_pol = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiPWM._EdgePiPWM__set_polarity")
    mock_pwmdevice= mocker.patch("edgepi.peripherals.pwm.PwmDevice")
    pwm_dev._EdgePiPWM__pwm_devs[params[0]] = mock_pwmdevice
    pwm_dev.set_config(params[0], params[1], params[2], params[3])
    if params[1] is not None:
        mock_set_freq.assert_called_once_with(params[0],params[1])
    else:
        assert mock_set_freq.call_count == 0
    if params[2] is not None:
        mock_set_duty.assert_called_once_with(params[0],params[2])
    else:
        assert mock_set_duty.call_count == 0
    if params[3] is not None:
        mock_set_pol.assert_called_once_with(params[0],params[3])
    else:
        assert mock_set_pol.call_count == 0
