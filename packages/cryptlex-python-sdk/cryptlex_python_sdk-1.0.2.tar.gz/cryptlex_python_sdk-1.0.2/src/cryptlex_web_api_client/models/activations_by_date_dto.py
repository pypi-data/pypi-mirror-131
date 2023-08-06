import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivationsByDateDto")


@attr.s(auto_attribs=True)
class ActivationsByDateDto:
    """ """

    activations: Union[Unset, int] = UNSET
    activated_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        activations = self.activations
        activated_at: Union[Unset, str] = UNSET
        if not isinstance(self.activated_at, Unset):
            activated_at = self.activated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if activations is not UNSET:
            field_dict["activations"] = activations
        if activated_at is not UNSET:
            field_dict["activatedAt"] = activated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        activations = d.pop("activations", UNSET)

        _activated_at = d.pop("activatedAt", UNSET)
        activated_at: Union[Unset, datetime.datetime]
        if isinstance(_activated_at, Unset):
            activated_at = UNSET
        else:
            activated_at = isoparse(_activated_at)

        activations_by_date_dto = cls(
            activations=activations,
            activated_at=activated_at,
        )

        return activations_by_date_dto
