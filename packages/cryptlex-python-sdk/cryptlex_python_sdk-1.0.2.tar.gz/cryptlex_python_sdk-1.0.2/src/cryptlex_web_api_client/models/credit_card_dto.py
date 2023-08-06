import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreditCardDto")


@attr.s(auto_attribs=True)
class CreditCardDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    brand: Union[Unset, None, str] = UNSET
    country: Union[Unset, None, str] = UNSET
    last4: Union[Unset, None, str] = UNSET
    address_zip: Union[Unset, None, str] = UNSET
    expiration_year: Union[Unset, int] = UNSET
    expiration_month: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        brand = self.brand
        country = self.country
        last4 = self.last4
        address_zip = self.address_zip
        expiration_year = self.expiration_year
        expiration_month = self.expiration_month

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if brand is not UNSET:
            field_dict["brand"] = brand
        if country is not UNSET:
            field_dict["country"] = country
        if last4 is not UNSET:
            field_dict["last4"] = last4
        if address_zip is not UNSET:
            field_dict["addressZip"] = address_zip
        if expiration_year is not UNSET:
            field_dict["expirationYear"] = expiration_year
        if expiration_month is not UNSET:
            field_dict["expirationMonth"] = expiration_month

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

        brand = d.pop("brand", UNSET)

        country = d.pop("country", UNSET)

        last4 = d.pop("last4", UNSET)

        address_zip = d.pop("addressZip", UNSET)

        expiration_year = d.pop("expirationYear", UNSET)

        expiration_month = d.pop("expirationMonth", UNSET)

        credit_card_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            brand=brand,
            country=country,
            last4=last4,
            address_zip=address_zip,
            expiration_year=expiration_year,
            expiration_month=expiration_month,
        )

        return credit_card_dto
