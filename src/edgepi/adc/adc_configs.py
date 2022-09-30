""" Utility module for ADC device configuration """


from dataclasses import dataclass


@dataclass(frozen=True)
class ADCVoltageConfig:
    """ADC voltage measurement configuration"""
    offset: float
    gain: float
    v_ref: float    # input reference voltage
