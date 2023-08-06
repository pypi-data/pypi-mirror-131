from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/trial-activations/export".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "productId": product_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, HttpErrorResponseDto]]:
    if response.status_code == 200:
        response_200 = None

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
    product_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        client=client,
        product_id=product_id,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, HttpErrorResponseDto]]:
    """Exports all trial activations in the csv format."""

    return sync_detailed(
        client=client,
        product_id=product_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        client=client,
        product_id=product_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    product_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, HttpErrorResponseDto]]:
    """Exports all trial activations in the csv format."""

    return (
        await asyncio_detailed(
            client=client,
            product_id=product_id,
        )
    ).parsed
