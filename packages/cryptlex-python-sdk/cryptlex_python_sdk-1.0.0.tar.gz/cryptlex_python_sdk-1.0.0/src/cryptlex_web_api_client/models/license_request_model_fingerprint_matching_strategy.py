from enum import Enum


class LicenseRequestModelFingerprintMatchingStrategy(str, Enum):
    FUZZY = "fuzzy"
    EXACT = "exact"
    LOOSE = "loose"

    def __str__(self) -> str:
        return str(self.value)
