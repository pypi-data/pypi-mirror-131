from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccessTokenDto")


@attr.s(auto_attribs=True)
class AccessTokenDto:
    """ """

    access_token: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if access_token is not UNSET:
            field_dict["accessToken"] = access_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access_token = d.pop("accessToken", UNSET)

        access_token_dto = cls(
            access_token=access_token,
        )

        return access_token_dto
