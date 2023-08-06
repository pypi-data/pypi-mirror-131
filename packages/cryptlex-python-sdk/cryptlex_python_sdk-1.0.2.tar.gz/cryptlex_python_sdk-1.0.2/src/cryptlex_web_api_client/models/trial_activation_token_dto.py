from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrialActivationTokenDto")


@attr.s(auto_attribs=True)
class TrialActivationTokenDto:
    """ """

    trial_activation_token: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        trial_activation_token = self.trial_activation_token

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if trial_activation_token is not UNSET:
            field_dict["trialActivationToken"] = trial_activation_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trial_activation_token = d.pop("trialActivationToken", UNSET)

        trial_activation_token_dto = cls(
            trial_activation_token=trial_activation_token,
        )

        return trial_activation_token_dto
