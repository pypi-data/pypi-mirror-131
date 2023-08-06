import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.license_policy_dto import LicensePolicyDto
from ..models.metadata_dto import MetadataDto
from ..models.trial_policy_dto import TrialPolicyDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProductDto")


@attr.s(auto_attribs=True)
class ProductDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    display_name: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    public_key: Union[Unset, None, str] = UNSET
    total_licenses: Union[Unset, int] = UNSET
    total_trial_activations: Union[Unset, int] = UNSET
    total_releases: Union[Unset, int] = UNSET
    total_product_versions: Union[Unset, int] = UNSET
    total_feature_flags: Union[Unset, int] = UNSET
    email_templates: Union[Unset, None, List[str]] = UNSET
    license_policy: Union[Unset, LicensePolicyDto] = UNSET
    trial_policy: Union[Unset, TrialPolicyDto] = UNSET
    metadata: Union[Unset, None, List[MetadataDto]] = UNSET

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
        public_key = self.public_key
        total_licenses = self.total_licenses
        total_trial_activations = self.total_trial_activations
        total_releases = self.total_releases
        total_product_versions = self.total_product_versions
        total_feature_flags = self.total_feature_flags
        email_templates: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.email_templates, Unset):
            if self.email_templates is None:
                email_templates = None
            else:
                email_templates = self.email_templates

        license_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.license_policy, Unset):
            license_policy = self.license_policy.to_dict()

        trial_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trial_policy, Unset):
            trial_policy = self.trial_policy.to_dict()

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
        if public_key is not UNSET:
            field_dict["publicKey"] = public_key
        if total_licenses is not UNSET:
            field_dict["totalLicenses"] = total_licenses
        if total_trial_activations is not UNSET:
            field_dict["totalTrialActivations"] = total_trial_activations
        if total_releases is not UNSET:
            field_dict["totalReleases"] = total_releases
        if total_product_versions is not UNSET:
            field_dict["totalProductVersions"] = total_product_versions
        if total_feature_flags is not UNSET:
            field_dict["totalFeatureFlags"] = total_feature_flags
        if email_templates is not UNSET:
            field_dict["emailTemplates"] = email_templates
        if license_policy is not UNSET:
            field_dict["licensePolicy"] = license_policy
        if trial_policy is not UNSET:
            field_dict["trialPolicy"] = trial_policy
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

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

        public_key = d.pop("publicKey", UNSET)

        total_licenses = d.pop("totalLicenses", UNSET)

        total_trial_activations = d.pop("totalTrialActivations", UNSET)

        total_releases = d.pop("totalReleases", UNSET)

        total_product_versions = d.pop("totalProductVersions", UNSET)

        total_feature_flags = d.pop("totalFeatureFlags", UNSET)

        email_templates = cast(List[str], d.pop("emailTemplates", UNSET))

        _license_policy = d.pop("licensePolicy", UNSET)
        license_policy: Union[Unset, LicensePolicyDto]
        if isinstance(_license_policy, Unset):
            license_policy = UNSET
        else:
            license_policy = LicensePolicyDto.from_dict(_license_policy)

        _trial_policy = d.pop("trialPolicy", UNSET)
        trial_policy: Union[Unset, TrialPolicyDto]
        if isinstance(_trial_policy, Unset):
            trial_policy = UNSET
        else:
            trial_policy = TrialPolicyDto.from_dict(_trial_policy)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = MetadataDto.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        product_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            display_name=display_name,
            description=description,
            public_key=public_key,
            total_licenses=total_licenses,
            total_trial_activations=total_trial_activations,
            total_releases=total_releases,
            total_product_versions=total_product_versions,
            total_feature_flags=total_feature_flags,
            email_templates=email_templates,
            license_policy=license_policy,
            trial_policy=trial_policy,
            metadata=metadata,
        )

        return product_dto
