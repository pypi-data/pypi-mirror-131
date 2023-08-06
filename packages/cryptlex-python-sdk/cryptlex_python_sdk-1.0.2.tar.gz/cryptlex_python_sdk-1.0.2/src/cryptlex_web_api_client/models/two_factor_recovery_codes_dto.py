from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TwoFactorRecoveryCodesDto")


@attr.s(auto_attribs=True)
class TwoFactorRecoveryCodesDto:
    """ """

    recovery_codes: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        recovery_codes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.recovery_codes, Unset):
            if self.recovery_codes is None:
                recovery_codes = None
            else:
                recovery_codes = self.recovery_codes

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if recovery_codes is not UNSET:
            field_dict["recoveryCodes"] = recovery_codes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        recovery_codes = cast(List[str], d.pop("recoveryCodes", UNSET))

        two_factor_recovery_codes_dto = cls(
            recovery_codes=recovery_codes,
        )

        return two_factor_recovery_codes_dto
