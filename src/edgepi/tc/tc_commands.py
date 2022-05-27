
class TCCommands():
    def __init__(self, cs_line):
        self.cs = cs_line

    def read_register(self):
        ''' read the value of any MAX31856 register '''
        pass

    def write_to_register(self):
        ''' write to any MAX31856 register '''
        pass

    def temp_to_code(self, temp:float):
        ''' converts a float temperature value to binary code for writing to register '''
        pass

    def code_to_temp(self, code):
        ''' converty register binary temperature code to float value'''
        pass
