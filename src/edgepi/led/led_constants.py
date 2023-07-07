""" Digital Output Constants """


from enum import Enum, unique

@unique
class LEDPins(Enum):
    """LED Gpio Pin Names"""

    LED1 = 'LED_OVR1'
    LED2 = 'LED_OVR2'
    LED3 = 'LED_OVR3'
    LED4 = 'LED_OVR4'
    LED5 = 'LED_OVR5'
    LED6 = 'LED_OVR6'
    LED7 = 'LED_OVR7'
    LED8 = 'LED_OVR8'
