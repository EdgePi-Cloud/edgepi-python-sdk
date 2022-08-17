""" Utility module for ADC commands """


import logging

import bitstring
from edgepi.adc.adc_constants import ADCComs, ADCReg
from edgepi.reg_helper.reg_helper import OpCode, BitMask
from edgepi.utilities.utilities import filter_dict


_logger = logging.getLogger(__name__)


class ChannelMappingError(ValueError):
    """Raised when an input channel is mapped to both ADC1 and ADC2"""


# pylint: disable=logging-too-many-args
class ADCCommands:
    """Class representing ADC commands"""

    def __init__(self):
        _logger.info("Initializing ADC Methods")

    def read_register_command(self, address: int, num: int):
        """Trigger ADC register read"""
        self.check_for_int([address, num])
        command = [ADCComs.COM_RREG.value + address, num - 1]
        _logger.debug("Command to send is %s", (command + [255] * num))
        return command + [255] * num

    def write_register_command(self, address, values):
        """Trigger ADC register write"""
        self.check_for_int([address])
        all(self.check_range(value, 0, 255) for value in values)
        self.check_for_int(values)
        command = [ADCComs.COM_WREG.value + address, len(values) - 1]
        _logger.debug("Command to send is %s", (command + values))
        return command + values

    def start_adc1(self):
        """Command to start ADC"""
        _logger.debug("Command to send is %s", ([ADCComs.COM_START1.value]))
        return [ADCComs.COM_START1.value]

    def stop_adc1(self):
        """Command to stop ADC"""
        _logger.debug("Command to send is %s", ([ADCComs.COM_STOP1.value]))
        return [ADCComs.COM_STOP1.value]

    def reset_adc(self):
        """Command to reset ADC"""
        _logger.debug("Command to send is %s", ([ADCComs.COM_RESET.value]))
        return [ADCComs.COM_RESET.value]

    @staticmethod
    def check_for_int(target_list):
        """Checks if a list contains only integer values"""
        if all(isinstance(value, int) for value in target_list) and target_list:
            return True
        raise ValueError(f"Non integer value passed {target_list}")

    @staticmethod
    def check_range(target, lower, upper):
        """Validates target is in range between a min and max value"""
        if lower <= target <= upper:
            return True
        raise ValueError(f"Target out of range {target}")

    @staticmethod
    def get_channel_assign_opcodes(
        adc_1_mux_p: int = None,
        adc_2_mux_p: int = None,
        adc_1_mux_n: int = None,
        adc_2_mux_n: int = None,
    ):
        """
        Generates OpCodes for assigning positive and negative multiplexers
        of either ADC1 or ADC2 to an ADC input channel. This is needed to allow
        users to assign multiplexers by input channel number.

        Args:
            adc_1_mux_p: input channel to assign to MUXP of ADC1
            adc_2_mux_p: input channel to assign to MUXP of ADC2
            adc_1_mux_n: input channel to assign to MUXN of ADC1
            adc_2_mux_n: input channel to assign to MUXN of ADC2

        Returns:
            `list`: if not empty, contains OpCode(s) for updating multiplexer
                channel assignment for ADC1, ADC2, or both.

        Raises:
            `ChannelMappingError`: if any two multiplexers are assigned the same input channel
        """
        args = filter_dict(locals(), "self")

        # no multiplexer config to update
        if all(x is None for x in list(args.values())):
            return []

        if len(args) != len(set(args)):
            raise ChannelMappingError(
                "ADC1 and ADC2 multiplexers must be assigned different input channels"
            )

        adc_mux_regs = {
            ADCReg.REG_INPMUX: (adc_1_mux_p, adc_1_mux_n),
            ADCReg.REG_ADC2MUX: (adc_2_mux_p, adc_2_mux_n),
        }

        mux_opcodes = []

        # TODO: what if user tries setting a mux to a channel already in use?
        # need to read mux register values to check for this

        for addx, byte in adc_mux_regs.items():
            mux_p = byte[0]
            mux_n = byte[1]

            # not updating mux's for this adc_num (no args passed)
            if mux_p is None and mux_n is None:
                continue
            # updating mux_p bits only, mask mux_p bits
            elif mux_n is None:
                mask = BitMask.HIGH_NIBBLE
                # replace None with 0 for building bitstring
                mux_n = 0
                mux_p = mux_p.value
            # updating mux_n bits only, mask mux_n bits
            elif mux_p is None:
                mask = BitMask.LOW_NIBBLE
                # replace None with 0 for building bitstring
                mux_p = 0
                mux_n = mux_n.value
            # updating both mux_n and mux_p
            else:
                mask = BitMask.BYTE
                mux_p = mux_p.value
                mux_n = mux_n.value

            adc_x_ch_bits = bitstring.pack("uint:4, uint:4", mux_p, mux_n).uint

            mux_opcodes.append(OpCode(adc_x_ch_bits, addx.value, mask.value))

        return mux_opcodes
