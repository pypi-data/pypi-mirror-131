from enum import Enum


class LicensePolicyRequestModelLeasingStrategy(str, Enum):
    PER_MACHINE = "per-machine"
    PER_INSTANCE = "per-instance"

    def __str__(self) -> str:
        return str(self.value)
