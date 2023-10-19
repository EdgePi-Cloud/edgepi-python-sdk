""" Integration test for peripheral concurrency """

import threading
import logging
import pytest

from edgepi.pwm.pwm_constants import Polarity, PWMPins
from edgepi.pwm.edgepi_pwm import EdgePiPWM

_logger = logging.getLogger(__name__)

class PropagatingThread(threading.Thread):
    """Propagating thread to raise exceptions in calling function"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exc = None

    def run(self):
        self.exc = None
        try:
            super().run()
        # pylint:disable=broad-exception-caught
        except Exception as err:
            self.exc = err

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        if self.exc:
            raise self.exc

@pytest.fixture(name="pwm_dev")
def fixture_test_pwm():
    pwm_dev = EdgePiPWM()
    yield pwm_dev

def pwm_open_set_config_close(pwm):
    """PWM init, setconfig and close"""
    pwm.init_pwm(PWMPins.PWM1)
    pwm.set_config(PWMPins.PWM1, frequency=1000, duty_cycle=0.5, polarity=Polarity.NORMAL)
    # pwm.close(PWMPins.PWM1)

#pylint:disable=unused-argument
@pytest.mark.parametrize("iteration", range(10))
def test_pwm_concurrency_shared(iteration, pwm_dev):
    """Test for PWM concurrency bug"""
    threads = [PropagatingThread(target=pwm_open_set_config_close(pwm_dev)) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def pwm_open_set_config_close_indiv():
    """PWM init, setconfig and close"""
    pwm = EdgePiPWM()
    pwm.init_pwm(PWMPins.PWM1)
    pwm.set_config(PWMPins.PWM1, frequency=1000, duty_cycle=0.5, polarity=Polarity.NORMAL)
    # pwm.close(PWMPins.PWM1)

#pylint:disable=unused-argument
@pytest.mark.parametrize("iteration", range(10))
def test_pwm_concurrency_indiv(iteration):
    """Test for pwm concurrency bug"""
    threads = [PropagatingThread(target=pwm_open_set_config_close_indiv()) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
