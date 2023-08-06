from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LicenseStatsDto")


@attr.s(auto_attribs=True)
class LicenseStatsDto:
    """ """

    active: Union[Unset, int] = UNSET
    expired: Union[Unset, int] = UNSET
    expiring_soon: Union[Unset, int] = UNSET
    revoked: Union[Unset, int] = UNSET
    suspended: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        active = self.active
        expired = self.expired
        expiring_soon = self.expiring_soon
        revoked = self.revoked
        suspended = self.suspended

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
        if expired is not UNSET:
            field_dict["expired"] = expired
        if expiring_soon is not UNSET:
            field_dict["expiringSoon"] = expiring_soon
        if revoked is not UNSET:
            field_dict["revoked"] = revoked
        if suspended is not UNSET:
            field_dict["suspended"] = suspended

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        active = d.pop("active", UNSET)

        expired = d.pop("expired", UNSET)

        expiring_soon = d.pop("expiringSoon", UNSET)

        revoked = d.pop("revoked", UNSET)

        suspended = d.pop("suspended", UNSET)

        license_stats_dto = cls(
            active=active,
            expired=expired,
            expiring_soon=expiring_soon,
            revoked=revoked,
            suspended=suspended,
        )

        return license_stats_dto
