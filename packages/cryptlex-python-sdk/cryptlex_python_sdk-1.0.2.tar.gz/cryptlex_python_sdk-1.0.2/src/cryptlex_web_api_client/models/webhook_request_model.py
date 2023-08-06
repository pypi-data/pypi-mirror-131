from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookRequestModel")


@attr.s(auto_attribs=True)
class WebhookRequestModel:
    """ """

    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    events: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        url = self.url
        token = self.token
        active = self.active
        events: Union[Unset, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            events = self.events

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
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
        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        token = d.pop("token", UNSET)

        active = d.pop("active", UNSET)

        events = cast(List[str], d.pop("events", UNSET))

        webhook_request_model = cls(
            name=name,
            url=url,
            token=token,
            active=active,
            events=events,
        )

        return webhook_request_model
