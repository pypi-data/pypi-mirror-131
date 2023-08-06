from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="PersonalAccessTokenRevokeRequestModel")


@attr.s(auto_attribs=True)
class PersonalAccessTokenRevokeRequestModel:
    """ """

    revoked: bool

    def to_dict(self) -> Dict[str, Any]:
        revoked = self.revoked

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "revoked": revoked,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        revoked = d.pop("revoked")

        personal_access_token_revoke_request_model = cls(
            revoked=revoked,
        )

        return personal_access_token_revoke_request_model
