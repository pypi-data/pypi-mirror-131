import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.activations_by_app_version_dto import ActivationsByAppVersionDto
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    license_id: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/analytics/activations/app-version".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_start_date: Union[Unset, None, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat() if start_date else None

    json_end_date: Union[Unset, None, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat() if end_date else None

    params: Dict[str, Any] = {
        "licenseId": license_id,
        "productId": product_id,
        "startDate": json_start_date,
        "endDate": json_end_date,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HttpErrorResponseDto, List[ActivationsByAppVersionDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ActivationsByAppVersionDto.from_dict(response_200_item_data)

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


def _build_response(
    *, response: httpx.Response
) -> Response[Union[HttpErrorResponseDto, List[ActivationsByAppVersionDto]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    license_id: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ActivationsByAppVersionDto]]]:
    kwargs = _get_kwargs(
        client=client,
        license_id=license_id,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    license_id: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ActivationsByAppVersionDto]]]:
    """Retrieve activations by app version."""

    return sync_detailed(
        client=client,
        license_id=license_id,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    license_id: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ActivationsByAppVersionDto]]]:
    kwargs = _get_kwargs(
        client=client,
        license_id=license_id,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    license_id: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    start_date: Union[Unset, None, datetime.datetime] = UNSET,
    end_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ActivationsByAppVersionDto]]]:
    """Retrieve activations by app version."""

    return (
        await asyncio_detailed(
            client=client,
            license_id=license_id,
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
