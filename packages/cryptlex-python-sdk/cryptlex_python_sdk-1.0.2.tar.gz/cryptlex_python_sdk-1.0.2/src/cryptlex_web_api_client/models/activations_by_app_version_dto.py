from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationsByAppVersionDto")


@attr.s(auto_attribs=True)
class ActivationsByAppVersionDto:
    """ """

    activations: Union[Unset, int] = UNSET
    app_version: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        activations = self.activations
        app_version = self.app_version

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if activations is not UNSET:
            field_dict["activations"] = activations
        if app_version is not UNSET:
            field_dict["appVersion"] = app_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activations = d.pop("activations", UNSET)

        app_version = d.pop("appVersion", UNSET)

        activations_by_app_version_dto = cls(
            activations=activations,
            app_version=app_version,
        )

        return activations_by_app_version_dto
