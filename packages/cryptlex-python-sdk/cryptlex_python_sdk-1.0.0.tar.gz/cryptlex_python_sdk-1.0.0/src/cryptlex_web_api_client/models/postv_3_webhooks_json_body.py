from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3WebhooksJsonBody")


@attr.s(auto_attribs=True)
class Postv3WebhooksJsonBody:
    """ """

    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    events: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        url = self.url
        token = self.token
        active = self.active
        events: Union[Unset, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            events = self.events

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        postv_3_webhooks_json_body = cls(
            name=name,
            url=url,
            token=token,
            active=active,
            events=events,
        )

        postv_3_webhooks_json_body.additional_properties = d
        return postv_3_webhooks_json_body

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
