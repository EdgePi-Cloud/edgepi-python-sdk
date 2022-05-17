from dataclasses import dataclass
from typing import List

#TODO: need to combine this calibration dataclass into one to avoid confusion. This requires some more research and revision in calculation
@dataclass
class DACHwCalib_const:
    gain: float = 0
    offset: float = 0

@dataclass
class DACSwCalib_const:
    gain: float = 2.5
    offset: float = 0

# TODO: add functions/classes for calibration