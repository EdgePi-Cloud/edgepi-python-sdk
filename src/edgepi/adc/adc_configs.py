""" Utility module for ADC device configuration """


from dataclasses import dataclass

# pylint: disable=fixme
# TODO: rev_id can be differ by chips, only manufacurer has control over it
@dataclass(frozen=True)
class AdcRegID:
    """ADC device register ID's"""

    dev_id: int = 1
    rev_id: int = 0

    def get_value(self) -> int:
        """Combines attribute bits in order into a single binary code"""
        return self.dev_id << 5 | self.rev_id << 0


@dataclass
class AdcRegPower:
    """ADC register power configuration"""

    reset: int = 1
    vbias: int = 0
    intref: int = 1

    def get_value(self) -> int:
        """Combines attribute bits in order into a single binary code"""
        return self.reset << 4 | self.vbias << 1 | self.intref << 0


@dataclass
class AdcRegInterface:
    """ADC register interface configuration"""

    timeout: int = 0
    status: int = 1
    crc: int = 1

    def get_value(self) -> int:
        """Combines attribute bits in order into a single binary code"""
        return self.timeout << 3 | self.status << 2 | self.crc << 0


@dataclass
class AdcRegMode0:
    """ADC register mode 0 configuration"""

    refrev: int = 0
    runmode: int = 0
    chop: int = 0
    delay: int = 0

    def get_value(self) -> int:
        """Combines attribute bits in order into a single binary code"""
        return self.refrev << 7 | self.runmode << 6 | self.chop << 4 | self.delay << 0


@dataclass
class AdcRegMode1:
    """ADC register mode 1 configuration"""

    filter: int = 4
    sbadc: int = 0
    sbpol: int = 0
    sbmag: int = 0

    def get_value(self) -> int:
        """Combines attribute bits in order into a single binary code"""
        return self.filter << 5 | self.sbadc << 4 | self.sbpol << 3 | self.sbmag << 0


@dataclass
class AdcRegMode2:
    """ADC register mode 2 configuration"""

    bypass: int = 0
    gain: int = 0
    dr: int = 4

    def get_value(self) -> int:
        """Combines attribute bits in order into a single binary code"""
        return self.bypass << 7 | self.gain << 4 | self.dr << 0


@dataclass(frozen=True)
class ADCVoltageConfig:
    """ADC voltage measurement configuration"""
    offset: float
    gain: float
    v_ref: float    # input reference voltage
