from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.license_policy_request_model_expiration_strategy import LicensePolicyRequestModelExpirationStrategy
from ..models.license_policy_request_model_fingerprint_matching_strategy import (
    LicensePolicyRequestModelFingerprintMatchingStrategy,
)
from ..models.license_policy_request_model_leasing_strategy import LicensePolicyRequestModelLeasingStrategy
from ..models.license_policy_request_model_type import LicensePolicyRequestModelType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LicensePolicyRequestModel")


@attr.s(auto_attribs=True)
class LicensePolicyRequestModel:
    """ """

    name: Union[Unset, str] = UNSET
    fingerprint_matching_strategy: Union[Unset, LicensePolicyRequestModelFingerprintMatchingStrategy] = UNSET
    allow_vm_activation: Union[Unset, bool] = UNSET
    allow_container_activation: Union[Unset, bool] = UNSET
    user_locked: Union[Unset, bool] = UNSET
    disable_geo_location: Union[Unset, bool] = UNSET
    allowed_ip_range: Union[Unset, None, str] = UNSET
    allowed_ip_ranges: Union[Unset, None, List[str]] = UNSET
    allowed_countries: Union[Unset, None, List[str]] = UNSET
    disallowed_countries: Union[Unset, None, List[str]] = UNSET
    allowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
    disallowed_ip_addresses: Union[Unset, None, List[str]] = UNSET
    validity: Union[Unset, int] = UNSET
    expiration_strategy: Union[Unset, LicensePolicyRequestModelExpirationStrategy] = UNSET
    allowed_activations: Union[Unset, int] = UNSET
    allowed_deactivations: Union[Unset, int] = UNSET
    type: Union[Unset, LicensePolicyRequestModelType] = UNSET
    key_pattern: Union[Unset, None, str] = UNSET
    lease_duration: Union[Unset, None, int] = UNSET
    allow_client_lease_duration: Union[Unset, bool] = UNSET
    leasing_strategy: Union[Unset, None, LicensePolicyRequestModelLeasingStrategy] = UNSET
    allowed_floating_clients: Union[Unset, None, int] = UNSET
    server_sync_grace_period: Union[Unset, int] = UNSET
    server_sync_interval: Union[Unset, int] = UNSET
    allowed_clock_offset: Union[Unset, int] = UNSET
    expiring_soon_event_offset: Union[Unset, int] = UNSET
    require_authentication: Union[Unset, bool] = UNSET
    required_metadata_keys: Union[Unset, None, List[str]] = UNSET
    required_meter_attributes: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        fingerprint_matching_strategy: Union[Unset, str] = UNSET
        if not isinstance(self.fingerprint_matching_strategy, Unset):
            fingerprint_matching_strategy = self.fingerprint_matching_strategy.value

        allow_vm_activation = self.allow_vm_activation
        allow_container_activation = self.allow_container_activation
        user_locked = self.user_locked
        disable_geo_location = self.disable_geo_location
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

        validity = self.validity
        expiration_strategy: Union[Unset, str] = UNSET
        if not isinstance(self.expiration_strategy, Unset):
            expiration_strategy = self.expiration_strategy.value

        allowed_activations = self.allowed_activations
        allowed_deactivations = self.allowed_deactivations
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        key_pattern = self.key_pattern
        lease_duration = self.lease_duration
        allow_client_lease_duration = self.allow_client_lease_duration
        leasing_strategy: Union[Unset, None, str] = UNSET
        if not isinstance(self.leasing_strategy, Unset):
            leasing_strategy = self.leasing_strategy.value if self.leasing_strategy else None

        allowed_floating_clients = self.allowed_floating_clients
        server_sync_grace_period = self.server_sync_grace_period
        server_sync_interval = self.server_sync_interval
        allowed_clock_offset = self.allowed_clock_offset
        expiring_soon_event_offset = self.expiring_soon_event_offset
        require_authentication = self.require_authentication
        required_metadata_keys: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.required_metadata_keys, Unset):
            if self.required_metadata_keys is None:
                required_metadata_keys = None
            else:
                required_metadata_keys = self.required_metadata_keys

        required_meter_attributes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.required_meter_attributes, Unset):
            if self.required_meter_attributes is None:
                required_meter_attributes = None
            else:
                required_meter_attributes = self.required_meter_attributes

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if fingerprint_matching_strategy is not UNSET:
            field_dict["fingerprintMatchingStrategy"] = fingerprint_matching_strategy
        if allow_vm_activation is not UNSET:
            field_dict["allowVmActivation"] = allow_vm_activation
        if allow_container_activation is not UNSET:
            field_dict["allowContainerActivation"] = allow_container_activation
        if user_locked is not UNSET:
            field_dict["userLocked"] = user_locked
        if disable_geo_location is not UNSET:
            field_dict["disableGeoLocation"] = disable_geo_location
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
        if validity is not UNSET:
            field_dict["validity"] = validity
        if expiration_strategy is not UNSET:
            field_dict["expirationStrategy"] = expiration_strategy
        if allowed_activations is not UNSET:
            field_dict["allowedActivations"] = allowed_activations
        if allowed_deactivations is not UNSET:
            field_dict["allowedDeactivations"] = allowed_deactivations
        if type is not UNSET:
            field_dict["type"] = type
        if key_pattern is not UNSET:
            field_dict["keyPattern"] = key_pattern
        if lease_duration is not UNSET:
            field_dict["leaseDuration"] = lease_duration
        if allow_client_lease_duration is not UNSET:
            field_dict["allowClientLeaseDuration"] = allow_client_lease_duration
        if leasing_strategy is not UNSET:
            field_dict["leasingStrategy"] = leasing_strategy
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
        if require_authentication is not UNSET:
            field_dict["requireAuthentication"] = require_authentication
        if required_metadata_keys is not UNSET:
            field_dict["requiredMetadataKeys"] = required_metadata_keys
        if required_meter_attributes is not UNSET:
            field_dict["requiredMeterAttributes"] = required_meter_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _fingerprint_matching_strategy = d.pop("fingerprintMatchingStrategy", UNSET)
        fingerprint_matching_strategy: Union[Unset, LicensePolicyRequestModelFingerprintMatchingStrategy]
        if isinstance(_fingerprint_matching_strategy, Unset):
            fingerprint_matching_strategy = UNSET
        else:
            fingerprint_matching_strategy = LicensePolicyRequestModelFingerprintMatchingStrategy(
                _fingerprint_matching_strategy
            )

        allow_vm_activation = d.pop("allowVmActivation", UNSET)

        allow_container_activation = d.pop("allowContainerActivation", UNSET)

        user_locked = d.pop("userLocked", UNSET)

        disable_geo_location = d.pop("disableGeoLocation", UNSET)

        allowed_ip_range = d.pop("allowedIpRange", UNSET)

        allowed_ip_ranges = cast(List[str], d.pop("allowedIpRanges", UNSET))

        allowed_countries = cast(List[str], d.pop("allowedCountries", UNSET))

        disallowed_countries = cast(List[str], d.pop("disallowedCountries", UNSET))

        allowed_ip_addresses = cast(List[str], d.pop("allowedIpAddresses", UNSET))

        disallowed_ip_addresses = cast(List[str], d.pop("disallowedIpAddresses", UNSET))

        validity = d.pop("validity", UNSET)

        _expiration_strategy = d.pop("expirationStrategy", UNSET)
        expiration_strategy: Union[Unset, LicensePolicyRequestModelExpirationStrategy]
        if isinstance(_expiration_strategy, Unset):
            expiration_strategy = UNSET
        else:
            expiration_strategy = LicensePolicyRequestModelExpirationStrategy(_expiration_strategy)

        allowed_activations = d.pop("allowedActivations", UNSET)

        allowed_deactivations = d.pop("allowedDeactivations", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, LicensePolicyRequestModelType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = LicensePolicyRequestModelType(_type)

        key_pattern = d.pop("keyPattern", UNSET)

        lease_duration = d.pop("leaseDuration", UNSET)

        allow_client_lease_duration = d.pop("allowClientLeaseDuration", UNSET)

        _leasing_strategy = d.pop("leasingStrategy", UNSET)
        leasing_strategy: Union[Unset, None, LicensePolicyRequestModelLeasingStrategy]
        if _leasing_strategy is None:
            leasing_strategy = None
        elif isinstance(_leasing_strategy, Unset):
            leasing_strategy = UNSET
        else:
            leasing_strategy = LicensePolicyRequestModelLeasingStrategy(_leasing_strategy)

        allowed_floating_clients = d.pop("allowedFloatingClients", UNSET)

        server_sync_grace_period = d.pop("serverSyncGracePeriod", UNSET)

        server_sync_interval = d.pop("serverSyncInterval", UNSET)

        allowed_clock_offset = d.pop("allowedClockOffset", UNSET)

        expiring_soon_event_offset = d.pop("expiringSoonEventOffset", UNSET)

        require_authentication = d.pop("requireAuthentication", UNSET)

        required_metadata_keys = cast(List[str], d.pop("requiredMetadataKeys", UNSET))

        required_meter_attributes = cast(List[str], d.pop("requiredMeterAttributes", UNSET))

        license_policy_request_model = cls(
            name=name,
            fingerprint_matching_strategy=fingerprint_matching_strategy,
            allow_vm_activation=allow_vm_activation,
            allow_container_activation=allow_container_activation,
            user_locked=user_locked,
            disable_geo_location=disable_geo_location,
            allowed_ip_range=allowed_ip_range,
            allowed_ip_ranges=allowed_ip_ranges,
            allowed_countries=allowed_countries,
            disallowed_countries=disallowed_countries,
            allowed_ip_addresses=allowed_ip_addresses,
            disallowed_ip_addresses=disallowed_ip_addresses,
            validity=validity,
            expiration_strategy=expiration_strategy,
            allowed_activations=allowed_activations,
            allowed_deactivations=allowed_deactivations,
            type=type,
            key_pattern=key_pattern,
            lease_duration=lease_duration,
            allow_client_lease_duration=allow_client_lease_duration,
            leasing_strategy=leasing_strategy,
            allowed_floating_clients=allowed_floating_clients,
            server_sync_grace_period=server_sync_grace_period,
            server_sync_interval=server_sync_interval,
            allowed_clock_offset=allowed_clock_offset,
            expiring_soon_event_offset=expiring_soon_event_offset,
            require_authentication=require_authentication,
            required_metadata_keys=required_metadata_keys,
            required_meter_attributes=required_meter_attributes,
        )

        return license_policy_request_model
