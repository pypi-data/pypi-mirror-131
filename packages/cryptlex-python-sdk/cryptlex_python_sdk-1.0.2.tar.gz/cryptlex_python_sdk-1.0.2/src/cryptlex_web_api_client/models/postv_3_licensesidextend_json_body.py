from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3LicensesidextendJsonBody")


@attr.s(auto_attribs=True)
class Postv3LicensesidextendJsonBody:
    """ """

    extension_length: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        extension_length = self.extension_length

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if extension_length is not UNSET:
            field_dict["extensionLength"] = extension_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        extension_length = d.pop("extensionLength", UNSET)

        postv_3_licensesidextend_json_body = cls(
            extension_length=extension_length,
        )

        postv_3_licensesidextend_json_body.additional_properties = d
        return postv_3_licensesidextend_json_body

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
