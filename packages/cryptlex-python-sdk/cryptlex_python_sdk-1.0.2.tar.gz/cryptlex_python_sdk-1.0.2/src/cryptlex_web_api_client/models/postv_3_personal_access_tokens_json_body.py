import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3PersonalAccessTokensJsonBody")


@attr.s(auto_attribs=True)
class Postv3PersonalAccessTokensJsonBody:
    """ """

    name: Union[Unset, str] = UNSET
    revoked: Union[Unset, None, bool] = UNSET
    expires_at: Union[Unset, None, datetime.datetime] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        revoked = self.revoked
        expires_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat() if self.expires_at else None

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if revoked is not UNSET:
            field_dict["revoked"] = revoked
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        revoked = d.pop("revoked", UNSET)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, None, datetime.datetime]
        if _expires_at is None:
            expires_at = None
        elif isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        scopes = cast(List[str], d.pop("scopes", UNSET))

        postv_3_personal_access_tokens_json_body = cls(
            name=name,
            revoked=revoked,
            expires_at=expires_at,
            scopes=scopes,
        )

        postv_3_personal_access_tokens_json_body.additional_properties = d
        return postv_3_personal_access_tokens_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
