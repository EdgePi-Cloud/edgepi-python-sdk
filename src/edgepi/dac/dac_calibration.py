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
class DACcalibParam:
    """Calibration constants for DAC"""

    gain_1: float = 2.5
    offset_1: float = 0

    gain_2: float = 5.0
    offset_2:float = 0

# TODO: add functions/classes for calibration

def generate_dict_calibration(calib: DACcalibParam = None,
                              list_ch: list = None,
                              list_param: list = None):
    """
    Function to generate dictionary of channel to calibration parameter dataclass
    Args:
        calib: DACcalibParam: dataclass containing calibration parameters
        list_ch: list of channel numbers from 0-7
        list_param: list of parameters for each channel, this should've be read from eeprom
    Return:
        dict_calib_param: dictionary of calibration parameter
                          {channel(int) : DACcalibParam(gain_1, offset_1, gain_2, offset_2)}
    """
    dict_calib_param = {}
    for i, ch in enumerate(list_ch, 0):
        dict_calib_param[ch] = calib(gain_1 = list_param[i][0],
                                             offset_1 = list_param[i][1],
                                             gain_2 = list_param[i][2],
                                             offset_2 = list_param[i][3])
    return dict_calib_param
