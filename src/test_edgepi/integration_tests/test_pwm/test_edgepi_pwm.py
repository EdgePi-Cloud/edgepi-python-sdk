"""EdgePi PWM integration test"""

import logging
import pytest

from edgepi.gpio.gpio_constants import GpioPins
from edgepi.pwm.pwm_constants import PWMCh, Polarity
from edgepi.pwm.edgepi_pwm import EdgePiPWM

_logger = logging.getLogger(__name__)

@pytest.fixture(name="pwm_dev")
def fixture_test_pwm():
    pwm_dev = EdgePiPWM(GpioPins.PWM1, 1000, 0.5, Polarity.NORMAL)
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
def test_pwm_init(pwm_num, freq, duty_cycle, polarity, result):
    pwm_dev = EdgePiPWM(pwm_num=pwm_num,freq=freq, duty_cycle=duty_cycle, polarity=polarity)
    assert pwm_dev.channel == result[0]
    assert pwm_dev.chip == result[1]
    assert pwm_dev.freq == result[2]
    assert pwm_dev.duty_cycle == result[3]
    assert pwm_dev.polarity.value == result[4].value
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

# TODO:When set frequncy test is called before get duty cycle pwm, the duty cycle value chagnes
# However when it is called individually, it is working as expectd.
def test_get_duty_cycle_pwm(pwm_dev):
    dc = pwm_dev.get_dutycycle()
    assert dc == 0.5

def test_set_duty_cycle_pwm(pwm_dev):
    init_duty_cycle = pwm_dev.get_dutycycle()
    pwm_dev.set_dutycycle(0.6)
    result = pwm_dev.get_dutycycle()
    assert result != init_duty_cycle

def test_get_polarity_pwm(pwm_dev):
    pol = pwm_dev.get_polarity()
    assert pol == Polarity.NORMAL.value

def test_set_polarity_pwm(pwm_dev):
    init_pol = pwm_dev.get_polarity()
    pwm_dev.set_polarity(Polarity.INVERSED)
    result = pwm_dev.get_polarity()
    assert result != init_pol

def test_enable(pwm_dev):
    pwm_dev.enable()

def test_disable(pwm_dev):
    pwm_dev.disable()
    