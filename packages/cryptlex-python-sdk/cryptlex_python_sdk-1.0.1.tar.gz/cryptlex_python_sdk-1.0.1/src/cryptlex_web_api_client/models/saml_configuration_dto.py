import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.saml_role_mapping_dto import SamlRoleMappingDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="SamlConfigurationDto")


@attr.s(auto_attribs=True)
class SamlConfigurationDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    metadata_url: Union[Unset, None, str] = UNSET
    assertion_consumer_service_url: Union[Unset, None, str] = UNSET
    return_url: Union[Unset, None, str] = UNSET
    entity_id: Union[Unset, None, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    auto_provision_users: Union[Unset, bool] = UNSET
    saml_role_mappings: Union[Unset, None, List[SamlRoleMappingDto]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        metadata_url = self.metadata_url
        assertion_consumer_service_url = self.assertion_consumer_service_url
        return_url = self.return_url
        entity_id = self.entity_id
        enabled = self.enabled
        auto_provision_users = self.auto_provision_users
        saml_role_mappings: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.saml_role_mappings, Unset):
            if self.saml_role_mappings is None:
                saml_role_mappings = None
            else:
                saml_role_mappings = []
                for saml_role_mappings_item_data in self.saml_role_mappings:
                    saml_role_mappings_item = saml_role_mappings_item_data.to_dict()

                    saml_role_mappings.append(saml_role_mappings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if metadata_url is not UNSET:
            field_dict["metadataUrl"] = metadata_url
        if assertion_consumer_service_url is not UNSET:
            field_dict["assertionConsumerServiceUrl"] = assertion_consumer_service_url
        if return_url is not UNSET:
            field_dict["returnUrl"] = return_url
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if auto_provision_users is not UNSET:
            field_dict["autoProvisionUsers"] = auto_provision_users
        if saml_role_mappings is not UNSET:
            field_dict["samlRoleMappings"] = saml_role_mappings

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

        metadata_url = d.pop("metadataUrl", UNSET)

        assertion_consumer_service_url = d.pop("assertionConsumerServiceUrl", UNSET)

        return_url = d.pop("returnUrl", UNSET)

        entity_id = d.pop("entityId", UNSET)

        enabled = d.pop("enabled", UNSET)

        auto_provision_users = d.pop("autoProvisionUsers", UNSET)

        saml_role_mappings = []
        _saml_role_mappings = d.pop("samlRoleMappings", UNSET)
        for saml_role_mappings_item_data in _saml_role_mappings or []:
            saml_role_mappings_item = SamlRoleMappingDto.from_dict(saml_role_mappings_item_data)

            saml_role_mappings.append(saml_role_mappings_item)

        saml_configuration_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            metadata_url=metadata_url,
            assertion_consumer_service_url=assertion_consumer_service_url,
            return_url=return_url,
            entity_id=entity_id,
            enabled=enabled,
            auto_provision_users=auto_provision_users,
            saml_role_mappings=saml_role_mappings,
        )

        return saml_configuration_dto
