from enum import Enum


class LicensePolicyRequestModelFingerprintMatchingStrategy(str, Enum):
    FUZZY = "fuzzy"
    EXACT = "exact"
    LOOSE = "loose"

    def __str__(self) -> str:
        return str(self.value)
