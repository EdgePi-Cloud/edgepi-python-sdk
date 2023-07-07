"""unit tests for pwm.py module"""
# pylint: disable=wrong-import-position
from unittest import mock
import sys
if sys.platform != 'linux':
    sys.modules['periphery'] = mock.MagicMock()
import pytest
from edgepi.peripherals.pwm import PwmDevice
from edgepi.pwm.pwm_constants import Polarity

@pytest.fixture(name="pwm_dev")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.pwm.PWM")
    pwm_dev = PwmDevice(0, 1)
    yield pwm_dev


@pytest.mark.parametrize(
    "chip, channel, result",
    [
        (0, 1, [0, 1, None]),
        (0, 0, [0, 0, None]),
    ],
)
def test_pwm_init(chip, channel, result):
    pwm_dev = PwmDevice(chip=chip, channel=channel)
    assert pwm_dev.chip == result[0]
    assert pwm_dev.channel == result[1]
    assert pwm_dev.pwm == result[2]

def test_pwm_open(mocker, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    pwm_dev.open_pwm()
    mock_pwm.assert_called_once_with(0, 1)

def test_pwm_enable(mocker, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mock_enable_pwm = mocker.patch("edgepi.peripherals.pwm.PWM.enable")
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    pwm_dev.enable_pwm()
    mock_pwm.assert_called_once_with(0, 1)
    mock_enable_pwm.assert_called_once()

def test_pwm_disable(mocker, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mock_disable_pwm = mocker.patch("edgepi.peripherals.pwm.PWM.disable")
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    pwm_dev.disable_pwm()
    mock_pwm.assert_called_once_with(0, 1)
    mock_disable_pwm.assert_called_once()

def test_pwm_close(mocker, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mock_close_pwm = mocker.patch("edgepi.peripherals.pwm.PWM.close")
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    pwm_dev.close_pwm()
    mock_pwm.assert_called_once_with(0, 1)
    mock_close_pwm.assert_called_once()

@pytest.mark.parametrize("expected", [(1000)])
def test_get_frequency_pwm(mocker, expected, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mocker.patch("edgepi.peripherals.pwm.PWM.frequency", return_value = expected)
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    mock_pwm.assert_called_once_with(0, 1)
    freq = pwm_dev.get_frequency_pwm()
    assert freq.return_value == expected

@pytest.mark.parametrize("freq", [(1000.0)])
def test_set_frequency_pwm(mocker, freq, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    mock_pwm.assert_called_once_with(0, 1)
    pwm_dev.set_frequency_pwm(freq)
    result = pwm_dev.get_frequency_pwm()
    assert result == freq

@pytest.mark.parametrize("expected", [(0.5),(0.4),(0.3),(0.2),(0.1),(0.6),(0.7),(0.8),(0.9),(1)])
def test_get_duty_cycle_pwm(mocker, expected, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mocker.patch("edgepi.peripherals.pwm.PWM.duty_cycle", return_value = expected)
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    mock_pwm.assert_called_once_with(0, 1)
    duty_cycle = pwm_dev.get_duty_cycle_pwm()
    assert duty_cycle.return_value == expected

@pytest.mark.parametrize("duty_cycle", [(0.5),(0.4),(0.3),(0.2),(0.1),(0.6),(0.7),(0.8),(0.9),(1)])
def test_set_duty_cycle_pwm(mocker, duty_cycle, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    mock_pwm.assert_called_once_with(0, 1)
    pwm_dev.set_duty_cycle_pwm(duty_cycle)
    result = pwm_dev.get_duty_cycle_pwm()
    assert result == duty_cycle

@pytest.mark.parametrize("expected", [("normal"),("inversed")])
def test_get_polarity_pwm(mocker, expected, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mocker.patch.object(mock_pwm, "polarity", expected)
    # mocker.patch("edgepi.peripherals.pwm.PWM.polarity", return_value = expected)
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    mock_pwm.assert_called_once_with(0, 1)
    pol = pwm_dev.get_polarity_pwm()
    assert pol == Polarity[expected.upper()]

# @pytest.mark.parametrize("polarity", [("normal"),("inversed")])
# def test_set_polarity_pwm(mocker, polarity, pwm_dev):
#     mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
#     pwm_dev.open_pwm()
#     pwm_dev.pwm = mock_pwm
#     mock_pwm.assert_called_once_with(0, 1)
#     pwm_dev.set_polarity_pwm(polarity)
#     result = pwm_dev.get_polarity_pwm()
#     assert result == polarity

@pytest.mark.parametrize("expected", [(True),(False)])
def test_get_enabled_pwm(mocker, expected, pwm_dev):
    mock_pwm = mocker.patch("edgepi.peripherals.pwm.PWM")
    mocker.patch("edgepi.peripherals.pwm.PWM.enabled", return_value = expected)
    pwm_dev.open_pwm()
    pwm_dev.pwm = mock_pwm
    mock_pwm.assert_called_once_with(0, 1)
    enabled = pwm_dev.get_enabled_pwm()
    assert enabled.return_value == expected
