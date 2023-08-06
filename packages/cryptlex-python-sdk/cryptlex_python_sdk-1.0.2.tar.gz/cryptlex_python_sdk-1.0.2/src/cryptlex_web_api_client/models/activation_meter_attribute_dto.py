from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationMeterAttributeDto")


@attr.s(auto_attribs=True)
class ActivationMeterAttributeDto:
    """ """

    name: Union[Unset, None, str] = UNSET
    uses: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        uses = self.uses

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if uses is not UNSET:
            field_dict["uses"] = uses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        uses = d.pop("uses", UNSET)

        activation_meter_attribute_dto = cls(
            name=name,
            uses=uses,
        )

        return activation_meter_attribute_dto
