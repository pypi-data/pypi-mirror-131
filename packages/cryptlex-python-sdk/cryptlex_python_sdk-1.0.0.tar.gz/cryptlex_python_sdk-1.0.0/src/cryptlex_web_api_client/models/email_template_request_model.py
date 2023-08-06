from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailTemplateRequestModel")


@attr.s(auto_attribs=True)
class EmailTemplateRequestModel:
    """ """

    name: Union[Unset, str] = UNSET
    from_name: Union[Unset, str] = UNSET
    from_email: Union[Unset, str] = UNSET
    cc: Union[Unset, None, str] = UNSET
    bcc: Union[Unset, None, str] = UNSET
    subject: Union[Unset, str] = UNSET
    body: Union[Unset, str] = UNSET
    reply_to: Union[Unset, None, str] = UNSET
    event: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    custom: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
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

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
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

        email_template_request_model = cls(
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
        )

        return email_template_request_model
