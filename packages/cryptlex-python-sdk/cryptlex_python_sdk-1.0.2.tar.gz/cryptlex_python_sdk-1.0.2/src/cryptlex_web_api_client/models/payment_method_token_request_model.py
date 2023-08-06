from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentMethodTokenRequestModel")


@attr.s(auto_attribs=True)
class PaymentMethodTokenRequestModel:
    """ """

    token: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        token = self.token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token = d.pop("token", UNSET)

        payment_method_token_request_model = cls(
            token=token,
        )

        return payment_method_token_request_model
