""" Helper methods for EdgePi ADC multiplexer mapping """


from bitstring import pack

from edgepi.reg_helper.reg_helper import OpCode, BitMask
from edgepi.adc.adc_constants import ADCChannel as CH


MUXS_PER_ADC = 2
NUM_CHANNELS = 11


class ChannelNotAvailableError(ValueError):
    """
    Raised when an input channel is unavailable for mapping to a multiplexer
    due to RTD_EN status.
    """


def _format_mux_values(mux_p, mux_n):
    # updating mux_p bits only, mask mux_p bits
    if mux_n is None:
        mask = BitMask.HIGH_NIBBLE
        # replace None with 0 for building bitstring
        mux_n_val = 0
        mux_p_val = mux_p.value
    # updating mux_n bits only, mask mux_n bits
    elif mux_p is None:
        mask = BitMask.LOW_NIBBLE
        # replace None with 0 for building bitstring
        mux_p_val = 0
        mux_n_val = mux_n.value
    # updating both mux_n and mux_p
    else:
        mask = BitMask.BYTE
        mux_p_val = mux_p.value
        mux_n_val = mux_n.value

    return mux_p_val, mux_n_val, mask


def generate_mux_opcodes(mux_updates: dict, mux_values: dict):
    """
    Generates list of OpCodes for updating mux mapping

    Args:
        `mux_updates` (dict): values for updating multiplexer mapping

        `mux_values` (dict): current multiplexer mapping

        Note: both of the above must be dictionaries formatted as:

            mux_reg_addx (ADCReg): (mux_p_val, mux_n_val)

    Returns:
        `list`: OpCodes for updated multiplexer mapping
    """
    mux_opcodes = []
    # generate OpCodes for mux updates
    for addx, byte in mux_updates.items():
        mux_p = byte[0]
        mux_n = byte[1]

        # not updating mux's for this adc_num (no args passed)
        if mux_p is None and mux_n is None:
            continue

        mux_p_val, mux_n_val, mask = _format_mux_values(mux_p, mux_n)

        # update mux_register values for duplicate mapping validation, but only
        # if these were updated
        if not mux_p is None:
            mux_values[addx][0] = mux_p_val

        if not mux_n is None:
            mux_values[addx][1] = mux_n_val

        adc_x_ch_bits = pack("uint:4, uint:4", mux_p_val, mux_n_val).uint

        mux_opcodes.append(OpCode(adc_x_ch_bits, addx.value, mask.value))

    return mux_opcodes


def validate_channels_allowed(channels: list, rtd_enabled: bool):
    """
    Checks if requested input channels to be mapped are available due to RTD_EN status

    Args:
        `channels` (list): list of ADCChannel objects representing input channel mapping
        `rtd_enabled` (bool): RTD_EN status
    """
    # channels available depend on RTD_EN status
    allowed_channels = (
        list(CH)
        if rtd_enabled
        else [CH.AIN0, CH.AIN1, CH.AIN2, CH.AIN3, CH.AINCOM, CH.FLOAT]
    )
    for ch in channels:
        if ch not in allowed_channels:
            raise ChannelNotAvailableError(
                f"Channel {ch.value} is currently not available. Enable RTD in order to use."
            )
