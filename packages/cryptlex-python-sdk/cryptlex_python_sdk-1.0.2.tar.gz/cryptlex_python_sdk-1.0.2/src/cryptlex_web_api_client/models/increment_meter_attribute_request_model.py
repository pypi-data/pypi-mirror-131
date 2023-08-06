from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IncrementMeterAttributeRequestModel")


@attr.s(auto_attribs=True)
class IncrementMeterAttributeRequestModel:
    """ """

    increment: Union[Unset, int] = UNSET
    activation_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        increment = self.increment
        activation_id = self.activation_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if increment is not UNSET:
            field_dict["increment"] = increment
        if activation_id is not UNSET:
            field_dict["activationId"] = activation_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        increment = d.pop("increment", UNSET)

        activation_id = d.pop("activationId", UNSET)

        increment_meter_attribute_request_model = cls(
            increment=increment,
            activation_id=activation_id,
        )

        return increment_meter_attribute_request_model
