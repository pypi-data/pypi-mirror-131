from enum import Enum


class LicenseDtoExpirationStrategy(str, Enum):
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
    ROLLING = "rolling"

    def __str__(self) -> str:
        return str(self.value)
