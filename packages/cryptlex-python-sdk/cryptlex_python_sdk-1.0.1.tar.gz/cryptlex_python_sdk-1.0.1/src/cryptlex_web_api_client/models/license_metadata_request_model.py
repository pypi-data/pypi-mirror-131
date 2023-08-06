from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="LicenseMetadataRequestModel")


@attr.s(auto_attribs=True)
class LicenseMetadataRequestModel:
    """ """

    key: str
    value: str
    visible: bool

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        value = self.value
        visible = self.visible

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "key": key,
                "value": value,
                "visible": visible,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        value = d.pop("value")

        visible = d.pop("visible")

        license_metadata_request_model = cls(
            key=key,
            value=value,
            visible=visible,
        )

        return license_metadata_request_model
