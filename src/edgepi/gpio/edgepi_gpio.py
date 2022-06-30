'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''

import logging
import time

from edgepi.peripherals.gpio import GpioDevice
from edgepi.peripherals.i2c import I2CDevice
from edgepi.gpio.gpio_commands import *

from edgepi.reg_helper.reg_helper import apply_opcodes

_logger = logging.getLogger(__name__)

class EdgePiGPIO(I2CDevice):
    ''' 
    A class used to represent the GPIO. This class will be imported to each module
    that requires GPIO manipulation. It is not intended for user.
    '''
    
    def __init__(self, config: str = None):
        if config is None:
            _logger.error(f'Config is not chosen, please choose a configuration')
        self.config = getPeriphConfig(config)
        _logger.debug(f'{self.config.name} Configuration Selected: {self.config}')
        if self.config is not None and 'i2c' in self.config.dev_path:
            super().__init__(self.config.dev_path)
            _logger.info(f'GPIO expander up and running')
            self.pinList = generate_pin_info(self.config.name)
            self.pinConfigAddress, self.pinOutAddress = getPinConfigAddress(self.config)

    
    def set_expander_default(self):
        ''' 
        function to set the pins to default configuration
        Note: always toggle output state first before changing the pin direction
        '''
        reg_dict = getDefaultValues(self.__reg_addressToValue_dict(), self.pinList)
        
        self.transfer(self.config.address.value, self.setWriteMsg(self.pinOutAddress, pinOutVal))
        self.transfer(self.config.address.value, self.setWriteMsg(self.pinConfigAddress, pinDirVal))
        pinOutVal = self.transfer(self.config.address.value, self.setReadMsg(self.pinOutAddress, [0xFF]))
        pinDirVal = self.transfer(self.config.address.value, self.setReadMsg(self.pinConfigAddress, [0xFF]))
        # TODO: check if writing was successfull
    
    def __read_register(self, address):
        ''' 
        function to read one register value
        Returns:
            A byte data
        '''
        _logger.debug(f'Reading a register value')
        msgRead = self.setReadMsg(address, [0xFF])
        _logger.debug(f'Read Message: Register Address {msgRead[0].data}, Msg Place Holder {msgRead[1].data}')
        self.transfer(self.config.address.value, msgRead)
        _logger.debug(f'Message Read: Register Address {msgRead[0].data}, Msg Place Holder {msgRead[1].data}')
        return msgRead[1].data[0]

    def __reg_addressToValue_dict(self):
        ''' 
        Function to map address : value dictionary
        Returns:
            Dictionary containing address : value
        '''
        _logger.info(f'Mapping a register addree : register value')
        reg_map = {}
        reg_map[self.pinOutAddress] = self.__read_register(self.pinOutAddress)
        reg_map[self.pinConfigAddress] = self.__read_register(self.pinConfigAddress)
        return reg_map