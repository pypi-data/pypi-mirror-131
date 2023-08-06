import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailTemplateDto")


@attr.s(auto_attribs=True)
class EmailTemplateDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    from_name: Union[Unset, None, str] = UNSET
    from_email: Union[Unset, None, str] = UNSET
    cc: Union[Unset, None, str] = UNSET
    bcc: Union[Unset, None, str] = UNSET
    subject: Union[Unset, None, str] = UNSET
    body: Union[Unset, None, str] = UNSET
    reply_to: Union[Unset, None, str] = UNSET
    event: Union[Unset, None, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    custom: Union[Unset, bool] = UNSET
    domain_verified: Union[Unset, bool] = UNSET
    sent: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        name = self.name
        from_name = self.from_name
        from_email = self.from_email
        cc = self.cc
        bcc = self.bcc
        subject = self.subject
        body = self.body
        reply_to = self.reply_to
        event = self.event
        enabled = self.enabled
        custom = self.custom
        domain_verified = self.domain_verified
        sent = self.sent

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
        if from_name is not UNSET:
            field_dict["fromName"] = from_name
        if from_email is not UNSET:
            field_dict["fromEmail"] = from_email
        if cc is not UNSET:
            field_dict["cc"] = cc
        if bcc is not UNSET:
            field_dict["bcc"] = bcc
        if subject is not UNSET:
            field_dict["subject"] = subject
        if body is not UNSET:
            field_dict["body"] = body
        if reply_to is not UNSET:
            field_dict["replyTo"] = reply_to
        if event is not UNSET:
            field_dict["event"] = event
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if custom is not UNSET:
            field_dict["custom"] = custom
        if domain_verified is not UNSET:
            field_dict["domainVerified"] = domain_verified
        if sent is not UNSET:
            field_dict["sent"] = sent

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

        from_name = d.pop("fromName", UNSET)

        from_email = d.pop("fromEmail", UNSET)

        cc = d.pop("cc", UNSET)

        bcc = d.pop("bcc", UNSET)

        subject = d.pop("subject", UNSET)

        body = d.pop("body", UNSET)

        reply_to = d.pop("replyTo", UNSET)

        event = d.pop("event", UNSET)

        enabled = d.pop("enabled", UNSET)

        custom = d.pop("custom", UNSET)

        domain_verified = d.pop("domainVerified", UNSET)

        sent = d.pop("sent", UNSET)

        email_template_dto = cls(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            from_name=from_name,
            from_email=from_email,
            cc=cc,
            bcc=bcc,
            subject=subject,
            body=body,
            reply_to=reply_to,
            event=event,
            enabled=enabled,
            custom=custom,
            domain_verified=domain_verified,
            sent=sent,
        )

        return email_template_dto
