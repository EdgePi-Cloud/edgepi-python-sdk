""" Digital Input Constants """


from enum import Enum, unique

@unique
class DinPins(Enum):
    """Digital Input Gpio Pin Names"""

    DIN1 = 'DIN1'
    DIN2 = 'DIN2'
    DIN3 = 'DIN3'
    DIN4 = 'DIN4'
    DIN5 = 'DIN5'
    DIN6 = 'DIN6'
    DIN7 = 'DIN7'
    DIN8 = 'DIN8'
