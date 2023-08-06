import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.release_file_dto import ReleaseFileDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReleaseDto")


@attr.s(auto_attribs=True)
class ReleaseDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    channel: Union[Unset, None, str] = UNSET
    version: Union[Unset, None, str] = UNSET
    platform: Union[Unset, None, str] = UNSET
    notes: Union[Unset, None, str] = UNSET
    total_files: Union[Unset, int] = UNSET
    files: Union[Unset, None, List[ReleaseFileDto]] = UNSET
    published: Union[Unset, bool] = UNSET
    private: Union[Unset, bool] = UNSET
    product_id: Union[Unset, None, str] = UNSET
    tenant_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        name = self.name
        channel = self.channel
        version = self.version
        platform = self.platform
        notes = self.notes
        total_files = self.total_files
        files: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            if self.files is None:
                files = None
            else:
                files = []
                for files_item_data in self.files:
                    files_item = files_item_data.to_dict()

                    files.append(files_item)

        published = self.published
        private = self.private
        product_id = self.product_id
        tenant_id = self.tenant_id

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
        if channel is not UNSET:
            field_dict["channel"] = channel
        if version is not UNSET:
            field_dict["version"] = version
        if platform is not UNSET:
            field_dict["platform"] = platform
        if notes is not UNSET:
            field_dict["notes"] = notes
        if total_files is not UNSET:
            field_dict["totalFiles"] = total_files
        if files is not UNSET:
            field_dict["files"] = files
        if published is not UNSET:
            field_dict["published"] = published
        if private is not UNSET:
            field_dict["private"] = private
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

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

        channel = d.pop("channel", UNSET)

        version = d.pop("version", UNSET)

        platform = d.pop("platform", UNSET)

        notes = d.pop("notes", UNSET)

        total_files = d.pop("totalFiles", UNSET)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = ReleaseFileDto.from_dict(files_item_data)

            files.append(files_item)

        published = d.pop("published", UNSET)

        private = d.pop("private", UNSET)

        product_id = d.pop("productId", UNSET)

        tenant_id = d.pop("tenantId", UNSET)

        release_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            channel=channel,
            version=version,
            platform=platform,
            notes=notes,
            total_files=total_files,
            files=files,
            published=published,
            private=private,
            product_id=product_id,
            tenant_id=tenant_id,
        )

        return release_dto
