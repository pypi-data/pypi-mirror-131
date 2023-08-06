from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.user_metadata_request_model import UserMetadataRequestModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="MeUpdateRequestModel")


@attr.s(auto_attribs=True)
class MeUpdateRequestModel:
    """ """

    first_name: str
    last_name: str
    email: str
    company: Union[Unset, None, str] = UNSET
    allow_customer_portal_access: Union[Unset, None, bool] = UNSET
    metadata: Union[Unset, None, List[UserMetadataRequestModel]] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    google_sso_enabled: Union[Unset, None, bool] = UNSET
    two_factor_enabled: Union[Unset, None, bool] = UNSET
    two_factor_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        last_name = self.last_name
        email = self.email
        company = self.company
        allow_customer_portal_access = self.allow_customer_portal_access
        metadata: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            if self.metadata is None:
                metadata = None
            else:
                metadata = []
                for metadata_item_data in self.metadata:
                    metadata_item = metadata_item_data.to_dict()

                    metadata.append(metadata_item)

        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        google_sso_enabled = self.google_sso_enabled
        two_factor_enabled = self.two_factor_enabled
        two_factor_code = self.two_factor_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            }
        )
        if company is not UNSET:
            field_dict["company"] = company
        if allow_customer_portal_access is not UNSET:
            field_dict["allowCustomerPortalAccess"] = allow_customer_portal_access
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if tags is not UNSET:
            field_dict["tags"] = tags
        if google_sso_enabled is not UNSET:
            field_dict["googleSsoEnabled"] = google_sso_enabled
        if two_factor_enabled is not UNSET:
            field_dict["twoFactorEnabled"] = two_factor_enabled
        if two_factor_code is not UNSET:
            field_dict["twoFactorCode"] = two_factor_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("firstName")

        last_name = d.pop("lastName")

        email = d.pop("email")

        company = d.pop("company", UNSET)

        allow_customer_portal_access = d.pop("allowCustomerPortalAccess", UNSET)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = UserMetadataRequestModel.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        tags = cast(List[str], d.pop("tags", UNSET))

        google_sso_enabled = d.pop("googleSsoEnabled", UNSET)

        two_factor_enabled = d.pop("twoFactorEnabled", UNSET)

        two_factor_code = d.pop("twoFactorCode", UNSET)

        me_update_request_model = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
            allow_customer_portal_access=allow_customer_portal_access,
            metadata=metadata,
            tags=tags,
            google_sso_enabled=google_sso_enabled,
            two_factor_enabled=two_factor_enabled,
            two_factor_code=two_factor_code,
        )

        return me_update_request_model
