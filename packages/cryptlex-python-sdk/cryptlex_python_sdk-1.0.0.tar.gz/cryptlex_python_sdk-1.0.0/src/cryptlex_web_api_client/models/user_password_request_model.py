from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPasswordRequestModel")


@attr.s(auto_attribs=True)
class UserPasswordRequestModel:
    """ """

    old_password: Union[Unset, str] = UNSET
    new_password: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        old_password = self.old_password
        new_password = self.new_password

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if old_password is not UNSET:
            field_dict["oldPassword"] = old_password
        if new_password is not UNSET:
            field_dict["newPassword"] = new_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        old_password = d.pop("oldPassword", UNSET)

        new_password = d.pop("newPassword", UNSET)

        user_password_request_model = cls(
            old_password=old_password,
            new_password=new_password,
        )

        return user_password_request_model
