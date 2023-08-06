from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountStatsDto")


@attr.s(auto_attribs=True)
class AccountStatsDto:
    """ """

    products: Union[Unset, int] = UNSET
    licenses: Union[Unset, int] = UNSET
    activations: Union[Unset, int] = UNSET
    trial_activations: Union[Unset, int] = UNSET
    releases: Union[Unset, int] = UNSET
    users: Union[Unset, int] = UNSET
    admins: Union[Unset, int] = UNSET
    email_templates: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        products = self.products
        licenses = self.licenses
        activations = self.activations
        trial_activations = self.trial_activations
        releases = self.releases
        users = self.users
        admins = self.admins
        email_templates = self.email_templates

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if products is not UNSET:
            field_dict["products"] = products
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if activations is not UNSET:
            field_dict["activations"] = activations
        if trial_activations is not UNSET:
            field_dict["trialActivations"] = trial_activations
        if releases is not UNSET:
            field_dict["releases"] = releases
        if users is not UNSET:
            field_dict["users"] = users
        if admins is not UNSET:
            field_dict["admins"] = admins
        if email_templates is not UNSET:
            field_dict["emailTemplates"] = email_templates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        products = d.pop("products", UNSET)

        licenses = d.pop("licenses", UNSET)

        activations = d.pop("activations", UNSET)

        trial_activations = d.pop("trialActivations", UNSET)

        releases = d.pop("releases", UNSET)

        users = d.pop("users", UNSET)

        admins = d.pop("admins", UNSET)

        email_templates = d.pop("emailTemplates", UNSET)

        account_stats_dto = cls(
            products=products,
            licenses=licenses,
            activations=activations,
            trial_activations=trial_activations,
            releases=releases,
            users=users,
            admins=admins,
            email_templates=email_templates,
        )

        return account_stats_dto
