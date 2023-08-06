from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TwoFactorSecretDto")


@attr.s(auto_attribs=True)
class TwoFactorSecretDto:
    """ """

    email: Union[Unset, None, str] = UNSET
    url: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        url = d.pop("url", UNSET)

        two_factor_secret_dto = cls(
            email=email,
            url=url,
        )

        return two_factor_secret_dto
