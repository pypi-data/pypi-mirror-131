from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.activations_by_os_dto_os import ActivationsByOsDtoOs
from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationsByOsDto")


@attr.s(auto_attribs=True)
class ActivationsByOsDto:
    """ """

    activations: Union[Unset, int] = UNSET
    os: Union[Unset, None, ActivationsByOsDtoOs] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        activations = self.activations
        os: Union[Unset, None, str] = UNSET
        if not isinstance(self.os, Unset):
            os = self.os.value if self.os else None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if activations is not UNSET:
            field_dict["activations"] = activations
        if os is not UNSET:
            field_dict["os"] = os

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activations = d.pop("activations", UNSET)

        _os = d.pop("os", UNSET)
        os: Union[Unset, None, ActivationsByOsDtoOs]
        if _os is None:
            os = None
        elif isinstance(_os, Unset):
            os = UNSET
        else:
            os = ActivationsByOsDtoOs(_os)

        activations_by_os_dto = cls(
            activations=activations,
            os=os,
        )

        return activations_by_os_dto
