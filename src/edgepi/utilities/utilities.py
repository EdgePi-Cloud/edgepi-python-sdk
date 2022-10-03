""" utility module for general purpose functions and classes

    Functions:
        filter_dict(dict, any)
        bitstring_from_list(list)
"""


from bitstring import BitArray, pack


def filter_dict(dictionary: dict, entry_key="", entry_val="") -> dict:
    """use for filtering an entry from a dictionary by key or value

    Args:
        dictionary (dict): any dictionary whose entries are to be filtered

        entry_key (any): the key of the entry to filter out

        entry_val (any): the value of the entry or entries to filter out

    Returns:
        a dictionary of entries from the original dictionary, after filtering out entries whose
        key or value matches either the entry_key or entry_val, respectively.
    """
    filtered_args = {
        key: value for (key, value) in dictionary.items() if key != entry_key and value != entry_val
    }
    return filtered_args


def bitstring_from_list(data: list) -> BitArray:
    """
    Builds a bitstring from a list of uint byte values

    Args:
        data (List[int]): a list of uint byte values

    Returns:
        BitArray: bitstring of bytes ordered from data[0], data[1], ..., data[n-1]
    """
    code = BitArray()
    for value in data:
        next_byte = pack("uint:8", value)
        code.append(next_byte)
    return code
