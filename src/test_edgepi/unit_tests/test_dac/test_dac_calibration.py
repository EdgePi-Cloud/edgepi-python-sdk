"""unit test for dac module"""

import pytest
from edgepi.dac.dac_calibration import DAC_calib_param, generate_dict_calibration


@pytest.mark.parametrize(
    "list_ch, list_param, result",
    [
        ([1], [[1.3, 1.2, 3.3, 4.5]], {1 : DAC_calib_param(1.3, 1.2, 3.3, 4.5)}),
        ([1, 2], [[1.3, 1.2, 3.3, 4.5], [1, 2, 3, 4]], {1 : DAC_calib_param(1.3, 1.2, 3.3, 4.5),
                                                        2 : DAC_calib_param(1, 2, 3, 4)}),
        ([0, 1, 2, 3, 4, 5, 6, 7], [[1.3, 1.2, 3.3, 4.5],
                                    [1, 2, 3, 4],
                                    [3, 4, 5, 8],
                                    [1.3, 1.2, 3.3, 41.5],
                                    [2.3, 3.2, 35.3, 24.5],
                                    [5.3, 5.2, 3.3, 34.5],
                                    [3.3, 7.2, 3.3, 45.5],
                                    [2.3, 19.2, 9.3, 46.5]],
                                    {0 : DAC_calib_param(1.3, 1.2, 3.3, 4.5),
                                     1 : DAC_calib_param(1, 2, 3, 4),
                                     2 : DAC_calib_param(3, 4, 5, 8),
                                     3 : DAC_calib_param(1.3, 1.2, 3.3, 41.5),
                                     4 : DAC_calib_param(2.3, 3.2, 35.3, 24.5),
                                     5 : DAC_calib_param(5.3, 5.2, 3.3, 34.5),
                                     6 : DAC_calib_param(3.3, 7.2, 3.3, 45.5),
                                     7 : DAC_calib_param(2.3, 19.2, 9.3, 46.5)})
    ])
def test_dac_generate_dict_calibration(list_ch, list_param, result):
    dict_calib_param = generate_dict_calibration(DAC_calib_param, list_ch, list_param)
    assert dict_calib_param == result