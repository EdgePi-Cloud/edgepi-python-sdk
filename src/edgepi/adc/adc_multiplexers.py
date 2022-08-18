""" Helper methods for EdgePi ADC multiplexer mapping """


from bitstring import pack

from edgepi.reg_helper.reg_helper import OpCode, BitMask


NUM_MUXS = 4

class ChannelMappingError(ValueError):
    """Raised when an input channel is mapped to both ADC1 and ADC2"""


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

    _validate_mux_mapping(mux_values)

    return mux_opcodes


def _validate_mux_mapping(mux_values: dict):
    """
    Verifies no two multiplexers are assigned the same channel

    Args:
        `mux_values`: updated multiplexer mapping

        Note: above must be formatted as:

            mux_reg_addx (ADCReg): (mux_p_val, mux_n_val)

    Raises:
        `ChannelMappingError`: if the updated multiplexer mapping contains any two
            multiplexers assigned the same input channel.
    """
    # TODO: by default, on startup some mux's are set to same channels.
    # Change each mux to different value in EdgePiADC __init__.
    mux_set = set()

    for entry in mux_values.values():
        mux_set.update(set(entry))

    if len(mux_set) < NUM_MUXS:
        raise ChannelMappingError("Attempting to assign channel already in use")
