from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.postv_3_product_versions_json_body import Postv3ProductVersionsJsonBody
from ...models.product_version_dto import ProductVersionDto
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Postv3ProductVersionsJsonBody,
) -> Dict[str, Any]:
    url = "{}/v3/product-versions".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, ProductVersionDto]]:
    if response.status_code == 201:
        response_201 = ProductVersionDto.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = HttpErrorResponseDto.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = HttpErrorResponseDto.from_dict(response.json())

        return response_403
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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, ProductVersionDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Postv3ProductVersionsJsonBody,
) -> Response[Union[HttpErrorResponseDto, ProductVersionDto]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: Postv3ProductVersionsJsonBody,
) -> Optional[Union[HttpErrorResponseDto, ProductVersionDto]]:
    """Creates a new product version."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Postv3ProductVersionsJsonBody,
) -> Response[Union[HttpErrorResponseDto, ProductVersionDto]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Postv3ProductVersionsJsonBody,
) -> Optional[Union[HttpErrorResponseDto, ProductVersionDto]]:
    """Creates a new product version."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
