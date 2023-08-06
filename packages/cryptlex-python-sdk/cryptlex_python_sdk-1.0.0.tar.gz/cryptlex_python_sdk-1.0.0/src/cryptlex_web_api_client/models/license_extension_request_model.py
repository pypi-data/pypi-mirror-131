from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseExtensionRequestModel")


@attr.s(auto_attribs=True)
class LicenseExtensionRequestModel:
    """ """

    extension_length: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        extension_length = self.extension_length

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if extension_length is not UNSET:
            field_dict["extensionLength"] = extension_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        extension_length = d.pop("extensionLength", UNSET)

        license_extension_request_model = cls(
            extension_length=extension_length,
        )

        return license_extension_request_model
