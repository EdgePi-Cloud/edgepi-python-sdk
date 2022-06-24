''' utility module for general purpose functions and classes

    Functions:
        filter_dict(dict, any)
'''

def filter_dict(dictionary:dict, keyword) -> dict:
    ''' use for filtering an entry from a dictionary by key

        Args:
            dictionary (dict): any dictionary whose entries are to be filtered

        Returns:
            a dictionary of entries from the original dictionary, after filtering out the entry whose key is the keyword.
    '''
    filtered_args = { key:value for (key,value) in dictionary.items() if key != keyword }
    return(filtered_args)
