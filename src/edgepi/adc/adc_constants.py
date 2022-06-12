from enum import Enum, unique

@unique
class EDGEPI_ADC_OP(Enum):
    OP_NOP = 0x00
    OP_RESET = 0x06
    OP_START1 = 0x09
    OP_STOP1 = 0x0A
    OP_START2 = 0x0C
    OP_STOP2 = 0x0E
    OP_RDATA1 = 0x12
    OP_RDATA2 = 0x14
    OP_SYOCAL1 = 0x16
    OP_SYGCAL1 = 0x17
    OP_SFOCAL1 = 0x19
    OP_SYOCAL2 = 0x1B
    OP_SYGCAL2 = 0x1C
    OP_SFOCAL2 = 0x1E
    OP_RREG = 0x20
    OP_WREG = 0x40

@unique
class EDGEPI_ADC_REG(Enum):
    REG_ID = 0X00
    REG_POWER = 0X01
    REG_INTERFACE = 0X02
    REG_MODE0 = 0X03
    REG_MODE1 = 0X04
    REG_MODE2 = 0X05
    REG_INPMUX = 0X06
    REG_OFCAL0 = 0X07
    REG_OFCAL1 = 0X08
    REG_OFCAL2 = 0X09
    REG_FSCAL0 = 0X0A
    REG_FSCAL1 = 0X0B
    REG_FSCAL2 = 0X0C
    REG_IDACMUX = 0X0D
    REG_IDACMAG = 0X0E
    REG_REFMUX = 0X0F
    REG_TDACP = 0X10
    REG_TDACN = 0X11
    REG_GPIOCON = 0X12
    REG_GPIODIR = 0X13
    REG_GPIODAT = 0X14
    REG_ADC2CFG = 0X15
    REG_ADC2MUX = 0X16
    REG_ADC2OFC0 = 0X17
    REG_ADC2OFC1 = 0X18
    REG_ADC2FSC0 = 0X19
    REG_ADC2FSC1 = 0X1A

@unique
class EDGEPI_ADC_CHANNEL(Enum):
    AIN0 = 0
    AIN1 = 1
    AIN2 = 2
    AIN3 = 3
    AIN4 = 4
    AIN5 = 5
    AIN6 = 6
    AIN7 = 7
    AIN8 = 8
    AIN9 = 9
    AINCOM = 10