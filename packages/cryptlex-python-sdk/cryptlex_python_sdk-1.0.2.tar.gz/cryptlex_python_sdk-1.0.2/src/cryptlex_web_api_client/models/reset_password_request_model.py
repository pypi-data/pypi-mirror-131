from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResetPasswordRequestModel")


@attr.s(auto_attribs=True)
class ResetPasswordRequestModel:
    """ """

    new_password: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        new_password = self.new_password
        token = self.token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if new_password is not UNSET:
            field_dict["newPassword"] = new_password
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_password = d.pop("newPassword", UNSET)

        token = d.pop("token", UNSET)

        reset_password_request_model = cls(
            new_password=new_password,
            token=token,
        )

        return reset_password_request_model
