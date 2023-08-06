from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationTokenDto")


@attr.s(auto_attribs=True)
class ActivationTokenDto:
    """ """

    activation_token: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        activation_token = self.activation_token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if activation_token is not UNSET:
            field_dict["activationToken"] = activation_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activation_token = d.pop("activationToken", UNSET)

        activation_token_dto = cls(
            activation_token=activation_token,
        )

        return activation_token_dto
