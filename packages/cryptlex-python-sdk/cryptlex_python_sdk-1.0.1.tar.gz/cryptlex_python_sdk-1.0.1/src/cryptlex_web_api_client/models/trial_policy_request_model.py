from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.trial_policy_request_model_fingerprint_matching_strategy import (
    TrialPolicyRequestModelFingerprintMatchingStrategy,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TrialPolicyRequestModel")


@attr.s(auto_attribs=True)
class TrialPolicyRequestModel:
    """ """

    name: Union[Unset, str] = UNSET
    fingerprint_matching_strategy: Union[Unset, TrialPolicyRequestModelFingerprintMatchingStrategy] = UNSET
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
    trial_length: Union[Unset, int] = UNSET

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

        trial_length = self.trial_length

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
        if trial_length is not UNSET:
            field_dict["trialLength"] = trial_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _fingerprint_matching_strategy = d.pop("fingerprintMatchingStrategy", UNSET)
        fingerprint_matching_strategy: Union[Unset, TrialPolicyRequestModelFingerprintMatchingStrategy]
        if isinstance(_fingerprint_matching_strategy, Unset):
            fingerprint_matching_strategy = UNSET
        else:
            fingerprint_matching_strategy = TrialPolicyRequestModelFingerprintMatchingStrategy(
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

        trial_length = d.pop("trialLength", UNSET)

        trial_policy_request_model = cls(
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
            trial_length=trial_length,
        )

        return trial_policy_request_model
