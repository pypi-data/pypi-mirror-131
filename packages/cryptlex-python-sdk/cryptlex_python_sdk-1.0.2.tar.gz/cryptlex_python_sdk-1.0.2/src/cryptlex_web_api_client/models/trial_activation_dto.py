import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.activation_metadata_dto import ActivationMetadataDto
from ..models.geo_location_dto import GeoLocationDto
from ..models.trial_activation_dto_os import TrialActivationDtoOs
from ..types import UNSET, Unset

T = TypeVar("T", bound="TrialActivationDto")


@attr.s(auto_attribs=True)
class TrialActivationDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    os: Union[Unset, None, TrialActivationDtoOs] = UNSET
    os_version: Union[Unset, None, str] = UNSET
    hostname: Union[Unset, None, str] = UNSET
    location: Union[Unset, GeoLocationDto] = UNSET
    vm_name: Union[Unset, None, str] = UNSET
    container: Union[Unset, bool] = UNSET
    offline: Union[Unset, bool] = UNSET
    app_version: Union[Unset, None, str] = UNSET
    expires_at: Union[Unset, None, datetime.datetime] = UNSET
    metadata: Union[Unset, None, List[ActivationMetadataDto]] = UNSET
    product_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        os: Union[Unset, None, str] = UNSET
        if not isinstance(self.os, Unset):
            os = self.os.value if self.os else None

        os_version = self.os_version
        hostname = self.hostname
        location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.location, Unset):
            location = self.location.to_dict()

        vm_name = self.vm_name
        container = self.container
        offline = self.offline
        app_version = self.app_version
        expires_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat() if self.expires_at else None

        metadata: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            if self.metadata is None:
                metadata = None
            else:
                metadata = []
                for metadata_item_data in self.metadata:
                    metadata_item = metadata_item_data.to_dict()

                    metadata.append(metadata_item)

        product_id = self.product_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if os is not UNSET:
            field_dict["os"] = os
        if os_version is not UNSET:
            field_dict["osVersion"] = os_version
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if location is not UNSET:
            field_dict["location"] = location
        if vm_name is not UNSET:
            field_dict["vmName"] = vm_name
        if container is not UNSET:
            field_dict["container"] = container
        if offline is not UNSET:
            field_dict["offline"] = offline
        if app_version is not UNSET:
            field_dict["appVersion"] = app_version
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if product_id is not UNSET:
            field_dict["productId"] = product_id

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

        _os = d.pop("os", UNSET)
        os: Union[Unset, None, TrialActivationDtoOs]
        if _os is None:
            os = None
        elif isinstance(_os, Unset):
            os = UNSET
        else:
            os = TrialActivationDtoOs(_os)

        os_version = d.pop("osVersion", UNSET)

        hostname = d.pop("hostname", UNSET)

        _location = d.pop("location", UNSET)
        location: Union[Unset, GeoLocationDto]
        if isinstance(_location, Unset):
            location = UNSET
        else:
            location = GeoLocationDto.from_dict(_location)

        vm_name = d.pop("vmName", UNSET)

        container = d.pop("container", UNSET)

        offline = d.pop("offline", UNSET)

        app_version = d.pop("appVersion", UNSET)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, None, datetime.datetime]
        if _expires_at is None:
            expires_at = None
        elif isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = ActivationMetadataDto.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        product_id = d.pop("productId", UNSET)

        trial_activation_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            os=os,
            os_version=os_version,
            hostname=hostname,
            location=location,
            vm_name=vm_name,
            container=container,
            offline=offline,
            app_version=app_version,
            expires_at=expires_at,
            metadata=metadata,
            product_id=product_id,
        )

        return trial_activation_dto
