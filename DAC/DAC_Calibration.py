from dataclasses import dataclass
from typing import List

@dataclass
class dac_hw_calib_const:
    gain: float = 2.5
    offset: float = 0

@dataclass
class dac_sw_calib_const:
    gain: float = 2.5
    offset: float = 0