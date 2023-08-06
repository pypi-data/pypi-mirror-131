from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpErrorResponseDto")


@attr.s(auto_attribs=True)
class HttpErrorResponseDto:
    """ """

    message: str
    code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        code = self.code

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "message": message,
            }
        )
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        code = d.pop("code", UNSET)

        http_error_response_dto = cls(
            message=message,
            code=code,
        )

        return http_error_response_dto
