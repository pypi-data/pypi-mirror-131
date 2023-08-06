import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.changes_dto import ChangesDto
from ..models.user_dto import UserDto
from ..types import UNSET, Unset

T = TypeVar("T", bound="EventLogDto")


@attr.s(auto_attribs=True)
class EventLogDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    resource: Union[Unset, None, str] = UNSET
    action: Union[Unset, None, str] = UNSET
    changes: Union[Unset, None, List[ChangesDto]] = UNSET
    resource_id: Union[Unset, None, str] = UNSET
    ip_address: Union[Unset, None, str] = UNSET
    user: Union[Unset, UserDto] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        resource = self.resource
        action = self.action
        changes: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.changes, Unset):
            if self.changes is None:
                changes = None
            else:
                changes = []
                for changes_item_data in self.changes:
                    changes_item = changes_item_data.to_dict()

                    changes.append(changes_item)

        resource_id = self.resource_id
        ip_address = self.ip_address
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if resource is not UNSET:
            field_dict["resource"] = resource
        if action is not UNSET:
            field_dict["action"] = action
        if changes is not UNSET:
            field_dict["changes"] = changes
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if ip_address is not UNSET:
            field_dict["ipAddress"] = ip_address
        if user is not UNSET:
            field_dict["user"] = user

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

        resource = d.pop("resource", UNSET)

        action = d.pop("action", UNSET)

        changes = []
        _changes = d.pop("changes", UNSET)
        for changes_item_data in _changes or []:
            changes_item = ChangesDto.from_dict(changes_item_data)

            changes.append(changes_item)

        resource_id = d.pop("resourceId", UNSET)

        ip_address = d.pop("ipAddress", UNSET)

        _user = d.pop("user", UNSET)
        user: Union[Unset, UserDto]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = UserDto.from_dict(_user)

        event_log_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            resource=resource,
            action=action,
            changes=changes,
            resource_id=resource_id,
            ip_address=ip_address,
            user=user,
        )

        return event_log_dto
