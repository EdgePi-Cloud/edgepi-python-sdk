from enum import Enum

class EDGEPI_TC_ADDRESSES(Enum):
    # Read addresses
    CR0_R = 0x00
    CR1_R = 0x01
    MASK_R = 0x02
    CJHF_R = 0x03
    CJLF_R = 0x04
    LTHFTH_R = 0x05
    LTHFTL_R = 0x06
    LTLFTH_R = 0x07
    LTLFTL_R = 0x08
    CJTO_R = 0x09
    CJTH_R = 0x0A
    CJTL_R = 0x0B
    LTCBH_R = 0x0C
    LTCBM_R = 0x0D
    LTCBL_R = 0x0E
    SR_R = 0x0F

    # Write addresses
    CR0_W = 0x80
    CR1_W = 0x81
    MASK_W = 0x82
    CJHF_W = 0x83
    CJLF_W = 0x84
    LTHFTH_W = 0x85
    LTHFTL_W = 0x86
    LTLFTH_W = 0x87
    LTLFTL_W = 0x88
    CJTO_W = 0x89
    CJTH_W = 0x8A
    CJTL_W = 0x8B

class EDGEPI_TC_COMMANDS(Enum):
    # CR0 opcodes
    CMODE_SINGLE = 0x40   # single-shot conversion mode
    CMODE_AUTO = 0x80     # continuous conversion mode
    FMODE_COMP = 0x00     # comparator fault mode
    FMODE_INTRPT = 0x04   # interrupt fault mode
    CJ_ENABLE = 0x00      # enable cold-junction sensor
    CJ_DISABLE = 0x08     # disable cold-junction sensor

    # CR1 opcodes
    AVGMODE_1 = 0x03       # single sample
    AVGMODE_2 = 0x13       # 2 samples averaged
    AVGMODE_4 = 0x23       # 4 samples averaged
    AVGMODE_8 = 0x33       # 8 samples averaged
    AVGMODE_16 = 0x43      # 16 samples averaged
