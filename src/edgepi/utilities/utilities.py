""" utility module for general purpose functions and classes

    Functions:
        filter_dict(dict, any)
"""


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
