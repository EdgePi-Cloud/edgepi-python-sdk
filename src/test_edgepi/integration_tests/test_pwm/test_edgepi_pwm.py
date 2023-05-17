"""EdgePi PWM integration test"""

import logging
import pytest

from edgepi.pwm.pwm_constants import PWMCh, Polarity, PWMPins
from edgepi.pwm.edgepi_pwm import EdgePiPWM

_logger = logging.getLogger(__name__)

@pytest.fixture(name="pwm_dev")
def fixture_test_pwm():
    pwm_dev = EdgePiPWM()
    yield pwm_dev

@pytest.fixture(name="pwm_dev_default")
def fixture_test_pwm():
    pwm_dev_default = EdgePiPWM()
    pwm_dev_default.init(PWMPins.PWM1)
    pwm_dev_default.set_config(PWMPins.PWM1, 1000, 50, Polarity.NORMAL)
    yield pwm_dev_default

@pytest.mark.parametrize("pwm_num",
                         [(PWMPins.PWM1),
                          (PWMPins.PWM2),
                          ])
def test_pwm_init(pwm_num, pwm_dev):
    pwm_dev.init_pwm(pwm_num)
    if pwm_num == PWMPins.PWM1:
        assert pwm_dev._EdgePiPWM__pwm_1 is not None
        assert pwm_dev._EdgePiPWM__pwm_2 is None
    else:
        assert pwm_dev._EdgePiPWM__pwm_1 is None
        assert pwm_dev._EdgePiPWM__pwm_2 is not None
    pwm_dev.close(pwm_num)

def test_get_frequency_pwm(pwm_dev_default):
    freq = pwm_dev_default.get_frequency(PWMPins.PWM1)
    assert freq == 1000
    pwm_dev_default.close(PWMPins.PWM1)

@pytest.mark.parametrize("freq", [(2000)])
def test_set_frequency_pwm(freq, pwm_dev_default):
    init_freq = pwm_dev_default.get_frequency(PWMPins.PWM1)
    pwm_dev_default.set_config(pwm_num = PWMPins.PWM1, frequency = freq)
    result = pwm_dev_default.get_frequency(PWMPins.PWM1)
    assert result != init_freq
    pwm_dev_default.close(PWMPins.PWM1)

def test_get_duty_cycle_pwm(pwm_dev_default):
    duty_cycle = pwm_dev_default.get_duty_cycle(PWMPins.PWM1)
    assert duty_cycle == 50
    pwm_dev_default.close(PWMPins.PWM1)

def test_set_duty_cycle_pwm(pwm_dev_default):
    init_duty_cycle = pwm_dev_default.get_duty_cycle(PWMPins.PWM1)
    pwm_dev_default.set_config(pwm_num = PWMPins.PWM1, duty_cycle=60)
    result = pwm_dev_default.get_duty_cycle(PWMPins.PWM1)
    assert result != init_duty_cycle
    pwm_dev_default.close(PWMPins.PWM1)

def test_get_polarity_pwm(pwm_dev_default):
    pol = pwm_dev_default.get_polarity(PWMPins.PWM1)
    assert pol == Polarity.NORMAL.value
    pwm_dev_default.close(PWMPins.PWM1)

def test_set_polarity_pwm(pwm_dev_default):
    init_pol = pwm_dev_default.get_polarity()
    pwm_dev_default.set_config(pwm_num = PWMPins.PWM1, polarity = Polarity.INVERSED)
    result = pwm_dev_default.get_polarity()
    assert result != init_pol
    pwm_dev_default.close(PWMPins.PWM1)

def test_enable(pwm_dev_default):
    pwm_dev_default.enable(PWMPins.PWM1)
    assert pwm_dev_default.get_enabled(PWMPins.PWM1) is True
    pwm_dev_default.close(PWMPins.PWM1)


def test_disable(pwm_dev_default):
    pwm_dev_default.disable(PWMPins.PWM1)
    assert pwm_dev_default.get_enabled(PWMPins.PWM1) is False
    pwm_dev_default.close(PWMPins.PWM1)
