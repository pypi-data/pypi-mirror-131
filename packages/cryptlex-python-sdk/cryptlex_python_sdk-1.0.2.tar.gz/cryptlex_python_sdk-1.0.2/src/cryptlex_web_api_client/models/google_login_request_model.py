from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GoogleLoginRequestModel")


@attr.s(auto_attribs=True)
class GoogleLoginRequestModel:
    """ """

    company_id: Union[Unset, None, str] = UNSET
    email: Union[Unset, str] = UNSET
    id_token: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        company_id = self.company_id
        email = self.email
        id_token = self.id_token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if company_id is not UNSET:
            field_dict["companyId"] = company_id
        if email is not UNSET:
            field_dict["email"] = email
        if id_token is not UNSET:
            field_dict["idToken"] = id_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        company_id = d.pop("companyId", UNSET)

        email = d.pop("email", UNSET)

        id_token = d.pop("idToken", UNSET)

        google_login_request_model = cls(
            company_id=company_id,
            email=email,
            id_token=id_token,
        )

        return google_login_request_model
