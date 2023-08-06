from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountUpdateRequestModel")


@attr.s(auto_attribs=True)
class AccountUpdateRequestModel:
    """ """

    email: Union[Unset, None, str] = UNSET
    company: Union[Unset, None, str] = UNSET
    company_id: Union[Unset, None, str] = UNSET
    custom_domain: Union[Unset, None, str] = UNSET
    website: Union[Unset, None, str] = UNSET
    logo_url: Union[Unset, None, str] = UNSET
    favicon_url: Union[Unset, None, str] = UNSET
    google_client_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        company = self.company
        company_id = self.company_id
        custom_domain = self.custom_domain
        website = self.website
        logo_url = self.logo_url
        favicon_url = self.favicon_url
        google_client_id = self.google_client_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if company is not UNSET:
            field_dict["company"] = company
        if company_id is not UNSET:
            field_dict["companyId"] = company_id
        if custom_domain is not UNSET:
            field_dict["customDomain"] = custom_domain
        if website is not UNSET:
            field_dict["website"] = website
        if logo_url is not UNSET:
            field_dict["logoUrl"] = logo_url
        if favicon_url is not UNSET:
            field_dict["faviconUrl"] = favicon_url
        if google_client_id is not UNSET:
            field_dict["googleClientId"] = google_client_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        company = d.pop("company", UNSET)

        company_id = d.pop("companyId", UNSET)

        custom_domain = d.pop("customDomain", UNSET)

        website = d.pop("website", UNSET)

        logo_url = d.pop("logoUrl", UNSET)

        favicon_url = d.pop("faviconUrl", UNSET)

        google_client_id = d.pop("googleClientId", UNSET)

        account_update_request_model = cls(
            email=email,
            company=company,
            company_id=company_id,
            custom_domain=custom_domain,
            website=website,
            logo_url=logo_url,
            favicon_url=favicon_url,
            google_client_id=google_client_id,
        )

        return account_update_request_model
