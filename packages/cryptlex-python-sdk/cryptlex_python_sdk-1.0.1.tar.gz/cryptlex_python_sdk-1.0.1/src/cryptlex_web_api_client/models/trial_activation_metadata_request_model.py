from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TrialActivationMetadataRequestModel")


@attr.s(auto_attribs=True)
class TrialActivationMetadataRequestModel:
    """ """

    key: str
    value: str

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        value = d.pop("value")

        trial_activation_metadata_request_model = cls(
            key=key,
            value=value,
        )

        return trial_activation_metadata_request_model
