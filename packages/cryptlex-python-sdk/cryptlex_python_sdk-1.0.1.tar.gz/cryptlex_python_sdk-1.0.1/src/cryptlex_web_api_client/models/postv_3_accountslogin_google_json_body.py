from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3AccountsloginGoogleJsonBody")


@attr.s(auto_attribs=True)
class Postv3AccountsloginGoogleJsonBody:
    """ """

    company_id: Union[Unset, None, str] = UNSET
    email: Union[Unset, str] = UNSET
    id_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        company_id = self.company_id
        email = self.email
        id_token = self.id_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        postv_3_accountslogin_google_json_body = cls(
            company_id=company_id,
            email=email,
            id_token=id_token,
        )

        postv_3_accountslogin_google_json_body.additional_properties = d
        return postv_3_accountslogin_google_json_body

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
