""" Calibration utility module for DAC devices """


from dataclasses import dataclass

# TODO: need to combine this calibration dataclass into one to avoid confusion.
# This requires some more research and revision in calculation
@dataclass
class DAChWCalibConst:
    """Calibration constants for DAC error values"""

    gain = 0
    offset = 0


@dataclass
class DACsWCalibConst:
    """Calibration constants for DAC amplifier values"""

    gain = 2.5
    offset = 0


# TODO: add functions/classes for calibration
