from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.product_version_feature_flag_request_model import ProductVersionFeatureFlagRequestModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3ProductVersionsJsonBody")


@attr.s(auto_attribs=True)
class Postv3ProductVersionsJsonBody:
    """ """

    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    product_id: Union[Unset, str] = UNSET
    feature_flags: Union[Unset, None, List[ProductVersionFeatureFlagRequestModel]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        display_name = self.display_name
        description = self.description
        product_id = self.product_id
        feature_flags: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.feature_flags, Unset):
            if self.feature_flags is None:
                feature_flags = None
            else:
                feature_flags = []
                for feature_flags_item_data in self.feature_flags:
                    feature_flags_item = feature_flags_item_data.to_dict()

                    feature_flags.append(feature_flags_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if feature_flags is not UNSET:
            field_dict["featureFlags"] = feature_flags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        description = d.pop("description", UNSET)

        product_id = d.pop("productId", UNSET)

        feature_flags = []
        _feature_flags = d.pop("featureFlags", UNSET)
        for feature_flags_item_data in _feature_flags or []:
            feature_flags_item = ProductVersionFeatureFlagRequestModel.from_dict(feature_flags_item_data)

            feature_flags.append(feature_flags_item)

        postv_3_product_versions_json_body = cls(
            name=name,
            display_name=display_name,
            description=description,
            product_id=product_id,
            feature_flags=feature_flags,
        )

        postv_3_product_versions_json_body.additional_properties = d
        return postv_3_product_versions_json_body

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
