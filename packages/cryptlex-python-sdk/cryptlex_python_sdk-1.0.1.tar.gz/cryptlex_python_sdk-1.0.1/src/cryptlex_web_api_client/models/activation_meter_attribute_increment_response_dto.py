from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationMeterAttributeIncrementResponseDto")


@attr.s(auto_attribs=True)
class ActivationMeterAttributeIncrementResponseDto:
    """ """

    name: Union[Unset, None, str] = UNSET
    uses: Union[Unset, int] = UNSET
    license_allowed_uses: Union[Unset, int] = UNSET
    license_total_uses: Union[Unset, int] = UNSET
    license_gross_uses: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        uses = self.uses
        license_allowed_uses = self.license_allowed_uses
        license_total_uses = self.license_total_uses
        license_gross_uses = self.license_gross_uses

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if uses is not UNSET:
            field_dict["uses"] = uses
        if license_allowed_uses is not UNSET:
            field_dict["licenseAllowedUses"] = license_allowed_uses
        if license_total_uses is not UNSET:
            field_dict["licenseTotalUses"] = license_total_uses
        if license_gross_uses is not UNSET:
            field_dict["licenseGrossUses"] = license_gross_uses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        uses = d.pop("uses", UNSET)

        license_allowed_uses = d.pop("licenseAllowedUses", UNSET)

        license_total_uses = d.pop("licenseTotalUses", UNSET)

        license_gross_uses = d.pop("licenseGrossUses", UNSET)

        activation_meter_attribute_increment_response_dto = cls(
            name=name,
            uses=uses,
            license_allowed_uses=license_allowed_uses,
            license_total_uses=license_total_uses,
            license_gross_uses=license_gross_uses,
        )

        return activation_meter_attribute_increment_response_dto
