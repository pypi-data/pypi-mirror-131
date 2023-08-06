import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.activation_dto_os import ActivationDtoOs
from ..models.activation_metadata_dto import ActivationMetadataDto
from ..models.activation_meter_attribute_dto import ActivationMeterAttributeDto
from ..models.geo_location_dto import GeoLocationDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationDto")


@attr.s(auto_attribs=True)
class ActivationDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    os: Union[Unset, None, ActivationDtoOs] = UNSET
    os_version: Union[Unset, None, str] = UNSET
    hostname: Union[Unset, None, str] = UNSET
    location: Union[Unset, GeoLocationDto] = UNSET
    vm_name: Union[Unset, None, str] = UNSET
    container: Union[Unset, bool] = UNSET
    offline: Union[Unset, bool] = UNSET
    app_version: Union[Unset, None, str] = UNSET
    expires_at: Union[Unset, None, datetime.datetime] = UNSET
    metadata: Union[Unset, None, List[ActivationMetadataDto]] = UNSET
    license_id: Union[Unset, None, str] = UNSET
    last_synced_at: Union[Unset, datetime.datetime] = UNSET
    lease_expires_at: Union[Unset, None, datetime.datetime] = UNSET
    meter_attributes: Union[Unset, None, List[ActivationMeterAttributeDto]] = UNSET

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

        license_id = self.license_id
        last_synced_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_synced_at, Unset):
            last_synced_at = self.last_synced_at.isoformat()

        lease_expires_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.lease_expires_at, Unset):
            lease_expires_at = self.lease_expires_at.isoformat() if self.lease_expires_at else None

        meter_attributes: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.meter_attributes, Unset):
            if self.meter_attributes is None:
                meter_attributes = None
            else:
                meter_attributes = []
                for meter_attributes_item_data in self.meter_attributes:
                    meter_attributes_item = meter_attributes_item_data.to_dict()

                    meter_attributes.append(meter_attributes_item)

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
        if license_id is not UNSET:
            field_dict["licenseId"] = license_id
        if last_synced_at is not UNSET:
            field_dict["lastSyncedAt"] = last_synced_at
        if lease_expires_at is not UNSET:
            field_dict["leaseExpiresAt"] = lease_expires_at
        if meter_attributes is not UNSET:
            field_dict["meterAttributes"] = meter_attributes

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
        os: Union[Unset, None, ActivationDtoOs]
        if _os is None:
            os = None
        elif isinstance(_os, Unset):
            os = UNSET
        else:
            os = ActivationDtoOs(_os)

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

        license_id = d.pop("licenseId", UNSET)

        _last_synced_at = d.pop("lastSyncedAt", UNSET)
        last_synced_at: Union[Unset, datetime.datetime]
        if isinstance(_last_synced_at, Unset):
            last_synced_at = UNSET
        else:
            last_synced_at = isoparse(_last_synced_at)

        _lease_expires_at = d.pop("leaseExpiresAt", UNSET)
        lease_expires_at: Union[Unset, None, datetime.datetime]
        if _lease_expires_at is None:
            lease_expires_at = None
        elif isinstance(_lease_expires_at, Unset):
            lease_expires_at = UNSET
        else:
            lease_expires_at = isoparse(_lease_expires_at)

        meter_attributes = []
        _meter_attributes = d.pop("meterAttributes", UNSET)
        for meter_attributes_item_data in _meter_attributes or []:
            meter_attributes_item = ActivationMeterAttributeDto.from_dict(meter_attributes_item_data)

            meter_attributes.append(meter_attributes_item)

        activation_dto = cls(
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
            license_id=license_id,
            last_synced_at=last_synced_at,
            lease_expires_at=lease_expires_at,
            meter_attributes=meter_attributes,
        )

        return activation_dto
