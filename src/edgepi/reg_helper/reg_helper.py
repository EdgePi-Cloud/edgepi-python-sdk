"""
Helper functions and class for modifying device register values

Classes:

    OpCode
    OpCodeMaskIncompatibleError(ValueError)

Functions:

    _add_change_flags(dict)
    apply_opcodes(dict, list)
    apply_opcode(OpCode, int)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OpCode:
    """
    Represents an operation to opcode to the value stored in a memory register

    Attributes
    ----------
    op_code : int
        the value used to update the register bits relevant to this setting or command.
        Please see below for a practical example on how to define the op_code.
    reg_address : int
        the register's address in the device's register memory map
    op_mask : int
        the value used to clear the register bits whose value will be updated
        when the op_code is applied. Mask bits intended to clear corresponding
        bits in the target value should be assigned a value of 0.
        Please see below for a practical example on how to define the op_mask.

    An example of how to define OpCode fields:

        Assume we have a register with the following bit values: register_value = (0b1010 1101)

        Let's assume we wish to update only the high bits (0b1010) to a new value, (0b0110).
        So our intended goal is to change the register_value to (0b0110 1101).

        To do so, we first need to clear, or in other words, mask these high bits.
        The mask to use here should be defined as (0b0000 1111). This allows us to clear the high bits
        in a single AND operation, as follows:

            (0b1010 1101) & (0b0000 1111) = (0b0000 1101).

        Now the high bits have been cleared, we can apply our opcode. In order to obtain our final
        register_value of (0b0110 1101), our opcode should be (0b0110 0000). Applying this opcode
        to our now 'masked' register_value, with an OR operation, gives us our final register value:

            (0b0000 1101) | (0b0110 0000) = (0b0110 1101)
    """

    op_code: int
    reg_address: int
    op_mask: int


class OpCodeMaskIncompatibleError(ValueError):
    """Raised when an OpCode contains an op_code which affects bits not covered by the op_mask"""


def apply_opcodes(register_values: dict, opcodes: list):
    """
    Generates updated register values after applying opcodes, and sets is_changed flag for updated registers.

    Args:
        register_values (dict): a map of a device's registers to a dictionary containing their corresponding register values.
                                The dictionary must contain entries of the form register_address (int): register_value (int).

        opcodes (list): a list of OpCode objects to be used for updating register values.

    Returns:
        a map of the device's registers to a dictionary containg the updated values and change flags

    Raises:
        ValueError: if either register_values or opcodes is empty
    """
    if len(register_values) < 1 or len(opcodes) < 1:
        raise ValueError("register_values and opcodes args must both be non-empty")
    _format_register_map(register_values)

    # apply each opcode to its corresponding register
    for opcode in opcodes:
        register_entry = register_values.get(opcode.reg_address)
        # if this opcode maps to a valid register address
        if register_entry is not None:
            # apply the opcode to the register
            register_entry["value"] = _apply_opcode(register_entry["value"], opcode)
            register_entry["is_changed"] = True

    return register_values


def _apply_opcode(register_value: int, opcode: OpCode):
    """
    Generates an update code for a specific register by applying an opcode

    Args:
        opcode (OpCode): an OpCode object representing the opcode to be applied to the register

        register_value (int): the current stored value of the register

    Returns:
        an update code, the value to be written back to the register in order to apply
        the opcode.
    """
    # ensure op_code only writes to bits of register covered by mask
    if (~opcode.op_mask & opcode.op_code) != opcode.op_code:
        raise OpCodeMaskIncompatibleError(f'''opcode ({hex(opcode.op_code)}) affects bits not covered by mask ({hex(opcode.op_mask)}''')

    register_value &= opcode.op_mask  # clear the bits to be overwritten
    register_value |= opcode.op_code  # apply the opcode to the cleared bits

    return register_value


def _add_change_flags(register_values: dict):
    """
    adds flags to register values for checking to see if register value has been modified later

    Args:
        register_values (dict): a map of the device's registers to their current values

    Returns:
        the same dictionary but with an added 'is_changed' field for each entry
    """
    for key in register_values:
        register_values[key]["is_changed"] = False


def _convert_values_to_dict(reg_map: dict) -> dict:
    """Changes a register_address, register_value map to use register_address, dictionary format
    where the dictionary now hold the register_value.

    Args:
        reg_map (dict): a dictionary containing (int) register_address, (int) register_value pairs

    Returns:
        a dictionary containing (int) register_address, {'value': register_value} pairs
    """
    # convert each addx, value pair to addx, dictionary pair
    for addx, value in reg_map.items():
        reg_map[addx] = {"value": value}


def _format_register_map(reg_map: dict) -> dict:
    """converts map of register_address, register_value pairs to a format compatible with functions
    defined in this module.

    Args:
        reg_map (dict): a dictionary containing (int) register_address, (int) register_value pairs

    Returns:
        a dictionary containing (int) register_address, {'value': register_value, 'is_changed': False} pairs
    """
    _convert_values_to_dict(reg_map)
    _add_change_flags(reg_map)
