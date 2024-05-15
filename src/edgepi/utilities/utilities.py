""" utility module for general purpose functions and classes

    Functions:
        filter_dict(dict, any)
        bitstring_from_list(list)
"""

from bitstring import BitArray

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


def filter_dict_list_key_val(dictionary: dict, entry_key: list, entry_val:list) -> dict:
    """use for filtering an entry from a dictionary by key or value

    Args:
        dictionary (dict): any dictionary whose entries are to be filtered

        entry_key (list): list of the key of the entry to filter out

        entry_val (list): list of the value of the entry or entries to filter out

    Returns:
        a dictionary of entries from the original dictionary, after filtering out entries whose
        key or value matches either the entry_key or entry_val, respectively.
    """
    filtered_args = {
        key: value for (key, value) in dictionary.items() \
        if key not in entry_key and value not in entry_val
    }
    return filtered_args


def bitstring_from_list(data: list[int]) -> BitArray:
    """
    Builds a bitstring from a list of uint byte values

    Args:
        data (List[int]): a list of uint byte values

    Returns:
        BitArray: bitstring of bytes ordered from data[0], data[1], ..., data[n-1]
    """
    # bytes() will raise a ValueError if any items are not in the range [0, 255]
    return BitArray(bytes(data))


def combine_to_uint32(a:int, b:int, c:int, d:int) -> int:
    return (a << 24) + (b << 16) + (c << 8) + d
