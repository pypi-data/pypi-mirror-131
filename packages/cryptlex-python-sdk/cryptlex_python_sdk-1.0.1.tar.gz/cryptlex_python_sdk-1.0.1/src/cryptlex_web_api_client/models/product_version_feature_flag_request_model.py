from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProductVersionFeatureFlagRequestModel")


@attr.s(auto_attribs=True)
class ProductVersionFeatureFlagRequestModel:
    """ """

    name: str
    enabled: bool
    data: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        enabled = self.enabled
        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "enabled": enabled,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        enabled = d.pop("enabled")

        data = d.pop("data", UNSET)

        product_version_feature_flag_request_model = cls(
            name=name,
            enabled=enabled,
            data=data,
        )

        return product_version_feature_flag_request_model
