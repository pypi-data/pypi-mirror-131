from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfflineActivationDto")


@attr.s(auto_attribs=True)
class OfflineActivationDto:
    """ """

    offline_response: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        offline_response = self.offline_response

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if offline_response is not UNSET:
            field_dict["offlineResponse"] = offline_response

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        offline_response = d.pop("offlineResponse", UNSET)

        offline_activation_dto = cls(
            offline_response=offline_response,
        )

        return offline_activation_dto
