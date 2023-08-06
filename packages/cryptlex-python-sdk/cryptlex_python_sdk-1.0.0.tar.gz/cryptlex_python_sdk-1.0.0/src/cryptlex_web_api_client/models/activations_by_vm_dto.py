from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationsByVmDto")


@attr.s(auto_attribs=True)
class ActivationsByVmDto:
    """ """

    activations: Union[Unset, int] = UNSET
    vm_name: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        activations = self.activations
        vm_name = self.vm_name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if activations is not UNSET:
            field_dict["activations"] = activations
        if vm_name is not UNSET:
            field_dict["vmName"] = vm_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activations = d.pop("activations", UNSET)

        vm_name = d.pop("vmName", UNSET)

        activations_by_vm_dto = cls(
            activations=activations,
            vm_name=vm_name,
        )

        return activations_by_vm_dto
