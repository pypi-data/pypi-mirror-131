from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ActivationMeterAttributeRequestModel")


@attr.s(auto_attribs=True)
class ActivationMeterAttributeRequestModel:
    """ """

    name: str
    uses_increment: int

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        uses_increment = self.uses_increment

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "usesIncrement": uses_increment,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        uses_increment = d.pop("usesIncrement")

        activation_meter_attribute_request_model = cls(
            name=name,
            uses_increment=uses_increment,
        )

        return activation_meter_attribute_request_model
