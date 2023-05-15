""" Digital Output Constants """


from enum import Enum, unique

@unique
class LEDPins(Enum):
    """GPIO Pin Names"""

    LED_OVR1 = 'LED_OVR1'
    LED_OVR2 = 'LED_OVR2'
    LED_OVR3 = 'LED_OVR3'
    LED_OVR4 = 'LED_OVR4'
    LED_OVR5 = 'LED_OVR5'
    LED_OVR6 = 'LED_OVR6'
    LED_OVR7 = 'LED_OVR7'
    LED_OVR8 = 'LED_OVR8'
