from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.getv_3_rolesclaims_response_200 import Getv3RolesclaimsResponse200
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/v3/roles/claims".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Getv3RolesclaimsResponse200, HttpErrorResponseDto]]:
    if response.status_code == 200:
        response_200 = Getv3RolesclaimsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = HttpErrorResponseDto.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = HttpErrorResponseDto.from_dict(response.json())

        return response_403
    if response.status_code == 429:
        response_429 = HttpErrorResponseDto.from_dict(response.json())

        return response_429
    if response.status_code == 500:
        response_500 = HttpErrorResponseDto.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Getv3RolesclaimsResponse200, HttpErrorResponseDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[Getv3RolesclaimsResponse200, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[Getv3RolesclaimsResponse200, HttpErrorResponseDto]]:
    """Returns the list of all the role claims (permissions)."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[Getv3RolesclaimsResponse200, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[Getv3RolesclaimsResponse200, HttpErrorResponseDto]]:
    """Returns the list of all the role claims (permissions)."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
