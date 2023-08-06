import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookDto")


@attr.s(auto_attribs=True)
class WebhookDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    url: Union[Unset, None, str] = UNSET
    token: Union[Unset, None, str] = UNSET
    active: Union[Unset, bool] = UNSET
    events: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        name = self.name
        url = self.url
        token = self.token
        active = self.active
        events: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            if self.events is None:
                events = None
            else:
                events = self.events

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url
        if token is not UNSET:
            field_dict["token"] = token
        if active is not UNSET:
            field_dict["active"] = active
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        token = d.pop("token", UNSET)

        active = d.pop("active", UNSET)

        events = cast(List[str], d.pop("events", UNSET))

        webhook_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            url=url,
            token=token,
            active=active,
            events=events,
        )

        return webhook_dto
