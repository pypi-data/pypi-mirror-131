from enum import Enum


class LicenseDtoType(str, Enum):
    NODE_LOCKED = "node-locked"
    HOSTED_FLOATING = "hosted-floating"
    ON_PREMISE_FLOATING = "on-premise-floating"

    def __str__(self) -> str:
        return str(self.value)
