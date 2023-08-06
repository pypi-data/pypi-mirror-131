import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.license_metadata_request_model import LicenseMetadataRequestModel
from ..models.license_meter_attribute_request_model import LicenseMeterAttributeRequestModel
from ..models.license_request_model_expiration_strategy import LicenseRequestModelExpirationStrategy
from ..models.license_request_model_fingerprint_matching_strategy import LicenseRequestModelFingerprintMatchingStrategy
from ..models.license_request_model_leasing_strategy import LicenseRequestModelLeasingStrategy
from ..models.license_request_model_type import LicenseRequestModelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseRequestModel")


@attr.s(auto_attribs=True)
class LicenseRequestModel:
    """ """

    key: Union[Unset, None, str] = UNSET
    revoked: Union[Unset, None, bool] = UNSET
    suspended: Union[Unset, None, bool] = UNSET
    fingerprint_matching_strategy: Union[Unset, None, LicenseRequestModelFingerprintMatchingStrategy] = UNSET
    allowed_activations: Union[Unset, None, int] = UNSET
    allowed_deactivations: Union[Unset, None, int] = UNSET
    lease_duration: Union[Unset, None, int] = UNSET
    allow_client_lease_duration: Union[Unset, None, bool] = UNSET
    allowed_floating_clients: Union[Unset, None, int] = UNSET
    server_sync_grace_period: Union[Unset, None, int] = UNSET
    server_sync_interval: Union[Unset, None, int] = UNSET
    allowed_clock_offset: Union[Unset, None, int] = UNSET
    expiring_soon_event_offset: Union[Unset, None, int] = UNSET
    allow_vm_activation: Union[Unset, None, bool] = UNSET
    allow_container_activation: Union[Unset, None, bool] = UNSET
    require_authentication: Union[Unset, None, bool] = UNSET
    disable_geo_location: Union[Unset, None, bool] = UNSET
    notes: Union[Unset, None, str] = UNSET
    allowed_ip_range: Union[Unset, None, str] = UNSET
    allowed_ip_ranges: Union[Unset, None, List[str]] = UNSET
    allowed_countries: Union[Unset, None, List[str]] = UNSET
    disallowed_countries: Union[Unset, None, List[str]] = UNSET
    allowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
    disallowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
    user_id: Union[Unset, None, str] = UNSET
    reseller_id: Union[Unset, None, str] = UNSET
    additional_user_ids: Union[Unset, None, List[str]] = UNSET
    product_version_id: Union[Unset, None, str] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    metadata: Union[Unset, None, List[LicenseMetadataRequestModel]] = UNSET
    meter_attributes: Union[Unset, None, List[LicenseMeterAttributeRequestModel]] = UNSET
    validity: Union[Unset, None, int] = UNSET
    leasing_strategy: Union[Unset, None, LicenseRequestModelLeasingStrategy] = UNSET
    user_locked: Union[Unset, None, bool] = UNSET
    expiration_strategy: Union[Unset, None, LicenseRequestModelExpirationStrategy] = UNSET
    type: Union[Unset, None, LicenseRequestModelType] = UNSET
    created_at: Union[Unset, None, datetime.datetime] = UNSET
    product_id: Union[Unset, str] = UNSET
    license_policy_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        revoked = self.revoked
        suspended = self.suspended
        fingerprint_matching_strategy: Union[Unset, None, str] = UNSET
        if not isinstance(self.fingerprint_matching_strategy, Unset):
            fingerprint_matching_strategy = (
                self.fingerprint_matching_strategy.value if self.fingerprint_matching_strategy else None
            )

        allowed_activations = self.allowed_activations
        allowed_deactivations = self.allowed_deactivations
        lease_duration = self.lease_duration
        allow_client_lease_duration = self.allow_client_lease_duration
        allowed_floating_clients = self.allowed_floating_clients
        server_sync_grace_period = self.server_sync_grace_period
        server_sync_interval = self.server_sync_interval
        allowed_clock_offset = self.allowed_clock_offset
        expiring_soon_event_offset = self.expiring_soon_event_offset
        allow_vm_activation = self.allow_vm_activation
        allow_container_activation = self.allow_container_activation
        require_authentication = self.require_authentication
        disable_geo_location = self.disable_geo_location
        notes = self.notes
        allowed_ip_range = self.allowed_ip_range
        allowed_ip_ranges: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.allowed_ip_ranges, Unset):
            if self.allowed_ip_ranges is None:
                allowed_ip_ranges = None
            else:
                allowed_ip_ranges = self.allowed_ip_ranges

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

        user_id = self.user_id
        reseller_id = self.reseller_id
        additional_user_ids: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.additional_user_ids, Unset):
            if self.additional_user_ids is None:
                additional_user_ids = None
            else:
                additional_user_ids = self.additional_user_ids

        product_version_id = self.product_version_id
        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

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

        validity = self.validity
        leasing_strategy: Union[Unset, None, str] = UNSET
        if not isinstance(self.leasing_strategy, Unset):
            leasing_strategy = self.leasing_strategy.value if self.leasing_strategy else None

        user_locked = self.user_locked
        expiration_strategy: Union[Unset, None, str] = UNSET
        if not isinstance(self.expiration_strategy, Unset):
            expiration_strategy = self.expiration_strategy.value if self.expiration_strategy else None

        type: Union[Unset, None, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value if self.type else None

        created_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat() if self.created_at else None

        product_id = self.product_id
        license_policy_id = self.license_policy_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if revoked is not UNSET:
            field_dict["revoked"] = revoked
        if suspended is not UNSET:
            field_dict["suspended"] = suspended
        if fingerprint_matching_strategy is not UNSET:
            field_dict["fingerprintMatchingStrategy"] = fingerprint_matching_strategy
        if allowed_activations is not UNSET:
            field_dict["allowedActivations"] = allowed_activations
        if allowed_deactivations is not UNSET:
            field_dict["allowedDeactivations"] = allowed_deactivations
        if lease_duration is not UNSET:
            field_dict["leaseDuration"] = lease_duration
        if allow_client_lease_duration is not UNSET:
            field_dict["allowClientLeaseDuration"] = allow_client_lease_duration
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
        if allow_vm_activation is not UNSET:
            field_dict["allowVmActivation"] = allow_vm_activation
        if allow_container_activation is not UNSET:
            field_dict["allowContainerActivation"] = allow_container_activation
        if require_authentication is not UNSET:
            field_dict["requireAuthentication"] = require_authentication
        if disable_geo_location is not UNSET:
            field_dict["disableGeoLocation"] = disable_geo_location
        if notes is not UNSET:
            field_dict["notes"] = notes
        if allowed_ip_range is not UNSET:
            field_dict["allowedIpRange"] = allowed_ip_range
        if allowed_ip_ranges is not UNSET:
            field_dict["allowedIpRanges"] = allowed_ip_ranges
        if allowed_countries is not UNSET:
            field_dict["allowedCountries"] = allowed_countries
        if disallowed_countries is not UNSET:
            field_dict["disallowedCountries"] = disallowed_countries
        if allowed_ip_addresses is not UNSET:
            field_dict["allowedIpAddresses"] = allowed_ip_addresses
        if disallowed_ip_addresses is not UNSET:
            field_dict["disallowedIpAddresses"] = disallowed_ip_addresses
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if reseller_id is not UNSET:
            field_dict["resellerId"] = reseller_id
        if additional_user_ids is not UNSET:
            field_dict["additionalUserIds"] = additional_user_ids
        if product_version_id is not UNSET:
            field_dict["productVersionId"] = product_version_id
        if tags is not UNSET:
            field_dict["tags"] = tags
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if meter_attributes is not UNSET:
            field_dict["meterAttributes"] = meter_attributes
        if validity is not UNSET:
            field_dict["validity"] = validity
        if leasing_strategy is not UNSET:
            field_dict["leasingStrategy"] = leasing_strategy
        if user_locked is not UNSET:
            field_dict["userLocked"] = user_locked
        if expiration_strategy is not UNSET:
            field_dict["expirationStrategy"] = expiration_strategy
        if type is not UNSET:
            field_dict["type"] = type
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if license_policy_id is not UNSET:
            field_dict["licensePolicyId"] = license_policy_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        revoked = d.pop("revoked", UNSET)

        suspended = d.pop("suspended", UNSET)

        _fingerprint_matching_strategy = d.pop("fingerprintMatchingStrategy", UNSET)
        fingerprint_matching_strategy: Union[Unset, None, LicenseRequestModelFingerprintMatchingStrategy]
        if _fingerprint_matching_strategy is None:
            fingerprint_matching_strategy = None
        elif isinstance(_fingerprint_matching_strategy, Unset):
            fingerprint_matching_strategy = UNSET
        else:
            fingerprint_matching_strategy = LicenseRequestModelFingerprintMatchingStrategy(
                _fingerprint_matching_strategy
            )

        allowed_activations = d.pop("allowedActivations", UNSET)

        allowed_deactivations = d.pop("allowedDeactivations", UNSET)

        lease_duration = d.pop("leaseDuration", UNSET)

        allow_client_lease_duration = d.pop("allowClientLeaseDuration", UNSET)

        allowed_floating_clients = d.pop("allowedFloatingClients", UNSET)

        server_sync_grace_period = d.pop("serverSyncGracePeriod", UNSET)

        server_sync_interval = d.pop("serverSyncInterval", UNSET)

        allowed_clock_offset = d.pop("allowedClockOffset", UNSET)

        expiring_soon_event_offset = d.pop("expiringSoonEventOffset", UNSET)

        allow_vm_activation = d.pop("allowVmActivation", UNSET)

        allow_container_activation = d.pop("allowContainerActivation", UNSET)

        require_authentication = d.pop("requireAuthentication", UNSET)

        disable_geo_location = d.pop("disableGeoLocation", UNSET)

        notes = d.pop("notes", UNSET)

        allowed_ip_range = d.pop("allowedIpRange", UNSET)

        allowed_ip_ranges = cast(List[str], d.pop("allowedIpRanges", UNSET))

        allowed_countries = cast(List[str], d.pop("allowedCountries", UNSET))

        disallowed_countries = cast(List[str], d.pop("disallowedCountries", UNSET))

        allowed_ip_addresses = cast(List[str], d.pop("allowedIpAddresses", UNSET))

        disallowed_ip_addresses = cast(List[str], d.pop("disallowedIpAddresses", UNSET))

        user_id = d.pop("userId", UNSET)

        reseller_id = d.pop("resellerId", UNSET)

        additional_user_ids = cast(List[str], d.pop("additionalUserIds", UNSET))

        product_version_id = d.pop("productVersionId", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = LicenseMetadataRequestModel.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        meter_attributes = []
        _meter_attributes = d.pop("meterAttributes", UNSET)
        for meter_attributes_item_data in _meter_attributes or []:
            meter_attributes_item = LicenseMeterAttributeRequestModel.from_dict(meter_attributes_item_data)

            meter_attributes.append(meter_attributes_item)

        validity = d.pop("validity", UNSET)

        _leasing_strategy = d.pop("leasingStrategy", UNSET)
        leasing_strategy: Union[Unset, None, LicenseRequestModelLeasingStrategy]
        if _leasing_strategy is None:
            leasing_strategy = None
        elif isinstance(_leasing_strategy, Unset):
            leasing_strategy = UNSET
        else:
            leasing_strategy = LicenseRequestModelLeasingStrategy(_leasing_strategy)

        user_locked = d.pop("userLocked", UNSET)

        _expiration_strategy = d.pop("expirationStrategy", UNSET)
        expiration_strategy: Union[Unset, None, LicenseRequestModelExpirationStrategy]
        if _expiration_strategy is None:
            expiration_strategy = None
        elif isinstance(_expiration_strategy, Unset):
            expiration_strategy = UNSET
        else:
            expiration_strategy = LicenseRequestModelExpirationStrategy(_expiration_strategy)

        _type = d.pop("type", UNSET)
        type: Union[Unset, None, LicenseRequestModelType]
        if _type is None:
            type = None
        elif isinstance(_type, Unset):
            type = UNSET
        else:
            type = LicenseRequestModelType(_type)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, None, datetime.datetime]
        if _created_at is None:
            created_at = None
        elif isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        product_id = d.pop("productId", UNSET)

        license_policy_id = d.pop("licensePolicyId", UNSET)

        license_request_model = cls(
            key=key,
            revoked=revoked,
            suspended=suspended,
            fingerprint_matching_strategy=fingerprint_matching_strategy,
            allowed_activations=allowed_activations,
            allowed_deactivations=allowed_deactivations,
            lease_duration=lease_duration,
            allow_client_lease_duration=allow_client_lease_duration,
            allowed_floating_clients=allowed_floating_clients,
            server_sync_grace_period=server_sync_grace_period,
            server_sync_interval=server_sync_interval,
            allowed_clock_offset=allowed_clock_offset,
            expiring_soon_event_offset=expiring_soon_event_offset,
            allow_vm_activation=allow_vm_activation,
            allow_container_activation=allow_container_activation,
            require_authentication=require_authentication,
            disable_geo_location=disable_geo_location,
            notes=notes,
            allowed_ip_range=allowed_ip_range,
            allowed_ip_ranges=allowed_ip_ranges,
            allowed_countries=allowed_countries,
            disallowed_countries=disallowed_countries,
            allowed_ip_addresses=allowed_ip_addresses,
            disallowed_ip_addresses=disallowed_ip_addresses,
            user_id=user_id,
            reseller_id=reseller_id,
            additional_user_ids=additional_user_ids,
            product_version_id=product_version_id,
            tags=tags,
            metadata=metadata,
            meter_attributes=meter_attributes,
            validity=validity,
            leasing_strategy=leasing_strategy,
            user_locked=user_locked,
            expiration_strategy=expiration_strategy,
            type=type,
            created_at=created_at,
            product_id=product_id,
            license_policy_id=license_policy_id,
        )

        return license_request_model
