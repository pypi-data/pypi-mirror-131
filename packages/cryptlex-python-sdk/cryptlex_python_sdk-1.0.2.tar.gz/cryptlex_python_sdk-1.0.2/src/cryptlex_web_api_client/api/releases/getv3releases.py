from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.getv_3_releases_channel_type_1 import Getv3ReleasesChannelType1
from ...models.getv_3_releases_name_type_1 import Getv3ReleasesNameType1
from ...models.getv_3_releases_platform_type_1 import Getv3ReleasesPlatformType1
from ...models.getv_3_releases_version_type_1 import Getv3ReleasesVersionType1
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.release_dto import ReleaseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: str,
    name: Union[Getv3ReleasesNameType1, None, Unset, str] = UNSET,
    platform: Union[Getv3ReleasesPlatformType1, None, Unset, str] = UNSET,
    channel: Union[Getv3ReleasesChannelType1, None, Unset, str] = UNSET,
    version: Union[Getv3ReleasesVersionType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/releases".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_name: Union[Dict[str, Any], None, Unset, str]
    if isinstance(name, Unset):
        json_name = UNSET
    elif name is None:
        json_name = None
    elif isinstance(name, Getv3ReleasesNameType1):
        json_name = UNSET
        if not isinstance(name, Unset):
            json_name = name.to_dict()

    else:
        json_name = name

    json_platform: Union[Dict[str, Any], None, Unset, str]
    if isinstance(platform, Unset):
        json_platform = UNSET
    elif platform is None:
        json_platform = None
    elif isinstance(platform, Getv3ReleasesPlatformType1):
        json_platform = UNSET
        if not isinstance(platform, Unset):
            json_platform = platform.to_dict()

    else:
        json_platform = platform

    json_channel: Union[Dict[str, Any], None, Unset, str]
    if isinstance(channel, Unset):
        json_channel = UNSET
    elif channel is None:
        json_channel = None
    elif isinstance(channel, Getv3ReleasesChannelType1):
        json_channel = UNSET
        if not isinstance(channel, Unset):
            json_channel = channel.to_dict()

    else:
        json_channel = channel

    json_version: Union[Dict[str, Any], None, Unset, str]
    if isinstance(version, Unset):
        json_version = UNSET
    elif version is None:
        json_version = None
    elif isinstance(version, Getv3ReleasesVersionType1):
        json_version = UNSET
        if not isinstance(version, Unset):
            json_version = version.to_dict()

    else:
        json_version = version

    params: Dict[str, Any] = {
        "page": page,
        "limit": limit,
        "sort": sort,
        "productId": product_id,
        "name": json_name,
        "platform": json_platform,
        "channel": json_channel,
        "version": json_version,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, List[ReleaseDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ReleaseDto.from_dict(response_200_item_data)

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, List[ReleaseDto]]]:
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
    product_id: str,
    name: Union[Getv3ReleasesNameType1, None, Unset, str] = UNSET,
    platform: Union[Getv3ReleasesPlatformType1, None, Unset, str] = UNSET,
    channel: Union[Getv3ReleasesChannelType1, None, Unset, str] = UNSET,
    version: Union[Getv3ReleasesVersionType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ReleaseDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        name=name,
        platform=platform,
        channel=channel,
        version=version,
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
    product_id: str,
    name: Union[Getv3ReleasesNameType1, None, Unset, str] = UNSET,
    platform: Union[Getv3ReleasesPlatformType1, None, Unset, str] = UNSET,
    channel: Union[Getv3ReleasesChannelType1, None, Unset, str] = UNSET,
    version: Union[Getv3ReleasesVersionType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ReleaseDto]]]:
    """Returns a list of releases. The releases are returned sorted by creation date in ascending order."""

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        name=name,
        platform=platform,
        channel=channel,
        version=version,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: str,
    name: Union[Getv3ReleasesNameType1, None, Unset, str] = UNSET,
    platform: Union[Getv3ReleasesPlatformType1, None, Unset, str] = UNSET,
    channel: Union[Getv3ReleasesChannelType1, None, Unset, str] = UNSET,
    version: Union[Getv3ReleasesVersionType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ReleaseDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        name=name,
        platform=platform,
        channel=channel,
        version=version,
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
    product_id: str,
    name: Union[Getv3ReleasesNameType1, None, Unset, str] = UNSET,
    platform: Union[Getv3ReleasesPlatformType1, None, Unset, str] = UNSET,
    channel: Union[Getv3ReleasesChannelType1, None, Unset, str] = UNSET,
    version: Union[Getv3ReleasesVersionType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ReleaseDto]]]:
    """Returns a list of releases. The releases are returned sorted by creation date in ascending order."""

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            sort=sort,
            product_id=product_id,
            name=name,
            platform=platform,
            channel=channel,
            version=version,
            query=query,
        )
    ).parsed
