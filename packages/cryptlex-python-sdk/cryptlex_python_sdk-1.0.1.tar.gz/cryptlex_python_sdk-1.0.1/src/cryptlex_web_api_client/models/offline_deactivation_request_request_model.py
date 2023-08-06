from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfflineDeactivationRequestRequestModel")


@attr.s(auto_attribs=True)
class OfflineDeactivationRequestRequestModel:
    """ """

    offline_request: Union[Unset, str] = UNSET
    license_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        offline_request = self.offline_request
        license_id = self.license_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if offline_request is not UNSET:
            field_dict["offlineRequest"] = offline_request
        if license_id is not UNSET:
            field_dict["licenseId"] = license_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        offline_request = d.pop("offlineRequest", UNSET)

        license_id = d.pop("licenseId", UNSET)

        offline_deactivation_request_request_model = cls(
            offline_request=offline_request,
            license_id=license_id,
        )

        return offline_deactivation_request_request_model
