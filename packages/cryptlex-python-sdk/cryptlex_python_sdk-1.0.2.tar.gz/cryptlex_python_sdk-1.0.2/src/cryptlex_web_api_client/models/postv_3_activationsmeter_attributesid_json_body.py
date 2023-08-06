from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3ActivationsmeterAttributesidJsonBody")


@attr.s(auto_attribs=True)
class Postv3ActivationsmeterAttributesidJsonBody:
    """ """

    increment: Union[Unset, int] = UNSET
    activation_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        increment = self.increment
        activation_id = self.activation_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        postv_3_activationsmeter_attributesid_json_body = cls(
            increment=increment,
            activation_id=activation_id,
        )

        postv_3_activationsmeter_attributesid_json_body.additional_properties = d
        return postv_3_activationsmeter_attributesid_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
