'''
Helper functions and class for modifying device register values

Classes:

    OpCode

Functions:

    apply_opcodes(dict, list)
    apply_opcode(object, int)
'''

from dataclasses import dataclass

@dataclass(frozen=True)
class OpCode:
    '''
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

            (0b0000 1101) | (0b0110 1101) = (0b0110 1101)
    '''
    op_code: int
    reg_address: int
    op_mask: int

class OpCodeMaskIncompatibleError(ValueError):
    '''Raised when an OpCode contains an op_code which affects bits not covered by the op_mask'''
    def __init__(self, opcode, mask):
        self.opcode = opcode
        self.mask = mask
    
    def __str__(self):
        return f'opcode ({hex(self.opcode)}) affects bits not covered by mask ({hex(self.mask)})'


def _add_change_flags(register_values:dict):
    '''
        adds flags to register values for checking to see if register value has been modified later

        Args:
            register_values (dict): a map of the device's registers to their current values
    '''
    for key in register_values:
        register_values[key]['flag'] = False

# TODO: make more efficient by grouping by address
def apply_opcodes(register_values:dict, opcodes:list):
    '''
    Generates updated register values after applying opcodes, and sets flag for updated registers

    Args:
        register_values (dict): a map of the device's registers to a dictionary containing the register value
                                and the change flag. The dictionary must contain entries of the form 
                                register_address: {'value': register_value}.

        updates (list): a list of valid Enum objects representing opcodes to be applied to registers.
                        See tc_constants.py for for a valid Enums.

    Returns:
        a map of the device's registers to a dictionary containg the updated values and change flags

    Raises:
        ValueError: if either register_values or opcodes is empty
    '''
    if len(register_values) < 1 or len(opcodes) < 1:
        raise ValueError('register_values and opcodes args must both be non-empty')
    _add_change_flags(register_values)

    # apply each opcode to its corresponding register
    for opcode in opcodes:
        if opcode is None:
            continue
        register_entry = register_values.get(opcode.value.reg_address)
        # if this opcode maps to a valid register address
        if register_entry is not None:
            # apply the opcode to the register
            register_entry['value'] = _apply_opcode(register_entry['value'], opcode.value)
            register_entry['flag'] = True

    return register_values

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
    # ensure op_code only writes to bits of register covered by mask
    # second conditional is to permit edge-case where opcode is 0x00, i.e. 
    # 'do not modify any bits' instruction.
    if (~opcode.op_mask & opcode.op_code) != opcode.op_code:
        raise OpCodeMaskIncompatibleError(opcode.op_code, opcode.op_mask)

    register_value &= opcode.op_mask    # clear the bits to be overwritten
    register_value |= opcode.op_code    # apply the opcode opcode to the cleared bits
   
    return register_value


def filter_dict(locals_dict:dict, keyword:str) -> list:
    ''' use for filtering the self argument from a function's locals() dictionary

        Args:
            locals_dict (dict): the dictionary obtained by calling locals() in the function

        Returns:
            a list of values from the locals() dictionary, with the self entry filtered out
    '''
    filtered_args = { key:value for (key,value) in locals_dict.items() if key != keyword }
    return filtered_args.values()
