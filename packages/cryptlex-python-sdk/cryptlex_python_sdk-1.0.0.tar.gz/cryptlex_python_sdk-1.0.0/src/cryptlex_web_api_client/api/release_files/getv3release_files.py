from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.getv_3_release_files_name_type_1 import Getv3ReleaseFilesNameType1
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.release_file_dto import ReleaseFileDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    release_id: str,
    name: Union[Getv3ReleaseFilesNameType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/release-files".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_name: Union[Dict[str, Any], None, Unset, str]
    if isinstance(name, Unset):
        json_name = UNSET
    elif name is None:
        json_name = None
    elif isinstance(name, Getv3ReleaseFilesNameType1):
        json_name = UNSET
        if not isinstance(name, Unset):
            json_name = name.to_dict()

    else:
        json_name = name

    params: Dict[str, Any] = {
        "page": page,
        "limit": limit,
        "sort": sort,
        "releaseId": release_id,
        "name": json_name,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, List[ReleaseFileDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ReleaseFileDto.from_dict(response_200_item_data)

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, List[ReleaseFileDto]]]:
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
    release_id: str,
    name: Union[Getv3ReleaseFilesNameType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ReleaseFileDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        release_id=release_id,
        name=name,
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
    release_id: str,
    name: Union[Getv3ReleaseFilesNameType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ReleaseFileDto]]]:
    """Returns a list of release files. The release files are returned sorted by creation date in ascending order."""

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        release_id=release_id,
        name=name,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    release_id: str,
    name: Union[Getv3ReleaseFilesNameType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[ReleaseFileDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        release_id=release_id,
        name=name,
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
    release_id: str,
    name: Union[Getv3ReleaseFilesNameType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[ReleaseFileDto]]]:
    """Returns a list of release files. The release files are returned sorted by creation date in ascending order."""

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            sort=sort,
            release_id=release_id,
            name=name,
            query=query,
        )
    ).parsed
