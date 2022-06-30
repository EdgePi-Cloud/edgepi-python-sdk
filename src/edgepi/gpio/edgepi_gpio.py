'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''

import logging
import time
from copy import deepcopy

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
            self.listRegDict = []

    def generate_default_reg_dict(self):
        ''' 
        Function to generate a list of default register dictionary
        Return:
            list of register dictionary [{register address : register value}]
            list of pin list
        '''
        pinLists = checkMultipleDev(self.pinList)
        listRegDict=[]
        for pinList in pinLists:
            if pinList:
                listRegDict.append(deepcopy(self._reg_addressToValue_dict(pinList[0].address)))
            else:
                listRegDict.append(None)
        return listRegDict, pinLists

    def set_expander_default(self):
        ''' 
        function to set the pins to default configuration
        Note: always toggle output state first before changing the pin direction
        Return:
            listDefaultRegDict: list of dictionary that includes default regsister address : value pair
        '''
        
        listDefaultRegDict, pinLists = self.generate_default_reg_dict()
        listRegDict = []
        for defaultRegDict in listDefaultRegDict:
            listRegDict.append(deepcopy(defaultRegDict))
        for regDict, pinList, defaultRegDict in zip(listRegDict, pinLists, listDefaultRegDict):
            if not pinList:
                continue
            dev_address = pinList[0].address
            regDict = getDefaultValues(regDict, pinList)
            
            for reg_addx, entry in regDict.items():
                if entry['is_changed']:
                    msgwrite = self.setWriteMsg(reg_addx, [entry['value']])
                    self.transfer(dev_address, msgwrite)

            for reg_address, value in defaultRegDict.items():
                defaultRegDict[reg_address] = self.transfer(dev_address, self.setReadMsg(reg_address, [value]))
        return listDefaultRegDict
    
    def read_register(self, reg_address, dev_address):
        ''' 
        function to read one register value
        In:
            reg_address: register address to read data from
            dev_address: expander address to read 
        Returns:
            A byte data
        '''
        _logger.debug(f'Reading a register value')
        msgRead = self.setReadMsg(reg_address, [0xFF])
        _logger.debug(f'Read Message: Register Address {msgRead[0].data}, Msg Place Holder {msgRead[1].data}')
        self.transfer(dev_address, msgRead)
        _logger.debug(f'Message Read: Register Address {msgRead[0].data}, Msg Place Holder {msgRead[1].data}')
        return msgRead[1].data[0]

    def reg_addressToValue_dict(self, dev_address):
        ''' 
        Function to map address : value dictionary
        In:
            dev_address: expander address to read 
        Returns:
            Dictionary containing address : value
        '''
        _logger.info(f'Mapping a register addree : register value')
        reg_map = {}
        reg_map[self.pinOutAddress] = self._read_register(self.pinOutAddress, dev_address)
        reg_map[self.pinConfigAddress] = self._read_register(self.pinConfigAddress, dev_address)
        return reg_map