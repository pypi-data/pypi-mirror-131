from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3RolesJsonBody")


@attr.s(auto_attribs=True)
class Postv3RolesJsonBody:
    """ """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    claims: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        claims: Union[Unset, List[str]] = UNSET
        if not isinstance(self.claims, Unset):
            claims = self.claims

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if claims is not UNSET:
            field_dict["claims"] = claims

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        claims = cast(List[str], d.pop("claims", UNSET))

        postv_3_roles_json_body = cls(
            name=name,
            description=description,
            claims=claims,
        )

        postv_3_roles_json_body.additional_properties = d
        return postv_3_roles_json_body

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
