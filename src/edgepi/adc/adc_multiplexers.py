""" Helper methods for EdgePi ADC multiplexer mapping """

import logging

from edgepi.reg_helper.reg_helper import OpCode, BitMask
from edgepi.adc.adc_constants import ADCChannel as CH, AllowedChannels, ADCReg

_logger = logging.getLogger(__name__)


class ChannelNotAvailableError(ValueError):
    """
    Raised when an input channel is unavailable for mapping to a multiplexer
    due to RTD_EN status.
    """

def generate_mux_opcode(addx:ADCReg, mux_p:CH, mux_n:CH) -> OpCode:
    """
    Generates OpCode for updating input multiplexer mapping.

    We know that mux_p_val can never be larger than 15 (are a byte),
    because mux_p and mux_n are ADCChannel.
    """
    return OpCode(
        op_code=(mux_p.value << 4) + mux_n.value,
        reg_address=addx.value,
        op_mask=BitMask.BYTE.value
    )

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
    if any((chan not in allowed_channels) for chan in channels):
        unavaliable_channel = next(chan for chan in channels if (chan not in allowed_channels))
        raise ChannelNotAvailableError(
            f"Channel 'AIN{unavaliable_channel.value}' is currently not available. "
            "Disable RTD in order to use."
        )
