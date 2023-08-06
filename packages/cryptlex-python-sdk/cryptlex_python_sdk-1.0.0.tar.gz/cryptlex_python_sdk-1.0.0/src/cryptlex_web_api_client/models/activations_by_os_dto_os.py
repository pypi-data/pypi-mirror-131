from enum import Enum


class ActivationsByOsDtoOs(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    ANDROID = "android"
    IOS = "ios"

    def __str__(self) -> str:
        return str(self.value)
