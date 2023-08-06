from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3ReleasesJsonBody")


@attr.s(auto_attribs=True)
class Postv3ReleasesJsonBody:
    """ """

    name: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    channel: Union[Unset, str] = UNSET
    platform: Union[Unset, str] = UNSET
    private: Union[Unset, None, bool] = UNSET
    notes: Union[Unset, None, str] = UNSET
    product_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        version = self.version
        channel = self.channel
        platform = self.platform
        private = self.private
        notes = self.notes
        product_id = self.product_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version
        if channel is not UNSET:
            field_dict["channel"] = channel
        if platform is not UNSET:
            field_dict["platform"] = platform
        if private is not UNSET:
            field_dict["private"] = private
        if notes is not UNSET:
            field_dict["notes"] = notes
        if product_id is not UNSET:
            field_dict["productId"] = product_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        version = d.pop("version", UNSET)

        channel = d.pop("channel", UNSET)

        platform = d.pop("platform", UNSET)

        private = d.pop("private", UNSET)

        notes = d.pop("notes", UNSET)

        product_id = d.pop("productId", UNSET)

        postv_3_releases_json_body = cls(
            name=name,
            version=version,
            channel=channel,
            platform=platform,
            private=private,
            notes=notes,
            product_id=product_id,
        )

        postv_3_releases_json_body.additional_properties = d
        return postv_3_releases_json_body

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
