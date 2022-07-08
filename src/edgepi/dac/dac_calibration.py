""" Calibration utility module for DAC devices """


from dataclasses import dataclass


# TODO: need to combine this calibration dataclass into one to avoid confusion.
# This requires some more research and revision in calculation
@dataclass
class DAChWCalibConst:
    """Calibration constants for DAC"""

    gain: float = 0
    offset: float = 0


@dataclass
class DACsWCalibConst:
    """Calibration constants for DAC"""

    gain: float = 2.5
    offset: float = 0


# pylint: disable=fixme
# TODO: add functions/classes for calibration
