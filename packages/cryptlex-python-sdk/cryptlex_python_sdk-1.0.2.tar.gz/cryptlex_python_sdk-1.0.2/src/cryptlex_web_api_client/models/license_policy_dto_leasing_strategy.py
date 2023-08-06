from enum import Enum


class LicensePolicyDtoLeasingStrategy(str, Enum):
    PER_MACHINE = "per-machine"
    PER_INSTANCE = "per-instance"

    def __str__(self) -> str:
        return str(self.value)
