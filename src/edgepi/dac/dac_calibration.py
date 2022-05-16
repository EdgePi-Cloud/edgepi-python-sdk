from dataclasses import dataclass
from typing import List

@dataclass
class DACHwCalib_const:
    gain: float = 0
    offset: float = 0

@dataclass
class DACSwCalib_const:
    gain: float = 2.5
    offset: float = 0

# TODO: add functions/classes for calibration