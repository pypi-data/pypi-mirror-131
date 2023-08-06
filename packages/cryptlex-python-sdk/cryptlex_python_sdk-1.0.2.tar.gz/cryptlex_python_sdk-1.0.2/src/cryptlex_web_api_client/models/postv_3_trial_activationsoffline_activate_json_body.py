from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3TrialActivationsofflineActivateJsonBody")


@attr.s(auto_attribs=True)
class Postv3TrialActivationsofflineActivateJsonBody:
    """ """

    offline_request: Union[Unset, str] = UNSET
    response_validity: Union[Unset, int] = UNSET
    product_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        offline_request = self.offline_request
        response_validity = self.response_validity
        product_id = self.product_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offline_request is not UNSET:
            field_dict["offlineRequest"] = offline_request
        if response_validity is not UNSET:
            field_dict["responseValidity"] = response_validity
        if product_id is not UNSET:
            field_dict["productId"] = product_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        offline_request = d.pop("offlineRequest", UNSET)

        response_validity = d.pop("responseValidity", UNSET)

        product_id = d.pop("productId", UNSET)

        postv_3_trial_activationsoffline_activate_json_body = cls(
            offline_request=offline_request,
            response_validity=response_validity,
            product_id=product_id,
        )

        postv_3_trial_activationsoffline_activate_json_body.additional_properties = d
        return postv_3_trial_activationsoffline_activate_json_body

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
