from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3ReleaseFilesJsonBody")


@attr.s(auto_attribs=True)
class Postv3ReleaseFilesJsonBody:
    """ """

    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    checksum: Union[Unset, str] = UNSET
    secured: Union[Unset, bool] = UNSET
    release_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        url = self.url
        size = self.size
        checksum = self.checksum
        secured = self.secured
        release_id = self.release_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url
        if size is not UNSET:
            field_dict["size"] = size
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if secured is not UNSET:
            field_dict["secured"] = secured
        if release_id is not UNSET:
            field_dict["releaseId"] = release_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        size = d.pop("size", UNSET)

        checksum = d.pop("checksum", UNSET)

        secured = d.pop("secured", UNSET)

        release_id = d.pop("releaseId", UNSET)

        postv_3_release_files_json_body = cls(
            name=name,
            url=url,
            size=size,
            checksum=checksum,
            secured=secured,
            release_id=release_id,
        )

        postv_3_release_files_json_body.additional_properties = d
        return postv_3_release_files_json_body

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
