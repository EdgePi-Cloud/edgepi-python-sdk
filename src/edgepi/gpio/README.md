# EdgePi GPIO Module Guide
GPIO module is intended to be used inside other modules that requires GPIO control. For example, DAC requires AO_ENx pins to be set high to propagate it's output voltage to the corresponding terminal block pin. RTD module requires RTD_EN pin to be set high to configure the internal RTD circuitry.
## Quick Use Example
This section demonstartes the use case of this module.

### Import and Initialization
```python
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.edgpio_config import GpioConfigs

#initialize gpio for DAC
edgepi_gpio = EdgePiGPIO(GpioConfigs.DAC.value)

#initialize gpio for ADC
edgepi_gpio = EdgePiGPIO(GpioConfigs.ADC.value)

#initialize gpio for RTD
edgepi_gpio = EdgePiGPIO(GpioConfigs.RTD.value)

#initialize gpio for LED
edgepi_gpio = EdgePiGPIO(GpioConfigs.LED.value)
```

### Set Default State
```python
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.edgpio_config import GpioConfigs

#initialize gpio for DAC
edgepi_gpio = EdgePiGPIO(GpioConfigs.DAC.value)

#set default gpio state
edgepi_gpio.set_expander_default()
```

### Set Expander Pin
```python
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.edgpio_config import GpioConfigs

#initialize gpio for DAC
edgepi_gpio = EdgePiGPIO(GpioConfigs.DAC.value)

#set default gpio state
edgepi_gpio.set_expander_default()

#set expander pin
edgepi_gpio.set_expander_pi('AO_EN2')
```

### clear Expander Pin
```python
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.edgpio_config import GpioConfigs

#initialize gpio for DAC
edgepi_gpio = EdgePiGPIO(GpioConfigs.DAC.value)

#set default gpio state
edgepi_gpio.set_expander_default()

#clear expander pin
edgepi_gpio.clear_expander_pi('AO_EN2')
```

### Toggle Expander Pin
```python
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.edgpio_config import GpioConfigs

#initialize gpio for DAC
edgepi_gpio = EdgePiGPIO(GpioConfigs.DAC.value)

#set default gpio state
edgepi_gpio.set_expander_default()

#Toggle expander pin
edgepi_gpio.Toggle_expander_pi('AO_EN2')
```

## Using GPIO Module

### DAC pin to GPIO pin
|DAC|GPIO|TB_Block|
|---|---|---|
|VOUT0|AO_EN1|A/DOUT1|
|VOUT1|AO_EN2|A/DOUT2|
|VOUT2|AO_EN3|A/DOUT3|
|VOUT3|AO_EN4|A/DOUT4|
|VOUT4|AO_EN5|A/DOUT5|
|VOUT5|AO_EN6|A/DOUT6|
|VOUT6|AO_EN7|A/DOUT7|
|VOUT7|AO_EN8|A/DOUT8|
|DAC_GAIN|DAC_GAIN||
