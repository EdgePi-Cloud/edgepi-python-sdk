""" Calibration utility module for DAC devices """


from dataclasses import dataclass


@dataclass
class DACcalibParam:
    """
    Calibration constants for DAC
    gain_1: gain calibration parameter when internal_gain is disabled
    offset_1: offset calibration parameter when internal_gain is disabled

    gain_2: gain calibration parameter when internal_gain is enabled
    offset_2: offset calibration parameter when internal_gain is enabled

    Note: default value of 2.5 and 0 are set, these values will be overwritten
          during the run-time.
    """
    # TODO: add documentation regading how these parameters are provided
    gain_1: float = 2.5
    offset_1: float = 0

    gain_2: float = 5.0
    offset_2:float = 0


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
