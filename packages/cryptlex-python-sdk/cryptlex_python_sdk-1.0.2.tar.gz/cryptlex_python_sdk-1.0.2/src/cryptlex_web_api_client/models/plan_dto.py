import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlanDto")


@attr.s(auto_attribs=True)
class PlanDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    display_name: Union[Unset, None, str] = UNSET
    interval: Union[Unset, None, str] = UNSET
    allowed_users: Union[Unset, int] = UNSET
    allowed_admins: Union[Unset, int] = UNSET
    allowed_products: Union[Unset, int] = UNSET
    allowed_meter_attributes: Union[Unset, int] = UNSET
    allowed_feature_flags: Union[Unset, int] = UNSET
    allowed_activations: Union[Unset, int] = UNSET
    allowed_trial_activations: Union[Unset, int] = UNSET
    allowed_releases: Union[Unset, int] = UNSET
    allowed_product_space: Union[Unset, int] = UNSET
    amount: Union[Unset, None, str] = UNSET
    allow_customer_portal_access: Union[Unset, bool] = UNSET
    allow_offline_activations: Union[Unset, bool] = UNSET
    allow_hosted_floating_licenses: Union[Unset, bool] = UNSET
    allow_on_premise_floating_licenses: Union[Unset, bool] = UNSET
    allow_custom_domain: Union[Unset, bool] = UNSET
    allow_sso: Union[Unset, bool] = UNSET
    allow_custom_roles: Union[Unset, bool] = UNSET
    allow_event_logs: Union[Unset, bool] = UNSET
    allow_custom_email_templates: Union[Unset, bool] = UNSET
    deprecated: Union[Unset, bool] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        display_name = self.display_name
        interval = self.interval
        allowed_users = self.allowed_users
        allowed_admins = self.allowed_admins
        allowed_products = self.allowed_products
        allowed_meter_attributes = self.allowed_meter_attributes
        allowed_feature_flags = self.allowed_feature_flags
        allowed_activations = self.allowed_activations
        allowed_trial_activations = self.allowed_trial_activations
        allowed_releases = self.allowed_releases
        allowed_product_space = self.allowed_product_space
        amount = self.amount
        allow_customer_portal_access = self.allow_customer_portal_access
        allow_offline_activations = self.allow_offline_activations
        allow_hosted_floating_licenses = self.allow_hosted_floating_licenses
        allow_on_premise_floating_licenses = self.allow_on_premise_floating_licenses
        allow_custom_domain = self.allow_custom_domain
        allow_sso = self.allow_sso
        allow_custom_roles = self.allow_custom_roles
        allow_event_logs = self.allow_event_logs
        allow_custom_email_templates = self.allow_custom_email_templates
        deprecated = self.deprecated
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if interval is not UNSET:
            field_dict["interval"] = interval
        if allowed_users is not UNSET:
            field_dict["allowedUsers"] = allowed_users
        if allowed_admins is not UNSET:
            field_dict["allowedAdmins"] = allowed_admins
        if allowed_products is not UNSET:
            field_dict["allowedProducts"] = allowed_products
        if allowed_meter_attributes is not UNSET:
            field_dict["allowedMeterAttributes"] = allowed_meter_attributes
        if allowed_feature_flags is not UNSET:
            field_dict["allowedFeatureFlags"] = allowed_feature_flags
        if allowed_activations is not UNSET:
            field_dict["allowedActivations"] = allowed_activations
        if allowed_trial_activations is not UNSET:
            field_dict["allowedTrialActivations"] = allowed_trial_activations
        if allowed_releases is not UNSET:
            field_dict["allowedReleases"] = allowed_releases
        if allowed_product_space is not UNSET:
            field_dict["allowedProductSpace"] = allowed_product_space
        if amount is not UNSET:
            field_dict["amount"] = amount
        if allow_customer_portal_access is not UNSET:
            field_dict["allowCustomerPortalAccess"] = allow_customer_portal_access
        if allow_offline_activations is not UNSET:
            field_dict["allowOfflineActivations"] = allow_offline_activations
        if allow_hosted_floating_licenses is not UNSET:
            field_dict["allowHostedFloatingLicenses"] = allow_hosted_floating_licenses
        if allow_on_premise_floating_licenses is not UNSET:
            field_dict["allowOnPremiseFloatingLicenses"] = allow_on_premise_floating_licenses
        if allow_custom_domain is not UNSET:
            field_dict["allowCustomDomain"] = allow_custom_domain
        if allow_sso is not UNSET:
            field_dict["allowSso"] = allow_sso
        if allow_custom_roles is not UNSET:
            field_dict["allowCustomRoles"] = allow_custom_roles
        if allow_event_logs is not UNSET:
            field_dict["allowEventLogs"] = allow_event_logs
        if allow_custom_email_templates is not UNSET:
            field_dict["allowCustomEmailTemplates"] = allow_custom_email_templates
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        interval = d.pop("interval", UNSET)

        allowed_users = d.pop("allowedUsers", UNSET)

        allowed_admins = d.pop("allowedAdmins", UNSET)

        allowed_products = d.pop("allowedProducts", UNSET)

        allowed_meter_attributes = d.pop("allowedMeterAttributes", UNSET)

        allowed_feature_flags = d.pop("allowedFeatureFlags", UNSET)

        allowed_activations = d.pop("allowedActivations", UNSET)

        allowed_trial_activations = d.pop("allowedTrialActivations", UNSET)

        allowed_releases = d.pop("allowedReleases", UNSET)

        allowed_product_space = d.pop("allowedProductSpace", UNSET)

        amount = d.pop("amount", UNSET)

        allow_customer_portal_access = d.pop("allowCustomerPortalAccess", UNSET)

        allow_offline_activations = d.pop("allowOfflineActivations", UNSET)

        allow_hosted_floating_licenses = d.pop("allowHostedFloatingLicenses", UNSET)

        allow_on_premise_floating_licenses = d.pop("allowOnPremiseFloatingLicenses", UNSET)

        allow_custom_domain = d.pop("allowCustomDomain", UNSET)

        allow_sso = d.pop("allowSso", UNSET)

        allow_custom_roles = d.pop("allowCustomRoles", UNSET)

        allow_event_logs = d.pop("allowEventLogs", UNSET)

        allow_custom_email_templates = d.pop("allowCustomEmailTemplates", UNSET)

        deprecated = d.pop("deprecated", UNSET)

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

        plan_dto = cls(
            id=id,
            name=name,
            display_name=display_name,
            interval=interval,
            allowed_users=allowed_users,
            allowed_admins=allowed_admins,
            allowed_products=allowed_products,
            allowed_meter_attributes=allowed_meter_attributes,
            allowed_feature_flags=allowed_feature_flags,
            allowed_activations=allowed_activations,
            allowed_trial_activations=allowed_trial_activations,
            allowed_releases=allowed_releases,
            allowed_product_space=allowed_product_space,
            amount=amount,
            allow_customer_portal_access=allow_customer_portal_access,
            allow_offline_activations=allow_offline_activations,
            allow_hosted_floating_licenses=allow_hosted_floating_licenses,
            allow_on_premise_floating_licenses=allow_on_premise_floating_licenses,
            allow_custom_domain=allow_custom_domain,
            allow_sso=allow_sso,
            allow_custom_roles=allow_custom_roles,
            allow_event_logs=allow_event_logs,
            allow_custom_email_templates=allow_custom_email_templates,
            deprecated=deprecated,
            created_at=created_at,
            updated_at=updated_at,
        )

        return plan_dto
