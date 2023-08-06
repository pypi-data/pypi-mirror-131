from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserEmailRequestModel")


@attr.s(auto_attribs=True)
class UserEmailRequestModel:
    """ """

    company_id: Union[Unset, None, str] = UNSET
    email: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        company_id = self.company_id
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if company_id is not UNSET:
            field_dict["companyId"] = company_id
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        company_id = d.pop("companyId", UNSET)

        email = d.pop("email", UNSET)

        user_email_request_model = cls(
            company_id=company_id,
            email=email,
        )

        return user_email_request_model
