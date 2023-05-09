"""EdgePi PWM integration test"""

import logging
import pytest

from edgepi.gpio.gpio_constants import GpioPins
from edgepi.pwm.pwm_constants import PWMCh, Polarity
from edgepi.pwm.edgepi_pwm import EdgePiPWM

_logger = logging.getLogger(__name__)

@pytest.fixture(name="pwm_dev")
def fixture_test_pwm():
    pwm_dev = EdgePiPWM(GpioPins.PWM1)
    pwm_dev.set_frequency(1000)
    pwm_dev.set_duty_cycle(0.5)
    pwm_dev.set_polarity(Polarity.NORMAL)
    yield pwm_dev

@pytest.mark.parametrize(
    "pwm_num, result",
    [
        (GpioPins.PWM1,
         [PWMCh.PWM_1.value.channel, PWMCh.PWM_1.value.chip]),
        (GpioPins.PWM2, 
         [PWMCh.PWM_2.value.channel, PWMCh.PWM_2.value.chip]),
    ],
)
def test_pwm_init(pwm_num, result):
    pwm_dev = EdgePiPWM(pwm_num=pwm_num)
    assert pwm_dev.channel == result[0]
    assert pwm_dev.chip == result[1]
    pwm_dev.close()

def test_get_frequency_pwm(pwm_dev):
    freq = pwm_dev.get_frequency()
    assert freq == 1000
    pwm_dev.close()

@pytest.mark.parametrize("freq", [(2000)])
def test_set_frequency_pwm(freq, pwm_dev):
    init_freq = pwm_dev.get_frequency()
    pwm_dev.set_frequency(freq)
    result = pwm_dev.get_frequency()
    assert result != init_freq
    pwm_dev.close()

def test_get_duty_cycle_pwm(pwm_dev):
    dc = pwm_dev.get_duty_cycle()
    assert dc == 0.5
    pwm_dev.close()

def test_set_duty_cycle_pwm(pwm_dev):
    init_duty_cycle = pwm_dev.get_duty_cycle()
    pwm_dev.set_duty_cycle(0.6)
    result = pwm_dev.get_duty_cycle()
    assert result != init_duty_cycle
    pwm_dev.close()

def test_get_polarity_pwm(pwm_dev):
    pol = pwm_dev.get_polarity()
    assert pol == Polarity.NORMAL.value
    pwm_dev.close()

def test_set_polarity_pwm(pwm_dev):
    init_pol = pwm_dev.get_polarity()
    pwm_dev.set_polarity(Polarity.INVERSED)
    result = pwm_dev.get_polarity()
    assert result != init_pol
    pwm_dev.close()

def test_enable(pwm_dev):
    pwm_dev.enable()
    assert pwm_dev.get_enabled() == True
    pwm_dev.close()


def test_disable(pwm_dev):
    pwm_dev.disable()
    assert pwm_dev.get_enabled() == False
    pwm_dev.close()

    