from typing import Any, Dict, Type, TypeVar

import attr

from ..models.account_status_request_model_status import AccountStatusRequestModelStatus

T = TypeVar("T", bound="AccountStatusRequestModel")


@attr.s(auto_attribs=True)
class AccountStatusRequestModel:
    """ """

    status: AccountStatusRequestModelStatus

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = AccountStatusRequestModelStatus(d.pop("status"))

        account_status_request_model = cls(
            status=status,
        )

        return account_status_request_model
