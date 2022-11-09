""" Helper methods for EdgePi ADC multiplexer mapping """

import logging

from bitstring import pack
from edgepi.reg_helper.reg_helper import OpCode, BitMask
from edgepi.adc.adc_constants import ADCChannel as CH, AllowedChannels

_logger = logging.getLogger(__name__)

MUXS_PER_ADC = 2
NUM_CHANNELS = 11


class ChannelNotAvailableError(ValueError):
    """
    Raised when an input channel is unavailable for mapping to a multiplexer
    due to RTD_EN status.
    """


def _format_mux_values(mux_p: CH, mux_n: CH):
    # all use cases will always update both mux_n and mux_p
    mask = BitMask.BYTE
    mux_p_val = mux_p.value
    mux_n_val = mux_n.value

    return mux_p_val, mux_n_val, mask


def generate_mux_opcodes(mux_updates: dict):
    """
    Generates list of OpCodes for updating input multiplexer mapping.
    Updates both positive and negative multiplexers.

    Args:
        `mux_updates` (dict): values for updating multiplexer mapping.
            This should be formatted as {ADCReg: (ADCChannel, ADChannel)}.

        `mux_values` (dict): current multiplexer mapping.
            This should be formatted as {ADCReg: (int, int)}.

        Note: both of the above must be dictionaries formatted as:

            mux_reg_addx (ADCReg): (mux_p_val, mux_n_val)

    Returns:
        `list`: OpCodes for updated multiplexer mapping
    """
    _logger.debug(f"mux updates = {mux_updates}")

    mux_opcodes = []
    # generate OpCodes for mux updates
    for addx, byte in mux_updates.items():
        mux_p = byte[0]
        mux_n = byte[1]

        # not updating mux's for this adc_num (no args passed)
        if mux_p is None or mux_n is None:
            continue

        mux_p_val, mux_n_val, mask = _format_mux_values(mux_p, mux_n)

        adc_x_ch_bits = pack("uint:4, uint:4", mux_p_val, mux_n_val).uint

        mux_opcodes.append(OpCode(adc_x_ch_bits, addx.value, mask.value))

    _logger.debug(f"mux opcodes = {mux_opcodes}")

    return mux_opcodes


def validate_channels_allowed(channels: list, rtd_enabled: bool):
    """
    Checks if requested input channels to be mapped are available due to RTD_EN status,
    i.e. in case ADC2 is being used while ADC1 is in RTD mode.

    Args:
        `channels` (list): list of ADCChannel objects representing input channel mapping
        `rtd_enabled` (bool): RTD_EN status
    """
    # channels available depend on RTD_EN status
    allowed_channels = (
        AllowedChannels.RTD_ON.value
        if rtd_enabled
        else AllowedChannels.RTD_OFF.value
    )
    for ch in channels:
        if ch not in allowed_channels:
            raise ChannelNotAvailableError(
                f"Channel 'AIN{ch.value}' is currently not available. Disable RTD in order to use."
            )
