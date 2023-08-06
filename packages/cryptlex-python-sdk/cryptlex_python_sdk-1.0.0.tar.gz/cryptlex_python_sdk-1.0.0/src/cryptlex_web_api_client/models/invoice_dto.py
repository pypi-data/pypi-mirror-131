import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="InvoiceDto")


@attr.s(auto_attribs=True)
class InvoiceDto:
    """ """

    id: Union[Unset, None, str] = UNSET
    date: Union[Unset, None, datetime.datetime] = UNSET
    description: Union[Unset, None, str] = UNSET
    total: Union[Unset, int] = UNSET
    paid: Union[Unset, bool] = UNSET
    period_end: Union[Unset, datetime.datetime] = UNSET
    period_start: Union[Unset, datetime.datetime] = UNSET
    invoice_pdf: Union[Unset, None, str] = UNSET
    receipt_number: Union[Unset, None, str] = UNSET
    statement_descriptor: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        date: Union[Unset, None, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat() if self.date else None

        description = self.description
        total = self.total
        paid = self.paid
        period_end: Union[Unset, str] = UNSET
        if not isinstance(self.period_end, Unset):
            period_end = self.period_end.isoformat()

        period_start: Union[Unset, str] = UNSET
        if not isinstance(self.period_start, Unset):
            period_start = self.period_start.isoformat()

        invoice_pdf = self.invoice_pdf
        receipt_number = self.receipt_number
        statement_descriptor = self.statement_descriptor

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if date is not UNSET:
            field_dict["date"] = date
        if description is not UNSET:
            field_dict["description"] = description
        if total is not UNSET:
            field_dict["total"] = total
        if paid is not UNSET:
            field_dict["paid"] = paid
        if period_end is not UNSET:
            field_dict["periodEnd"] = period_end
        if period_start is not UNSET:
            field_dict["periodStart"] = period_start
        if invoice_pdf is not UNSET:
            field_dict["invoicePdf"] = invoice_pdf
        if receipt_number is not UNSET:
            field_dict["receiptNumber"] = receipt_number
        if statement_descriptor is not UNSET:
            field_dict["statementDescriptor"] = statement_descriptor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, None, datetime.datetime]
        if _date is None:
            date = None
        elif isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        description = d.pop("description", UNSET)

        total = d.pop("total", UNSET)

        paid = d.pop("paid", UNSET)

        _period_end = d.pop("periodEnd", UNSET)
        period_end: Union[Unset, datetime.datetime]
        if isinstance(_period_end, Unset):
            period_end = UNSET
        else:
            period_end = isoparse(_period_end)

        _period_start = d.pop("periodStart", UNSET)
        period_start: Union[Unset, datetime.datetime]
        if isinstance(_period_start, Unset):
            period_start = UNSET
        else:
            period_start = isoparse(_period_start)

        invoice_pdf = d.pop("invoicePdf", UNSET)

        receipt_number = d.pop("receiptNumber", UNSET)

        statement_descriptor = d.pop("statementDescriptor", UNSET)

        invoice_dto = cls(
            id=id,
            date=date,
            description=description,
            total=total,
            paid=paid,
            period_end=period_end,
            period_start=period_start,
            invoice_pdf=invoice_pdf,
            receipt_number=receipt_number,
            statement_descriptor=statement_descriptor,
        )

        return invoice_dto
