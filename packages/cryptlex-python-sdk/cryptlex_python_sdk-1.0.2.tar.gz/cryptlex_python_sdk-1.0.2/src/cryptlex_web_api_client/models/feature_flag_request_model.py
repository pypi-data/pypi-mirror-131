from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeatureFlagRequestModel")


@attr.s(auto_attribs=True)
class FeatureFlagRequestModel:
    """ """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    product_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        product_id = self.product_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if product_id is not UNSET:
            field_dict["productId"] = product_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        product_id = d.pop("productId", UNSET)

        feature_flag_request_model = cls(
            name=name,
            description=description,
            product_id=product_id,
        )

        return feature_flag_request_model
