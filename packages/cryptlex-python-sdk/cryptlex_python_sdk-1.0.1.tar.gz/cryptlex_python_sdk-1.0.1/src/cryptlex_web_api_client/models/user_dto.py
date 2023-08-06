import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.metadata_dto import MetadataDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserDto")


@attr.s(auto_attribs=True)
class UserDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    first_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    email: Union[Unset, None, str] = UNSET
    company: Union[Unset, None, str] = UNSET
    two_factor_enabled: Union[Unset, bool] = UNSET
    google_sso_enabled: Union[Unset, bool] = UNSET
    allow_customer_portal_access: Union[Unset, bool] = UNSET
    role: Union[Unset, None, str] = UNSET
    roles: Union[Unset, None, List[str]] = UNSET
    last_login_at: Union[Unset, None, datetime.datetime] = UNSET
    last_seen_at: Union[Unset, None, datetime.datetime] = UNSET
    metadata: Union[Unset, None, List[MetadataDto]] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        name = self.name
        first_name = self.first_name
        last_name = self.last_name
        email = self.email
        company = self.company
        two_factor_enabled = self.two_factor_enabled
        google_sso_enabled = self.google_sso_enabled
        allow_customer_portal_access = self.allow_customer_portal_access
        role = self.role
        roles: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.roles, Unset):
            if self.roles is None:
                roles = None
            else:
                roles = self.roles

        last_login_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_login_at, Unset):
            last_login_at = self.last_login_at.isoformat() if self.last_login_at else None

        last_seen_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_seen_at, Unset):
            last_seen_at = self.last_seen_at.isoformat() if self.last_seen_at else None

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
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if company is not UNSET:
            field_dict["company"] = company
        if two_factor_enabled is not UNSET:
            field_dict["twoFactorEnabled"] = two_factor_enabled
        if google_sso_enabled is not UNSET:
            field_dict["googleSsoEnabled"] = google_sso_enabled
        if allow_customer_portal_access is not UNSET:
            field_dict["allowCustomerPortalAccess"] = allow_customer_portal_access
        if role is not UNSET:
            field_dict["role"] = role
        if roles is not UNSET:
            field_dict["roles"] = roles
        if last_login_at is not UNSET:
            field_dict["lastLoginAt"] = last_login_at
        if last_seen_at is not UNSET:
            field_dict["lastSeenAt"] = last_seen_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if tags is not UNSET:
            field_dict["tags"] = tags

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

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        email = d.pop("email", UNSET)

        company = d.pop("company", UNSET)

        two_factor_enabled = d.pop("twoFactorEnabled", UNSET)

        google_sso_enabled = d.pop("googleSsoEnabled", UNSET)

        allow_customer_portal_access = d.pop("allowCustomerPortalAccess", UNSET)

        role = d.pop("role", UNSET)

        roles = cast(List[str], d.pop("roles", UNSET))

        _last_login_at = d.pop("lastLoginAt", UNSET)
        last_login_at: Union[Unset, None, datetime.datetime]
        if _last_login_at is None:
            last_login_at = None
        elif isinstance(_last_login_at, Unset):
            last_login_at = UNSET
        else:
            last_login_at = isoparse(_last_login_at)

        _last_seen_at = d.pop("lastSeenAt", UNSET)
        last_seen_at: Union[Unset, None, datetime.datetime]
        if _last_seen_at is None:
            last_seen_at = None
        elif isinstance(_last_seen_at, Unset):
            last_seen_at = UNSET
        else:
            last_seen_at = isoparse(_last_seen_at)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = MetadataDto.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        tags = cast(List[str], d.pop("tags", UNSET))

        user_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
            two_factor_enabled=two_factor_enabled,
            google_sso_enabled=google_sso_enabled,
            allow_customer_portal_access=allow_customer_portal_access,
            role=role,
            roles=roles,
            last_login_at=last_login_at,
            last_seen_at=last_seen_at,
            metadata=metadata,
            tags=tags,
        )

        return user_dto
