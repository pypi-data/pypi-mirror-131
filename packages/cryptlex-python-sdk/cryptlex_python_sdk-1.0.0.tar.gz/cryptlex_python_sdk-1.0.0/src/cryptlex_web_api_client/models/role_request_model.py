from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleRequestModel")


@attr.s(auto_attribs=True)
class RoleRequestModel:
    """ """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    claims: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        claims: Union[Unset, List[str]] = UNSET
        if not isinstance(self.claims, Unset):
            claims = self.claims

        field_dict: Dict[str, Any] = {}
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

        role_request_model = cls(
            name=name,
            description=description,
            claims=claims,
        )

        return role_request_model
