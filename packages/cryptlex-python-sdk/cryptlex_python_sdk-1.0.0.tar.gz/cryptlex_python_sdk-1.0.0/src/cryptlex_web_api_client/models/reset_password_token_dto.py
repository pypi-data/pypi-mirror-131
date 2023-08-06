from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResetPasswordTokenDto")


@attr.s(auto_attribs=True)
class ResetPasswordTokenDto:
    """ """

    reset_password_token: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        reset_password_token = self.reset_password_token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if reset_password_token is not UNSET:
            field_dict["resetPasswordToken"] = reset_password_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reset_password_token = d.pop("resetPasswordToken", UNSET)

        reset_password_token_dto = cls(
            reset_password_token=reset_password_token,
        )

        return reset_password_token_dto
