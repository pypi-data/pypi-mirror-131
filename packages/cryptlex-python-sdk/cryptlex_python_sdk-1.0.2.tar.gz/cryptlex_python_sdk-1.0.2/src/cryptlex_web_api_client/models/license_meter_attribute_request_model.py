from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseMeterAttributeRequestModel")


@attr.s(auto_attribs=True)
class LicenseMeterAttributeRequestModel:
    """ """

    name: str
    allowed_uses: int
    visible: Union[Unset, None, bool] = UNSET
    floating: Union[Unset, None, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        allowed_uses = self.allowed_uses
        visible = self.visible
        floating = self.floating

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "allowedUses": allowed_uses,
            }
        )
        if visible is not UNSET:
            field_dict["visible"] = visible
        if floating is not UNSET:
            field_dict["floating"] = floating

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        allowed_uses = d.pop("allowedUses")

        visible = d.pop("visible", UNSET)

        floating = d.pop("floating", UNSET)

        license_meter_attribute_request_model = cls(
            name=name,
            allowed_uses=allowed_uses,
            visible=visible,
            floating=floating,
        )

        return license_meter_attribute_request_model
