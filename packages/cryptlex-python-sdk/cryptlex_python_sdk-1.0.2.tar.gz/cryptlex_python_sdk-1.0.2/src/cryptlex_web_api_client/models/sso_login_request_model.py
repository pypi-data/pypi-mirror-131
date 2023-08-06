from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SsoLoginRequestModel")


@attr.s(auto_attribs=True)
class SsoLoginRequestModel:
    """ """

    company_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        company_id = self.company_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if company_id is not UNSET:
            field_dict["companyId"] = company_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        company_id = d.pop("companyId", UNSET)

        sso_login_request_model = cls(
            company_id=company_id,
        )

        return sso_login_request_model
