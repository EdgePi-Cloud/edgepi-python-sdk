"""helper module to read serialized byte string"""
import os
PATH = os.path.dirname(os.path.abspath(__file__))

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/edgepi_default_bin","rb") as fd:
        b_string = fd.read()
    return b_string
