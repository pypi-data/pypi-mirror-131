from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserLicenseMeterAttributeDto")


@attr.s(auto_attribs=True)
class UserLicenseMeterAttributeDto:
    """ """

    name: Union[Unset, None, str] = UNSET
    allowed_uses: Union[Unset, int] = UNSET
    total_uses: Union[Unset, int] = UNSET
    gross_uses: Union[Unset, int] = UNSET
    floating: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        allowed_uses = self.allowed_uses
        total_uses = self.total_uses
        gross_uses = self.gross_uses
        floating = self.floating

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if allowed_uses is not UNSET:
            field_dict["allowedUses"] = allowed_uses
        if total_uses is not UNSET:
            field_dict["totalUses"] = total_uses
        if gross_uses is not UNSET:
            field_dict["grossUses"] = gross_uses
        if floating is not UNSET:
            field_dict["floating"] = floating

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        allowed_uses = d.pop("allowedUses", UNSET)

        total_uses = d.pop("totalUses", UNSET)

        gross_uses = d.pop("grossUses", UNSET)

        floating = d.pop("floating", UNSET)

        user_license_meter_attribute_dto = cls(
            name=name,
            allowed_uses=allowed_uses,
            total_uses=total_uses,
            gross_uses=gross_uses,
            floating=floating,
        )

        return user_license_meter_attribute_dto
