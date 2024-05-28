""" Helper methods for EdgePi ADC multiplexer mapping """

import logging

from edgepi.reg_helper.reg_helper import OpCode, BitMask
from edgepi.adc.adc_constants import ADCChannel as CH, AllowedChannels, ADCReg

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

def generate_mux_opcodes(adc1_mux: (CH, CH), adc2_mux: (CH, CH)) -> list:
    """
    Generates list of OpCodes for updating input multiplexer mapping.
    Updates both positive and negative multiplexers.

    Args:
        `adc1_mux` (ADCChannel, ADCChannel): The new channel values for for updating
            multiplexer mapping for adc1. The first is mux_p, the second is mux_n.
        `adc2_mux` (ADCChannel, ADCChannel): The new channel values for for updating
            multiplexer mapping for adc2. The first is mux_p, the second is mux_n.

        Note: both of the above must be tuples must be formatted as (mux_p_val, mux_n_val)

    Returns:
        `list`: OpCodes for updated multiplexer mapping
    """
    mux_opcodes = []

    def do_opcode(addx, mux_p: CH, mux_n: CH):
        # not updating mux's for this adc_num (no args passed)
        if mux_p is None or mux_n is None:
            return []

        # NOTE: for this function, we know that mux_p_val can never be larger than 15, 
        # because mux_p and mux_n are ADCChannel
        mux_p_val, mux_n_val, mask = _format_mux_values(mux_p, mux_n)

        adc_x_ch_bits = (mux_p_val << 4) + mux_n_val
        return [OpCode(adc_x_ch_bits, addx.value, mask.value)]

    # ADCReg.REG_INPMUX controls multiplexing for ad1, whileADCReg.REG_ADC2MUX controls
    # multiplexing for adc2
    mux_opcodes += do_opcode(ADCReg.REG_INPMUX, adc1_mux[0], adc1_mux[1])
    mux_opcodes += do_opcode(ADCReg.REG_ADC2MUX, adc2_mux[0], adc2_mux[1])

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
    for chan in channels:
        if chan not in allowed_channels:
            raise ChannelNotAvailableError(
                f"Channel 'AIN{chan.value}' is currently not available. "
                "Disable RTD in order to use."
            )
