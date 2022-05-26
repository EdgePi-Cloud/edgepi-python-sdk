from dataclasses import dataclass

# TODO: rev_id can be differ by chips, only manufacurer has control over it
@dataclass(frozen=True)
class AdcRegID:
    dev_id: int = 1
    rev_id: int = 0

    def get_value(self)-> int:
        return self.dev_id<<5 | self.rev_id<<0

@dataclass
class AdcRegPower:
    reset: int = 1
    vbias: int = 0
    intref: int = 1

    def get_value(self) -> int:
        return self.reset<<4 | self.vbias<<1 | self.intref<<0

