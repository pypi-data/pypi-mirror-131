import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReleaseFileDto")


@attr.s(auto_attribs=True)
class ReleaseFileDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    url: Union[Unset, None, str] = UNSET
    size: Union[Unset, int] = UNSET
    downloads: Union[Unset, int] = UNSET
    extension: Union[Unset, None, str] = UNSET
    checksum: Union[Unset, None, str] = UNSET
    secured: Union[Unset, bool] = UNSET
    release_id: Union[Unset, None, str] = UNSET

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
        size = self.size
        downloads = self.downloads
        extension = self.extension
        checksum = self.checksum
        secured = self.secured
        release_id = self.release_id

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
        if size is not UNSET:
            field_dict["size"] = size
        if downloads is not UNSET:
            field_dict["downloads"] = downloads
        if extension is not UNSET:
            field_dict["extension"] = extension
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

        size = d.pop("size", UNSET)

        downloads = d.pop("downloads", UNSET)

        extension = d.pop("extension", UNSET)

        checksum = d.pop("checksum", UNSET)

        secured = d.pop("secured", UNSET)

        release_id = d.pop("releaseId", UNSET)

        release_file_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            url=url,
            size=size,
            downloads=downloads,
            extension=extension,
            checksum=checksum,
            secured=secured,
            release_id=release_id,
        )

        return release_file_dto
