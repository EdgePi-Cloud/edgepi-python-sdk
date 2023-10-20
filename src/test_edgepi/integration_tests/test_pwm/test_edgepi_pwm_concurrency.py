""" Integration test for peripheral concurrency """

import threading
import logging
import pytest

from edgepi.pwm.pwm_constants import Polarity, PWMPins
from edgepi.pwm.edgepi_pwm import EdgePiPWM, PwmDeviceError

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

def pwm_open_set_config(pwm):
    """PWM init, setconfig"""
    pwm.init_pwm(PWMPins.PWM1)
    pwm.set_config(PWMPins.PWM1, frequency=1000, duty_cycle=0.5, polarity=Polarity.NORMAL)

def pwm_open_close(pwm):
    """PWM init and close"""
    pwm.init_pwm(PWMPins.PWM1)
    pwm.close(PWMPins.PWM1)

def pwm_set_config(pwm):
    """PWM setconfig"""
    pwm.set_config(PWMPins.PWM1, frequency=1000, duty_cycle=0.5, polarity=Polarity.NORMAL)

#pylint:disable=unused-argument
@pytest.mark.parametrize("iteration", range(10))
def test_pwm_concurrency_shared(iteration, pwm_dev):
    """Test for PWM concurrency bug"""
    threads = [PropagatingThread(target=pwm_open_set_config(pwm_dev)) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

@pytest.mark.parametrize("iteration", range(10))
def test_pwm_concurrency_shared_error(iteration, pwm_dev):
    """Test for PWM concurrency bug"""
    with pytest.raises(PwmDeviceError):
        threads_open_close = [PropagatingThread(target=pwm_open_close(pwm_dev)) for _ in range(10)]
        threads_set_config = [PropagatingThread(target=pwm_set_config(pwm_dev)) for _ in range(10)]
        for _, indx in enumerate(threads_open_close):
            threads_open_close[indx].start()
            threads_set_config[indx].start()
        for _, indx in enumerate(threads_open_close):
            threads_open_close[indx].join()
            threads_set_config[indx].join()

def pwm_open_set_config_indiv():
    """PWM init, setconfig """
    pwm = EdgePiPWM()
    pwm.init_pwm(PWMPins.PWM1)
    pwm.set_config(PWMPins.PWM1, frequency=1000, duty_cycle=0.5, polarity=Polarity.NORMAL)

def pwm_open_close_indiv():
    """PWM init close"""
    pwm = EdgePiPWM()
    pwm.init_pwm(PWMPins.PWM1)
    pwm.close(PWMPins.PWM1)

def pwm_set_config_indiv():
    """PWM setconfig"""
    pwm = EdgePiPWM()
    pwm.set_config(PWMPins.PWM1, frequency=1000, duty_cycle=0.5, polarity=Polarity.NORMAL)


#pylint:disable=unused-argument
@pytest.mark.parametrize("iteration", range(10))
def test_pwm_concurrency_close_indiv_error(iteration):
    """Test for pwm concurrency bug"""
    with pytest.raises(PwmDeviceError):
        threads_open_close = [PropagatingThread(target=pwm_open_close_indiv()) for _ in range(10)]
        threads_set_config = [PropagatingThread(target=pwm_set_config_indiv()) for _ in range(10)]
        for _, indx in enumerate(threads_open_close):
            threads_open_close[indx].start()
            threads_set_config[indx].start()
        for _, indx in enumerate(threads_open_close):
            threads_open_close[indx].join()
            threads_set_config[indx].join()

@pytest.mark.parametrize("iteration", range(10))
def test_pwm_concurrency_close_indiv(iteration, pwm_dev):
    """Test for PWM concurrency bug"""
    threads = [PropagatingThread(target=pwm_open_set_config_indiv()) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
