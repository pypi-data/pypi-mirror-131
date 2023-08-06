from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfflineActivationRequestModel")


@attr.s(auto_attribs=True)
class OfflineActivationRequestModel:
    """ """

    offline_request: Union[Unset, str] = UNSET
    response_validity: Union[Unset, int] = UNSET
    license_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        offline_request = self.offline_request
        response_validity = self.response_validity
        license_id = self.license_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if offline_request is not UNSET:
            field_dict["offlineRequest"] = offline_request
        if response_validity is not UNSET:
            field_dict["responseValidity"] = response_validity
        if license_id is not UNSET:
            field_dict["licenseId"] = license_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        offline_request = d.pop("offlineRequest", UNSET)

        response_validity = d.pop("responseValidity", UNSET)

        license_id = d.pop("licenseId", UNSET)

        offline_activation_request_model = cls(
            offline_request=offline_request,
            response_validity=response_validity,
            license_id=license_id,
        )

        return offline_activation_request_model
