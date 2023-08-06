import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.product_version_feature_flag_dto import ProductVersionFeatureFlagDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProductVersionDto")


@attr.s(auto_attribs=True)
class ProductVersionDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    display_name: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    product_id: Union[Unset, None, str] = UNSET
    feature_flags: Union[Unset, None, List[ProductVersionFeatureFlagDto]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

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
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
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
        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        description = d.pop("description", UNSET)

        product_id = d.pop("productId", UNSET)

        feature_flags = []
        _feature_flags = d.pop("featureFlags", UNSET)
        for feature_flags_item_data in _feature_flags or []:
            feature_flags_item = ProductVersionFeatureFlagDto.from_dict(feature_flags_item_data)

            feature_flags.append(feature_flags_item)

        product_version_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            display_name=display_name,
            description=description,
            product_id=product_id,
            feature_flags=feature_flags,
        )

        return product_version_dto
