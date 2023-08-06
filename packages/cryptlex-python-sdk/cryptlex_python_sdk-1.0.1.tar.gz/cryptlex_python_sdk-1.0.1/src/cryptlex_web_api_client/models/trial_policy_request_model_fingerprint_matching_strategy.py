from enum import Enum


class TrialPolicyRequestModelFingerprintMatchingStrategy(str, Enum):
    FUZZY = "fuzzy"
    EXACT = "exact"
    LOOSE = "loose"

    def __str__(self) -> str:
        return str(self.value)
