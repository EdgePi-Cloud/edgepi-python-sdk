""" Calibration utility module for DAC devices """


from dataclasses import dataclass


# TODO: need to combine this calibration dataclass into one to avoid confusion.
# This requires some more research and revision in calculation
@dataclass
class DAChWCalibConst:
    """Calibration constants for DAC error values"""

    gain: float = 0
    offset: float = 0


@dataclass
class DACsWCalibConst:
    """Calibration constants for DAC amplifier values"""

    gain: float = 2.5
    offset: float = 0


# TODO: add functions/classes for calibration
