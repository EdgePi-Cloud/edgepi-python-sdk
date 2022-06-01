from edgepi.tc.tc_constants import TCAddresses

mock_register_values = {
                        TCAddresses.CR0_R.value: 0x00,
                        TCAddresses.CR1_R.value: 0x03,
                        TCAddresses.MASK_R.value: 0xFF,
                        TCAddresses.CJHF_R.value: 0x7F,
                        TCAddresses.CJLF_R.value: 0xC0,
                        TCAddresses.LTHFTH_R.value: 0x7F,
                        TCAddresses.LTHFTL_R.value: 0xFF,
                        TCAddresses.LTLFTH_R.value: 0x80,
                        TCAddresses.LTLFTL_R.value: 0x00,
                        TCAddresses.CJTO_R.value: 0x00, 
                        TCAddresses.CJTH_R.value: 0x00,
                        TCAddresses.CJTL_R.value: 0x00,
                        TCAddresses.LTCBH_R.value: 0x00,
                        TCAddresses.LTCBM_R.value: 0x00,
                        TCAddresses.LTCBL_R.value: 0x00,
                        TCAddresses.SR_R.value: 0x00
                        }

def mock_MAX31856_transfer(data):
    ''' mocks SPI transfer of register data from MAX31856 
    Returns:
        a list of register values starting from start address (data[0]).
    '''
    if not data:
        raise ValueError('Cannot transfer empty data container')
    elif len(data) < 2:
        raise ValueError('Only address provided, no read bytes specified')

    out_data = data
    bytes_to_read = len(data) - 1
    reg_addx = data[0].value # start address 
    reg_index = 1
    while bytes_to_read > 0:
        out_data[reg_index] = mock_register_values.get(reg_addx)
        reg_index += 1
        reg_addx += 1
        bytes_to_read -= 1
    return out_data
    