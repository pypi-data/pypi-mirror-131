from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3AccountsloginJsonBody")


@attr.s(auto_attribs=True)
class Postv3AccountsloginJsonBody:
    """ """

    company_id: Union[Unset, None, str] = UNSET
    email: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    two_factor_code: Union[Unset, None, str] = UNSET
    two_factor_recovery_code: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        company_id = self.company_id
        email = self.email
        password = self.password
        two_factor_code = self.two_factor_code
        two_factor_recovery_code = self.two_factor_recovery_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if company_id is not UNSET:
            field_dict["companyId"] = company_id
        if email is not UNSET:
            field_dict["email"] = email
        if password is not UNSET:
            field_dict["password"] = password
        if two_factor_code is not UNSET:
            field_dict["twoFactorCode"] = two_factor_code
        if two_factor_recovery_code is not UNSET:
            field_dict["twoFactorRecoveryCode"] = two_factor_recovery_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        company_id = d.pop("companyId", UNSET)

        email = d.pop("email", UNSET)

        password = d.pop("password", UNSET)

        two_factor_code = d.pop("twoFactorCode", UNSET)

        two_factor_recovery_code = d.pop("twoFactorRecoveryCode", UNSET)

        postv_3_accountslogin_json_body = cls(
            company_id=company_id,
            email=email,
            password=password,
            two_factor_code=two_factor_code,
            two_factor_recovery_code=two_factor_recovery_code,
        )

        postv_3_accountslogin_json_body.additional_properties = d
        return postv_3_accountslogin_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
