import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.plan_dto import PlanDto
from ..models.tenant_dto_status import TenantDtoStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantDto")


@attr.s(auto_attribs=True)
class TenantDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    company: Union[Unset, None, str] = UNSET
    email: Union[Unset, None, str] = UNSET
    status: Union[Unset, None, TenantDtoStatus] = UNSET
    custom_domain: Union[Unset, None, str] = UNSET
    website: Union[Unset, None, str] = UNSET
    logo_url: Union[Unset, None, str] = UNSET
    favicon_url: Union[Unset, None, str] = UNSET
    google_client_id: Union[Unset, None, str] = UNSET
    trial_expires_at: Union[Unset, datetime.datetime] = UNSET
    plan: Union[Unset, PlanDto] = UNSET
    company_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        company = self.company
        email = self.email
        status: Union[Unset, None, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value if self.status else None

        custom_domain = self.custom_domain
        website = self.website
        logo_url = self.logo_url
        favicon_url = self.favicon_url
        google_client_id = self.google_client_id
        trial_expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.trial_expires_at, Unset):
            trial_expires_at = self.trial_expires_at.isoformat()

        plan: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.to_dict()

        company_id = self.company_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if company is not UNSET:
            field_dict["company"] = company
        if email is not UNSET:
            field_dict["email"] = email
        if status is not UNSET:
            field_dict["status"] = status
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
        if trial_expires_at is not UNSET:
            field_dict["trialExpiresAt"] = trial_expires_at
        if plan is not UNSET:
            field_dict["plan"] = plan
        if company_id is not UNSET:
            field_dict["companyId"] = company_id

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

        company = d.pop("company", UNSET)

        email = d.pop("email", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, None, TenantDtoStatus]
        if _status is None:
            status = None
        elif isinstance(_status, Unset):
            status = UNSET
        else:
            status = TenantDtoStatus(_status)

        custom_domain = d.pop("customDomain", UNSET)

        website = d.pop("website", UNSET)

        logo_url = d.pop("logoUrl", UNSET)

        favicon_url = d.pop("faviconUrl", UNSET)

        google_client_id = d.pop("googleClientId", UNSET)

        _trial_expires_at = d.pop("trialExpiresAt", UNSET)
        trial_expires_at: Union[Unset, datetime.datetime]
        if isinstance(_trial_expires_at, Unset):
            trial_expires_at = UNSET
        else:
            trial_expires_at = isoparse(_trial_expires_at)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, PlanDto]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = PlanDto.from_dict(_plan)

        company_id = d.pop("companyId", UNSET)

        tenant_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            company=company,
            email=email,
            status=status,
            custom_domain=custom_domain,
            website=website,
            logo_url=logo_url,
            favicon_url=favicon_url,
            google_client_id=google_client_id,
            trial_expires_at=trial_expires_at,
            plan=plan,
            company_id=company_id,
        )

        return tenant_dto
