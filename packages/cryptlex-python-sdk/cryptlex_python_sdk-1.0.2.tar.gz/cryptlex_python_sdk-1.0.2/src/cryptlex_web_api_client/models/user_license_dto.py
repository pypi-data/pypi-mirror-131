import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.user_license_dto_type import UserLicenseDtoType
from ..models.user_license_meter_attribute_dto import UserLicenseMeterAttributeDto
from ..models.user_product_dto import UserProductDto
from ..models.user_product_version_dto import UserProductVersionDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserLicenseDto")


@attr.s(auto_attribs=True)
class UserLicenseDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    key: Union[Unset, None, str] = UNSET
    revoked: Union[Unset, bool] = UNSET
    suspended: Union[Unset, bool] = UNSET
    type: Union[Unset, None, UserLicenseDtoType] = UNSET
    validity: Union[Unset, int] = UNSET
    total_activations: Union[Unset, int] = UNSET
    total_deactivations: Union[Unset, int] = UNSET
    allowed_activations: Union[Unset, int] = UNSET
    allowed_deactivations: Union[Unset, int] = UNSET
    allowed_floating_clients: Union[Unset, int] = UNSET
    lease_duration: Union[Unset, int] = UNSET
    expires_at: Union[Unset, None, datetime.datetime] = UNSET
    notes: Union[Unset, None, str] = UNSET
    meter_attributes: Union[Unset, None, List[UserLicenseMeterAttributeDto]] = UNSET
    product: Union[Unset, UserProductDto] = UNSET
    product_version: Union[Unset, UserProductVersionDto] = UNSET

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
        type: Union[Unset, None, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value if self.type else None

        validity = self.validity
        total_activations = self.total_activations
        total_deactivations = self.total_deactivations
        allowed_activations = self.allowed_activations
        allowed_deactivations = self.allowed_deactivations
        allowed_floating_clients = self.allowed_floating_clients
        lease_duration = self.lease_duration
        expires_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat() if self.expires_at else None

        notes = self.notes
        meter_attributes: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.meter_attributes, Unset):
            if self.meter_attributes is None:
                meter_attributes = None
            else:
                meter_attributes = []
                for meter_attributes_item_data in self.meter_attributes:
                    meter_attributes_item = meter_attributes_item_data.to_dict()

                    meter_attributes.append(meter_attributes_item)

        product: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.product, Unset):
            product = self.product.to_dict()

        product_version: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.product_version, Unset):
            product_version = self.product_version.to_dict()

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
        if type is not UNSET:
            field_dict["type"] = type
        if validity is not UNSET:
            field_dict["validity"] = validity
        if total_activations is not UNSET:
            field_dict["totalActivations"] = total_activations
        if total_deactivations is not UNSET:
            field_dict["totalDeactivations"] = total_deactivations
        if allowed_activations is not UNSET:
            field_dict["allowedActivations"] = allowed_activations
        if allowed_deactivations is not UNSET:
            field_dict["allowedDeactivations"] = allowed_deactivations
        if allowed_floating_clients is not UNSET:
            field_dict["allowedFloatingClients"] = allowed_floating_clients
        if lease_duration is not UNSET:
            field_dict["leaseDuration"] = lease_duration
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if notes is not UNSET:
            field_dict["notes"] = notes
        if meter_attributes is not UNSET:
            field_dict["meterAttributes"] = meter_attributes
        if product is not UNSET:
            field_dict["product"] = product
        if product_version is not UNSET:
            field_dict["productVersion"] = product_version

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

        _type = d.pop("type", UNSET)
        type: Union[Unset, None, UserLicenseDtoType]
        if _type is None:
            type = None
        elif isinstance(_type, Unset):
            type = UNSET
        else:
            type = UserLicenseDtoType(_type)

        validity = d.pop("validity", UNSET)

        total_activations = d.pop("totalActivations", UNSET)

        total_deactivations = d.pop("totalDeactivations", UNSET)

        allowed_activations = d.pop("allowedActivations", UNSET)

        allowed_deactivations = d.pop("allowedDeactivations", UNSET)

        allowed_floating_clients = d.pop("allowedFloatingClients", UNSET)

        lease_duration = d.pop("leaseDuration", UNSET)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, None, datetime.datetime]
        if _expires_at is None:
            expires_at = None
        elif isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        notes = d.pop("notes", UNSET)

        meter_attributes = []
        _meter_attributes = d.pop("meterAttributes", UNSET)
        for meter_attributes_item_data in _meter_attributes or []:
            meter_attributes_item = UserLicenseMeterAttributeDto.from_dict(meter_attributes_item_data)

            meter_attributes.append(meter_attributes_item)

        _product = d.pop("product", UNSET)
        product: Union[Unset, UserProductDto]
        if isinstance(_product, Unset):
            product = UNSET
        else:
            product = UserProductDto.from_dict(_product)

        _product_version = d.pop("productVersion", UNSET)
        product_version: Union[Unset, UserProductVersionDto]
        if isinstance(_product_version, Unset):
            product_version = UNSET
        else:
            product_version = UserProductVersionDto.from_dict(_product_version)

        user_license_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            key=key,
            revoked=revoked,
            suspended=suspended,
            type=type,
            validity=validity,
            total_activations=total_activations,
            total_deactivations=total_deactivations,
            allowed_activations=allowed_activations,
            allowed_deactivations=allowed_deactivations,
            allowed_floating_clients=allowed_floating_clients,
            lease_duration=lease_duration,
            expires_at=expires_at,
            notes=notes,
            meter_attributes=meter_attributes,
            product=product,
            product_version=product_version,
        )

        return user_license_dto
