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

@dataclass
class DAC_calib_param:
    """Calibration constants for DAC amplifier values"""

    gain_1: float = 2.5
    offset_1: float = 0

    gain_2: float = 5.0
    offset_2:float = 0

# TODO: add functions/classes for calibration

def generate_dict_calibration(calib: DAC_calib_param = None, list_ch: list = None, list_param: list = None):
    dict_calib_param = {}
    for i in range(len(list_ch)):
        dict_calib_param[list_ch[i]] = calib(gain_1 = list_param[i][0], offset_1 = list_param[i][1], gain_2 = list_param[i][2], offset_2 = list_param[i][3])
    return dict_calib_param