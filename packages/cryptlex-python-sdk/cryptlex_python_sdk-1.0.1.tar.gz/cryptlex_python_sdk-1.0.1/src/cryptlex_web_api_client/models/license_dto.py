import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.license_dto_expiration_strategy import LicenseDtoExpirationStrategy
from ..models.license_dto_fingerprint_matching_strategy import LicenseDtoFingerprintMatchingStrategy
from ..models.license_dto_leasing_strategy import LicenseDtoLeasingStrategy
from ..models.license_dto_type import LicenseDtoType
from ..models.license_meter_attribute_dto import LicenseMeterAttributeDto
from ..models.metadata_dto import MetadataDto
from ..models.user_dto import UserDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseDto")


@attr.s(auto_attribs=True)
class LicenseDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    key: Union[Unset, None, str] = UNSET
    revoked: Union[Unset, bool] = UNSET
    suspended: Union[Unset, bool] = UNSET
    total_activations: Union[Unset, int] = UNSET
    total_deactivations: Union[Unset, int] = UNSET
    validity: Union[Unset, int] = UNSET
    expiration_strategy: Union[Unset, None, LicenseDtoExpirationStrategy] = UNSET
    fingerprint_matching_strategy: Union[Unset, None, LicenseDtoFingerprintMatchingStrategy] = UNSET
    allowed_activations: Union[Unset, int] = UNSET
    allowed_deactivations: Union[Unset, int] = UNSET
    type: Union[Unset, None, LicenseDtoType] = UNSET
    allowed_floating_clients: Union[Unset, int] = UNSET
    server_sync_grace_period: Union[Unset, int] = UNSET
    server_sync_interval: Union[Unset, int] = UNSET
    allowed_clock_offset: Union[Unset, int] = UNSET
    expiring_soon_event_offset: Union[Unset, int] = UNSET
    lease_duration: Union[Unset, int] = UNSET
    leasing_strategy: Union[Unset, None, LicenseDtoLeasingStrategy] = UNSET
    expires_at: Union[Unset, None, datetime.datetime] = UNSET
    allow_vm_activation: Union[Unset, bool] = UNSET
    allow_container_activation: Union[Unset, bool] = UNSET
    allow_client_lease_duration: Union[Unset, bool] = UNSET
    user_locked: Union[Unset, bool] = UNSET
    require_authentication: Union[Unset, bool] = UNSET
    disable_geo_location: Union[Unset, bool] = UNSET
    notes: Union[Unset, None, str] = UNSET
    product_id: Union[Unset, None, str] = UNSET
    product_version_id: Union[Unset, None, str] = UNSET
    user: Union[Unset, UserDto] = UNSET
    reseller: Union[Unset, UserDto] = UNSET
    additional_user_ids: Union[Unset, None, List[str]] = UNSET
    allowed_ip_range: Union[Unset, None, str] = UNSET
    allowed_ip_ranges: Union[Unset, None, List[str]] = UNSET
    allowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
    disallowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
    allowed_countries: Union[Unset, None, List[str]] = UNSET
    disallowed_countries: Union[Unset, None, List[str]] = UNSET
    metadata: Union[Unset, None, List[MetadataDto]] = UNSET
    meter_attributes: Union[Unset, None, List[LicenseMeterAttributeDto]] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        key = self.key
        revoked = self.revoked
        suspended = self.suspended
        total_activations = self.total_activations
        total_deactivations = self.total_deactivations
        validity = self.validity
        expiration_strategy: Union[Unset, None, str] = UNSET
        if not isinstance(self.expiration_strategy, Unset):
            expiration_strategy = self.expiration_strategy.value if self.expiration_strategy else None

        fingerprint_matching_strategy: Union[Unset, None, str] = UNSET
        if not isinstance(self.fingerprint_matching_strategy, Unset):
            fingerprint_matching_strategy = (
                self.fingerprint_matching_strategy.value if self.fingerprint_matching_strategy else None
            )

        allowed_activations = self.allowed_activations
        allowed_deactivations = self.allowed_deactivations
        type: Union[Unset, None, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value if self.type else None

        allowed_floating_clients = self.allowed_floating_clients
        server_sync_grace_period = self.server_sync_grace_period
        server_sync_interval = self.server_sync_interval
        allowed_clock_offset = self.allowed_clock_offset
        expiring_soon_event_offset = self.expiring_soon_event_offset
        lease_duration = self.lease_duration
        leasing_strategy: Union[Unset, None, str] = UNSET
        if not isinstance(self.leasing_strategy, Unset):
            leasing_strategy = self.leasing_strategy.value if self.leasing_strategy else None

        expires_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat() if self.expires_at else None

        allow_vm_activation = self.allow_vm_activation
        allow_container_activation = self.allow_container_activation
        allow_client_lease_duration = self.allow_client_lease_duration
        user_locked = self.user_locked
        require_authentication = self.require_authentication
        disable_geo_location = self.disable_geo_location
        notes = self.notes
        product_id = self.product_id
        product_version_id = self.product_version_id
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        reseller: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reseller, Unset):
            reseller = self.reseller.to_dict()

        additional_user_ids: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.additional_user_ids, Unset):
            if self.additional_user_ids is None:
                additional_user_ids = None
            else:
                additional_user_ids = self.additional_user_ids

        allowed_ip_range = self.allowed_ip_range
        allowed_ip_ranges: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.allowed_ip_ranges, Unset):
            if self.allowed_ip_ranges is None:
                allowed_ip_ranges = None
            else:
                allowed_ip_ranges = self.allowed_ip_ranges

        allowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.allowed_ip_addresses, Unset):
            if self.allowed_ip_addresses is None:
                allowed_ip_addresses = None
            else:
                allowed_ip_addresses = self.allowed_ip_addresses

        disallowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.disallowed_ip_addresses, Unset):
            if self.disallowed_ip_addresses is None:
                disallowed_ip_addresses = None
            else:
                disallowed_ip_addresses = self.disallowed_ip_addresses

        allowed_countries: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.allowed_countries, Unset):
            if self.allowed_countries is None:
                allowed_countries = None
            else:
                allowed_countries = self.allowed_countries

        disallowed_countries: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.disallowed_countries, Unset):
            if self.disallowed_countries is None:
                disallowed_countries = None
            else:
                disallowed_countries = self.disallowed_countries

        metadata: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            if self.metadata is None:
                metadata = None
            else:
                metadata = []
                for metadata_item_data in self.metadata:
                    metadata_item = metadata_item_data.to_dict()

                    metadata.append(metadata_item)

        meter_attributes: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.meter_attributes, Unset):
            if self.meter_attributes is None:
                meter_attributes = None
            else:
                meter_attributes = []
                for meter_attributes_item_data in self.meter_attributes:
                    meter_attributes_item = meter_attributes_item_data.to_dict()

                    meter_attributes.append(meter_attributes_item)

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
        if key is not UNSET:
            field_dict["key"] = key
        if revoked is not UNSET:
            field_dict["revoked"] = revoked
        if suspended is not UNSET:
            field_dict["suspended"] = suspended
        if total_activations is not UNSET:
            field_dict["totalActivations"] = total_activations
        if total_deactivations is not UNSET:
            field_dict["totalDeactivations"] = total_deactivations
        if validity is not UNSET:
            field_dict["validity"] = validity
        if expiration_strategy is not UNSET:
            field_dict["expirationStrategy"] = expiration_strategy
        if fingerprint_matching_strategy is not UNSET:
            field_dict["fingerprintMatchingStrategy"] = fingerprint_matching_strategy
        if allowed_activations is not UNSET:
            field_dict["allowedActivations"] = allowed_activations
        if allowed_deactivations is not UNSET:
            field_dict["allowedDeactivations"] = allowed_deactivations
        if type is not UNSET:
            field_dict["type"] = type
        if allowed_floating_clients is not UNSET:
            field_dict["allowedFloatingClients"] = allowed_floating_clients
        if server_sync_grace_period is not UNSET:
            field_dict["serverSyncGracePeriod"] = server_sync_grace_period
        if server_sync_interval is not UNSET:
            field_dict["serverSyncInterval"] = server_sync_interval
        if allowed_clock_offset is not UNSET:
            field_dict["allowedClockOffset"] = allowed_clock_offset
        if expiring_soon_event_offset is not UNSET:
            field_dict["expiringSoonEventOffset"] = expiring_soon_event_offset
        if lease_duration is not UNSET:
            field_dict["leaseDuration"] = lease_duration
        if leasing_strategy is not UNSET:
            field_dict["leasingStrategy"] = leasing_strategy
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if allow_vm_activation is not UNSET:
            field_dict["allowVmActivation"] = allow_vm_activation
        if allow_container_activation is not UNSET:
            field_dict["allowContainerActivation"] = allow_container_activation
        if allow_client_lease_duration is not UNSET:
            field_dict["allowClientLeaseDuration"] = allow_client_lease_duration
        if user_locked is not UNSET:
            field_dict["userLocked"] = user_locked
        if require_authentication is not UNSET:
            field_dict["requireAuthentication"] = require_authentication
        if disable_geo_location is not UNSET:
            field_dict["disableGeoLocation"] = disable_geo_location
        if notes is not UNSET:
            field_dict["notes"] = notes
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if product_version_id is not UNSET:
            field_dict["productVersionId"] = product_version_id
        if user is not UNSET:
            field_dict["user"] = user
        if reseller is not UNSET:
            field_dict["reseller"] = reseller
        if additional_user_ids is not UNSET:
            field_dict["additionalUserIds"] = additional_user_ids
        if allowed_ip_range is not UNSET:
            field_dict["allowedIpRange"] = allowed_ip_range
        if allowed_ip_ranges is not UNSET:
            field_dict["allowedIpRanges"] = allowed_ip_ranges
        if allowed_ip_addresses is not UNSET:
            field_dict["allowedIpAddresses"] = allowed_ip_addresses
        if disallowed_ip_addresses is not UNSET:
            field_dict["disallowedIpAddresses"] = disallowed_ip_addresses
        if allowed_countries is not UNSET:
            field_dict["allowedCountries"] = allowed_countries
        if disallowed_countries is not UNSET:
            field_dict["disallowedCountries"] = disallowed_countries
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if meter_attributes is not UNSET:
            field_dict["meterAttributes"] = meter_attributes
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

        key = d.pop("key", UNSET)

        revoked = d.pop("revoked", UNSET)

        suspended = d.pop("suspended", UNSET)

        total_activations = d.pop("totalActivations", UNSET)

        total_deactivations = d.pop("totalDeactivations", UNSET)

        validity = d.pop("validity", UNSET)

        _expiration_strategy = d.pop("expirationStrategy", UNSET)
        expiration_strategy: Union[Unset, None, LicenseDtoExpirationStrategy]
        if _expiration_strategy is None:
            expiration_strategy = None
        elif isinstance(_expiration_strategy, Unset):
            expiration_strategy = UNSET
        else:
            expiration_strategy = LicenseDtoExpirationStrategy(_expiration_strategy)

        _fingerprint_matching_strategy = d.pop("fingerprintMatchingStrategy", UNSET)
        fingerprint_matching_strategy: Union[Unset, None, LicenseDtoFingerprintMatchingStrategy]
        if _fingerprint_matching_strategy is None:
            fingerprint_matching_strategy = None
        elif isinstance(_fingerprint_matching_strategy, Unset):
            fingerprint_matching_strategy = UNSET
        else:
            fingerprint_matching_strategy = LicenseDtoFingerprintMatchingStrategy(_fingerprint_matching_strategy)

        allowed_activations = d.pop("allowedActivations", UNSET)

        allowed_deactivations = d.pop("allowedDeactivations", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, None, LicenseDtoType]
        if _type is None:
            type = None
        elif isinstance(_type, Unset):
            type = UNSET
        else:
            type = LicenseDtoType(_type)

        allowed_floating_clients = d.pop("allowedFloatingClients", UNSET)

        server_sync_grace_period = d.pop("serverSyncGracePeriod", UNSET)

        server_sync_interval = d.pop("serverSyncInterval", UNSET)

        allowed_clock_offset = d.pop("allowedClockOffset", UNSET)

        expiring_soon_event_offset = d.pop("expiringSoonEventOffset", UNSET)

        lease_duration = d.pop("leaseDuration", UNSET)

        _leasing_strategy = d.pop("leasingStrategy", UNSET)
        leasing_strategy: Union[Unset, None, LicenseDtoLeasingStrategy]
        if _leasing_strategy is None:
            leasing_strategy = None
        elif isinstance(_leasing_strategy, Unset):
            leasing_strategy = UNSET
        else:
            leasing_strategy = LicenseDtoLeasingStrategy(_leasing_strategy)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, None, datetime.datetime]
        if _expires_at is None:
            expires_at = None
        elif isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        allow_vm_activation = d.pop("allowVmActivation", UNSET)

        allow_container_activation = d.pop("allowContainerActivation", UNSET)

        allow_client_lease_duration = d.pop("allowClientLeaseDuration", UNSET)

        user_locked = d.pop("userLocked", UNSET)

        require_authentication = d.pop("requireAuthentication", UNSET)

        disable_geo_location = d.pop("disableGeoLocation", UNSET)

        notes = d.pop("notes", UNSET)

        product_id = d.pop("productId", UNSET)

        product_version_id = d.pop("productVersionId", UNSET)

        _user = d.pop("user", UNSET)
        user: Union[Unset, UserDto]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = UserDto.from_dict(_user)

        _reseller = d.pop("reseller", UNSET)
        reseller: Union[Unset, UserDto]
        if isinstance(_reseller, Unset):
            reseller = UNSET
        else:
            reseller = UserDto.from_dict(_reseller)

        additional_user_ids = cast(List[str], d.pop("additionalUserIds", UNSET))

        allowed_ip_range = d.pop("allowedIpRange", UNSET)

        allowed_ip_ranges = cast(List[str], d.pop("allowedIpRanges", UNSET))

        allowed_ip_addresses = cast(List[str], d.pop("allowedIpAddresses", UNSET))

        disallowed_ip_addresses = cast(List[str], d.pop("disallowedIpAddresses", UNSET))

        allowed_countries = cast(List[str], d.pop("allowedCountries", UNSET))

        disallowed_countries = cast(List[str], d.pop("disallowedCountries", UNSET))

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = MetadataDto.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        meter_attributes = []
        _meter_attributes = d.pop("meterAttributes", UNSET)
        for meter_attributes_item_data in _meter_attributes or []:
            meter_attributes_item = LicenseMeterAttributeDto.from_dict(meter_attributes_item_data)

            meter_attributes.append(meter_attributes_item)

        tags = cast(List[str], d.pop("tags", UNSET))

        license_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            key=key,
            revoked=revoked,
            suspended=suspended,
            total_activations=total_activations,
            total_deactivations=total_deactivations,
            validity=validity,
            expiration_strategy=expiration_strategy,
            fingerprint_matching_strategy=fingerprint_matching_strategy,
            allowed_activations=allowed_activations,
            allowed_deactivations=allowed_deactivations,
            type=type,
            allowed_floating_clients=allowed_floating_clients,
            server_sync_grace_period=server_sync_grace_period,
            server_sync_interval=server_sync_interval,
            allowed_clock_offset=allowed_clock_offset,
            expiring_soon_event_offset=expiring_soon_event_offset,
            lease_duration=lease_duration,
            leasing_strategy=leasing_strategy,
            expires_at=expires_at,
            allow_vm_activation=allow_vm_activation,
            allow_container_activation=allow_container_activation,
            allow_client_lease_duration=allow_client_lease_duration,
            user_locked=user_locked,
            require_authentication=require_authentication,
            disable_geo_location=disable_geo_location,
            notes=notes,
            product_id=product_id,
            product_version_id=product_version_id,
            user=user,
            reseller=reseller,
            additional_user_ids=additional_user_ids,
            allowed_ip_range=allowed_ip_range,
            allowed_ip_ranges=allowed_ip_ranges,
            allowed_ip_addresses=allowed_ip_addresses,
            disallowed_ip_addresses=disallowed_ip_addresses,
            allowed_countries=allowed_countries,
            disallowed_countries=disallowed_countries,
            metadata=metadata,
            meter_attributes=meter_attributes,
            tags=tags,
        )

        return license_dto
