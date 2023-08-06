from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="SamlRoleMappingRequestModel")


@attr.s(auto_attribs=True)
class SamlRoleMappingRequestModel:
    """ """

    identity_provider_role: str
    service_provider_role: str

    def to_dict(self) -> Dict[str, Any]:
        identity_provider_role = self.identity_provider_role
        service_provider_role = self.service_provider_role

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "identityProviderRole": identity_provider_role,
                "serviceProviderRole": service_provider_role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        identity_provider_role = d.pop("identityProviderRole")

        service_provider_role = d.pop("serviceProviderRole")

        saml_role_mapping_request_model = cls(
            identity_provider_role=identity_provider_role,
            service_provider_role=service_provider_role,
        )

        return saml_role_mapping_request_model
