""" Utility module for issuing commands to GPIO devices """


from edgepi.gpio.gpio_configs import GpioConfigs


def get_periph_config(config: str = None):
    """Used to get proper config dataclass to configure neccessary peripheral configuration"""
    for periphery_config in GpioConfigs:
        if config == periphery_config.value.name:
            return periphery_config.value
    return None
