from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterRequestModel")


@attr.s(auto_attribs=True)
class RegisterRequestModel:
    """ """

    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    company: Union[Unset, str] = UNSET
    company_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        last_name = self.last_name
        email = self.email
        password = self.password
        company = self.company
        company_id = self.company_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if password is not UNSET:
            field_dict["password"] = password
        if company is not UNSET:
            field_dict["company"] = company
        if company_id is not UNSET:
            field_dict["companyId"] = company_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        email = d.pop("email", UNSET)

        password = d.pop("password", UNSET)

        company = d.pop("company", UNSET)

        company_id = d.pop("companyId", UNSET)

        register_request_model = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            company=company,
            company_id=company_id,
        )

        return register_request_model
