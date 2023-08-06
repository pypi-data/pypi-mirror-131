from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangesDto")


@attr.s(auto_attribs=True)
class ChangesDto:
    """ """

    property_name: Union[Unset, None, str] = UNSET
    old_value: Union[Unset, Any] = UNSET
    new_value: Union[Unset, Any] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        property_name = self.property_name
        old_value = self.old_value

        new_value = self.new_value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if property_name is not UNSET:
            field_dict["propertyName"] = property_name
        if old_value is not UNSET:
            field_dict["oldValue"] = old_value
        if new_value is not UNSET:
            field_dict["newValue"] = new_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        property_name = d.pop("propertyName", UNSET)

        old_value = d.pop("oldValue", UNSET)

        new_value = d.pop("newValue", UNSET)

        changes_dto = cls(
            property_name=property_name,
            old_value=old_value,
            new_value=new_value,
        )

        return changes_dto
