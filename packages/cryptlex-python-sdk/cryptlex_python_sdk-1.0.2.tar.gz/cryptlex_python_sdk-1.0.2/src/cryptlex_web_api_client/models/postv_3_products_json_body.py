from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.product_metadata_request_model import ProductMetadataRequestModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3ProductsJsonBody")


@attr.s(auto_attribs=True)
class Postv3ProductsJsonBody:
    """ """

    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    email_templates: Union[Unset, None, List[str]] = UNSET
    license_policy_id: Union[Unset, str] = UNSET
    trial_policy_id: Union[Unset, None, str] = UNSET
    metadata: Union[Unset, None, List[ProductMetadataRequestModel]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        display_name = self.display_name
        description = self.description
        email_templates: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.email_templates, Unset):
            if self.email_templates is None:
                email_templates = None
            else:
                email_templates = self.email_templates

        license_policy_id = self.license_policy_id
        trial_policy_id = self.trial_policy_id
        metadata: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            if self.metadata is None:
                metadata = None
            else:
                metadata = []
                for metadata_item_data in self.metadata:
                    metadata_item = metadata_item_data.to_dict()

                    metadata.append(metadata_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if email_templates is not UNSET:
            field_dict["emailTemplates"] = email_templates
        if license_policy_id is not UNSET:
            field_dict["licensePolicyId"] = license_policy_id
        if trial_policy_id is not UNSET:
            field_dict["trialPolicyId"] = trial_policy_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        description = d.pop("description", UNSET)

        email_templates = cast(List[str], d.pop("emailTemplates", UNSET))

        license_policy_id = d.pop("licensePolicyId", UNSET)

        trial_policy_id = d.pop("trialPolicyId", UNSET)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = ProductMetadataRequestModel.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        postv_3_products_json_body = cls(
            name=name,
            display_name=display_name,
            description=description,
            email_templates=email_templates,
            license_policy_id=license_policy_id,
            trial_policy_id=trial_policy_id,
            metadata=metadata,
        )

        postv_3_products_json_body.additional_properties = d
        return postv_3_products_json_body

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
