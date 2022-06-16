''' utility module for general purpose functions and classes

    Functions:
        filter_dict(dict, any)
'''

def filter_dict(dictionary:dict, keyword) -> list:
    ''' use for filtering an entry from a dictionary by key

        Args:
            dictionary (dict): any dictionary whose entries are to be filtered

        Returns:
            a list of values from the dictionary, with the entry whose key is the keyword, filtered out.
    '''
    filtered_args = { key:value for (key,value) in dictionary.items() if key != keyword }
    return list(filtered_args.values())
