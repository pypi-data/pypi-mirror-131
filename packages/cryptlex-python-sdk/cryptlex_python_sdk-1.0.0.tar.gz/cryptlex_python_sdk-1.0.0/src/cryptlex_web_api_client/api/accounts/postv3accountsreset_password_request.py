from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.postv_3_accountsreset_password_request_json_body import Postv3AccountsresetPasswordRequestJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: Postv3AccountsresetPasswordRequestJsonBody,
    origin: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/accounts/reset-password-request".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if origin is not UNSET:
        headers["origin"] = origin

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HttpErrorResponseDto]]:
    if response.status_code == 202:
        response_202 = None

        return response_202
    if response.status_code == 400:
        response_400 = HttpErrorResponseDto.from_dict(response.json())

        return response_400
    if response.status_code == 409:
        response_409 = HttpErrorResponseDto.from_dict(response.json())

        return response_409
    if response.status_code == 429:
        response_429 = HttpErrorResponseDto.from_dict(response.json())

        return response_429
    if response.status_code == 500:
        response_500 = HttpErrorResponseDto.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, HttpErrorResponseDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Postv3AccountsresetPasswordRequestJsonBody,
    origin: Union[Unset, str] = UNSET,
) -> Response[Union[Any, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        origin=origin,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: Postv3AccountsresetPasswordRequestJsonBody,
    origin: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, HttpErrorResponseDto]]:
    """Sends the reset password email."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        origin=origin,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Postv3AccountsresetPasswordRequestJsonBody,
    origin: Union[Unset, str] = UNSET,
) -> Response[Union[Any, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        origin=origin,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Postv3AccountsresetPasswordRequestJsonBody,
    origin: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, HttpErrorResponseDto]]:
    """Sends the reset password email."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            origin=origin,
        )
    ).parsed
