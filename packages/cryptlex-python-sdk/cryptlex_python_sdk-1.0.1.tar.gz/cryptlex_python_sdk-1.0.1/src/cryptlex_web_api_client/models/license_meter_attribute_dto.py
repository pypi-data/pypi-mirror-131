import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseMeterAttributeDto")


@attr.s(auto_attribs=True)
class LicenseMeterAttributeDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    allowed_uses: Union[Unset, int] = UNSET
    total_uses: Union[Unset, int] = UNSET
    gross_uses: Union[Unset, int] = UNSET
    floating: Union[Unset, bool] = UNSET
    visible: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        name = self.name
        allowed_uses = self.allowed_uses
        total_uses = self.total_uses
        gross_uses = self.gross_uses
        floating = self.floating
        visible = self.visible

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
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
        if visible is not UNSET:
            field_dict["visible"] = visible

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        name = d.pop("name", UNSET)

        allowed_uses = d.pop("allowedUses", UNSET)

        total_uses = d.pop("totalUses", UNSET)

        gross_uses = d.pop("grossUses", UNSET)

        floating = d.pop("floating", UNSET)

        visible = d.pop("visible", UNSET)

        license_meter_attribute_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            allowed_uses=allowed_uses,
            total_uses=total_uses,
            gross_uses=gross_uses,
            floating=floating,
            visible=visible,
        )

        return license_meter_attribute_dto
