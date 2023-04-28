"""unit tests for pwm.py module"""
# pylint: disable=wrong-import-position
from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
import pytest
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.pwm.pwm_constants import PWMCh, Polarity
from edgepi.pwm.edgepi_pwm import EdgePiPWM

@pytest.fixture(name="pwm_dev")
def fixture_test_dac(mocker):
    mocker_pwm= mocker.patch("edgepi.peripherals.pwm.PWM")
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev = EdgePiPWM(GpioPins.PWM1, 1000, 0.5, Polarity.NORMAL)
    pwm_dev.pwm = mocker_pwm
    yield pwm_dev


@pytest.mark.parametrize(
    "pwm_num, freq, duty_cycle, polarity, result",
    [
        (GpioPins.PWM1, 1000, 0.5, Polarity.NORMAL,
         [PWMCh.PWM_1.value.channel, PWMCh.PWM_1.value.chip, 1000, 0.5, Polarity.NORMAL]),
        (GpioPins.PWM2, 1000, 0.1, Polarity.INVERSED, 
         [PWMCh.PWM_2.value.channel, PWMCh.PWM_2.value.chip, 1000, 0.1, Polarity.INVERSED]),
    ],
)
def test_pwm_init(mocker, pwm_num, freq, duty_cycle, polarity, result):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiGPIO")
    pwm_dev = EdgePiPWM(pwm_num=pwm_num,freq=freq, duty_cycle=duty_cycle, polarity=polarity)
    mock_pwm.assert_called_once_with(result[1], result[0])
    assert pwm_dev.channel == result[0]
    assert pwm_dev.chip == result[1]
    assert pwm_dev.freq == result[2]
    assert pwm_dev.duty_cycle == result[3]
    assert pwm_dev.polarity == result[4].value

@pytest.mark.parametrize(
    "pwm_num, result",
    [
        (GpioPins.PWM1,[GpioPins.AO_EN1.value, GpioPins.DOUT1.value]),
        (GpioPins.PWM2, [GpioPins.AO_EN2.value, GpioPins.DOUT2.value]),
    ],
)
def test_pwm_enable(mocker, pwm_num, result):
    mocker_pwm= mocker.patch("edgepi.peripherals.pwm.PWM")
    mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO")
    pwm_dev = EdgePiPWM(GpioPins.PWM1, 1000, 0.5, Polarity.NORMAL)
    pwm_dev.pwm = mocker_pwm
    mock_enable_pwm = mocker.patch("edgepi.peripherals.pwm.PWM.enable")
    mock_clear_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.clear_pin_state")
    mock_set_pin = mocker.patch("edgepi.pwm.edgepi_pwm.EdgePiGPIO.set_pin_state")
    pwm_dev.enable()
    mock_enable_pwm.assert_called_once()
    mock_set_pin.assert_called_with(result[0])
    mock_clear_pin.assert_has_calls([result[1], pwm_num.value])


def test_pwm_disable(mocker, pwm_dev):
    mock_disable_pwm = mocker.patch("edgepi.peripherals.pwm.PWM.disable")
    pwm_dev.disable()
    mock_disable_pwm.assert_called_once()

def test_pwm_close(mocker, pwm_dev):
    mock_close_pwm = mocker.patch("edgepi.peripherals.pwm.PWM.close")
    pwm_dev.close()
    mock_close_pwm.assert_called_once()

@pytest.mark.parametrize("expected", [(1000), (5000), (10000)])
def test_get_frequency_pwm(mocker, expected, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PWM.frequency", return_value = expected)
    freq = pwm_dev.get_frequency()
    assert freq.return_value == expected

@pytest.mark.parametrize("freq", [(1000)])
def test_set_frequency_pwm(freq, pwm_dev):
    pwm_dev.set_frequency(freq)
    result = pwm_dev.get_frequency()
    assert result == freq

@pytest.mark.parametrize("expected", [(0.5),(0.4),(0.3),(0.2),(0.1),(0.6),(0.7),(0.8),(0.9),(1)])
def test_get_duty_cycle_pwm(mocker,expected, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PWM.duty_cycle", return_value = expected)
    dc = pwm_dev.get_dutycycle()
    assert dc.return_value == expected

@pytest.mark.parametrize("duty_cycle", [(0.5),(0.4),(0.3),(0.2),(0.1),(0.6),(0.7),(0.8),(0.9),(1)])
def test_set_duty_cycle_pwm(duty_cycle, pwm_dev):
    pwm_dev.set_dutycycle(duty_cycle)
    result = pwm_dev.get_dutycycle()
    assert result == duty_cycle

@pytest.mark.parametrize("expected", [(Polarity.NORMAL),(Polarity.INVERSED)])
def test_get_polarity_pwm(mocker, expected, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PWM.polarity", return_value = expected)
    pol = pwm_dev.get_polarity()
    assert pol.return_value == expected

@pytest.mark.parametrize("polarity", [(Polarity.NORMAL),(Polarity.INVERSED)])
def test_set_polarity_pwm(polarity, pwm_dev):
    pwm_dev.set_polarity(polarity)
    result = pwm_dev.get_polarity()
    assert result == polarity

@pytest.mark.parametrize("expected", [(True),(False)])
def test_get_enabled_pwm(mocker, expected, pwm_dev):
    mocker.patch("edgepi.peripherals.pwm.PWM.enabled", return_value = expected)
    enabled = pwm_dev.get_enabled()
    assert enabled.return_value == expected