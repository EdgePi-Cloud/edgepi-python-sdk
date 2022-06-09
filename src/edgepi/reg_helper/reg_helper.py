'''
Helper functions and class for modifying device register values

Classes:

    OpCode

Functions:

    apply_opcodes(dict, list)
    apply_opcode(object, int)
'''

from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class OpCode:
    '''
    Represents an operation to opcode to the value stored in a memory register

    Attributes
    ----------
    op_code : int
        the value to be written to the register
    reg_address : int
        the register's address in the device's register memory map
    op_mask : int
        the value to be used to op_mask the register bits whose value will be updated
    '''
    # needs better name
    op_code: int
    reg_address: int
    op_mask: int

# TODO: make more efficient by grouping by address
def apply_opcodes(register_values:dict, opcodes:list):
    '''
    Generates updated register values after applying opcodes

    Args:
        register_values (dict): a map of the device's registers to their current values

        updates (list): a list of valid Enum objects representing opcodes to be applied to registers.
                        See tc_constants.py for for a valid Enums.

    Returns:
        a map of the device's registers to their updated values
    '''
    # apply each opcode to its corresponding register
    for opcode in opcodes:
        if opcode is None:
            continue
        register_value = register_values.get(opcode.value.reg_address)
        # apply the opcode to the register
        register_values[opcode.value.reg_address] = _apply_opcode(register_value, opcode.value)

    return register_values

# TODO: this needs to be very thoroughly unit-tested
def _apply_opcode(register_value:int, opcode:OpCode):
    '''
    Generates an update code for a specific register by applying an opcode

    Args:
        opcode (OpCode): an OpCode object representing the opcode to be applied to the register

        register_value (int): the current stored value of the register

    Returns:
        an update code, the value to be written back to the register in order to apply
        the opcode.
    '''
    # TODO: input validation for op_code: negate op_mask + AND with op_code
    # to ensure op_code only writes to desired bits

    register_value &= opcode.op_mask    # clear the bits to be overwritten
    register_value |= opcode.op_code    # apply the opcode opcode to the cleared bits
    
    return register_value
