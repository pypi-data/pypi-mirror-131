import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.activation_log_dto import ActivationLogDto
from ...models.getv_3_activation_logs_created_at_type_1 import Getv3ActivationLogsCreatedAtType1
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    license_id: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3ActivationLogsCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/activation-logs".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_created_at: Union[Dict[str, Any], None, Unset, str]
    if isinstance(created_at, Unset):
        json_created_at = UNSET
    elif created_at is None:
        json_created_at = None
    elif isinstance(created_at, datetime.datetime):
        json_created_at = UNSET
        if not isinstance(created_at, Unset):
            json_created_at = created_at.isoformat()

    else:
        json_created_at = UNSET
        if not isinstance(created_at, Unset):
            json_created_at = created_at.to_dict()

    params: Dict[str, Any] = {
        "page": page,
        "limit": limit,
        "sort": sort,
        "productId": product_id,
        "licenseId": license_id,
        "createdAt": json_created_at,
        "query": query,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, List[ActivationLogDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ActivationLogDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, List[ActivationLogDto]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    license_id: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3ActivationLogsCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ActivationLogDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        license_id=license_id,
        created_at=created_at,
        query=query,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    license_id: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3ActivationLogsCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ActivationLogDto]]]:
    """Returns a list of activation logs. The activation logs are returned sorted by creation date in ascending order."""

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        license_id=license_id,
        created_at=created_at,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    license_id: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3ActivationLogsCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ActivationLogDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        license_id=license_id,
        created_at=created_at,
        query=query,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    license_id: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3ActivationLogsCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ActivationLogDto]]]:
    """Returns a list of activation logs. The activation logs are returned sorted by creation date in ascending order."""

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            sort=sort,
            product_id=product_id,
            license_id=license_id,
            created_at=created_at,
            query=query,
        )
    ).parsed
