""" Calibration utility module for DAC devices """


from dataclasses import dataclass
from decimal import Decimal


# TODO: need to combine this calibration dataclass into one to avoid confusion.
# This requires some more research and revision in calculation
@dataclass
class DAChWCalibConst:
    """Calibration constants for DAC error values"""

    gain: Decimal = Decimal(0)
    offset: Decimal = Decimal(0)


@dataclass
class DACsWCalibConst:
    """Calibration constants for DAC amplifier values"""

    gain: Decimal = Decimal(2.5)
    offset: Decimal = Decimal(0)


# TODO: add functions/classes for calibration
