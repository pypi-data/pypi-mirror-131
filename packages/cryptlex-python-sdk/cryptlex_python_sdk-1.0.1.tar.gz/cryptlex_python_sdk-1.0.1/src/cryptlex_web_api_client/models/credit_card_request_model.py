from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="CreditCardRequestModel")


@attr.s(auto_attribs=True)
class CreditCardRequestModel:
    """ """

    expiration_month: int
    expiration_year: int
    address_zip: str

    def to_dict(self) -> Dict[str, Any]:
        expiration_month = self.expiration_month
        expiration_year = self.expiration_year
        address_zip = self.address_zip

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expirationMonth": expiration_month,
                "expirationYear": expiration_year,
                "addressZip": address_zip,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expiration_month = d.pop("expirationMonth")

        expiration_year = d.pop("expirationYear")

        address_zip = d.pop("addressZip")

        credit_card_request_model = cls(
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            address_zip=address_zip,
        )

        return credit_card_request_model
