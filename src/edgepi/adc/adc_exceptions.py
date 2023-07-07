"""ADC Exception Classes"""

class ADCStateMissingMap(Exception):
    """ "Raised if ADCState.get_map() is called before ADCState has been assigned a cached state"""

class ADCRegisterUpdateError(Exception):
    """Raised when a register update fails to set register to expected value"""

class VoltageReadError(Exception):
    """Raised if a voltage read fails to return the expected number of bytes"""

class ContinuousModeError(Exception):
    """Raised when `read_voltage` is called and ADC is not in CONTINUOUS conversion mode"""

class RTDEnabledError(Exception):
    """Raised when user attempts to set ADC configuration that conflicts with RTD mode"""

class InvalidDifferentialPairError(Exception):
    """
    Raised when calibration values are attempted to be retrieved for an invalid Differential
    read pair
    """

class CalibKeyMissingError(Exception):
    """Raised when calibration values are missing from EEPROM dictionary"""
