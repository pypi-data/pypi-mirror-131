from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationsByCountryDto")


@attr.s(auto_attribs=True)
class ActivationsByCountryDto:
    """ """

    activations: Union[Unset, int] = UNSET
    country_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        activations = self.activations
        country_code = self.country_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if activations is not UNSET:
            field_dict["activations"] = activations
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activations = d.pop("activations", UNSET)

        country_code = d.pop("countryCode", UNSET)

        activations_by_country_dto = cls(
            activations=activations,
            country_code=country_code,
        )

        return activations_by_country_dto
