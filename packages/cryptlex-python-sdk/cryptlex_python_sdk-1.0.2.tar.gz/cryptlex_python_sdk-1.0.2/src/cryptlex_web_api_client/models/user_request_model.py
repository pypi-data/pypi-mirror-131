from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.user_metadata_request_model import UserMetadataRequestModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserRequestModel")


@attr.s(auto_attribs=True)
class UserRequestModel:
    """ """

    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    company: Union[Unset, None, str] = UNSET
    allow_customer_portal_access: Union[Unset, None, bool] = UNSET
    metadata: Union[Unset, None, List[UserMetadataRequestModel]] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    password: Union[Unset, str] = UNSET
    role: Union[Unset, None, str] = UNSET

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

        password = self.password
        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if company is not UNSET:
            field_dict["company"] = company
        if allow_customer_portal_access is not UNSET:
            field_dict["allowCustomerPortalAccess"] = allow_customer_portal_access
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if tags is not UNSET:
            field_dict["tags"] = tags
        if password is not UNSET:
            field_dict["password"] = password
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        email = d.pop("email", UNSET)

        company = d.pop("company", UNSET)

        allow_customer_portal_access = d.pop("allowCustomerPortalAccess", UNSET)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = UserMetadataRequestModel.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        tags = cast(List[str], d.pop("tags", UNSET))

        password = d.pop("password", UNSET)

        role = d.pop("role", UNSET)

        user_request_model = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
            allow_customer_portal_access=allow_customer_portal_access,
            metadata=metadata,
            tags=tags,
            password=password,
            role=role,
        )

        return user_request_model
