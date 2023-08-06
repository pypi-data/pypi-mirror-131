from enum import Enum


class LicensePolicyRequestModelExpirationStrategy(str, Enum):
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
    ROLLING = "rolling"

    def __str__(self) -> str:
        return str(self.value)
