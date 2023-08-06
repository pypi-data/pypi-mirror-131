from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationsByOsVersionDto")


@attr.s(auto_attribs=True)
class ActivationsByOsVersionDto:
    """ """

    activations: Union[Unset, int] = UNSET
    os_version: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        activations = self.activations
        os_version = self.os_version

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if activations is not UNSET:
            field_dict["activations"] = activations
        if os_version is not UNSET:
            field_dict["osVersion"] = os_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activations = d.pop("activations", UNSET)

        os_version = d.pop("osVersion", UNSET)

        activations_by_os_version_dto = cls(
            activations=activations,
            os_version=os_version,
        )

        return activations_by_os_version_dto
