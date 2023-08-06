import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.getv_3_users_activationapp_version_type_1 import Getv3UsersActivationappVersionType1
from ...models.getv_3_users_company_type_1 import Getv3UsersCompanyType1
from ...models.getv_3_users_created_at_type_1 import Getv3UsersCreatedAtType1
from ...models.getv_3_users_email_type_1 import Getv3UsersEmailType1
from ...models.getv_3_users_last_seen_at_type_1 import Getv3UsersLastSeenAtType1
from ...models.getv_3_users_metadatakey_type_1 import Getv3UsersMetadatakeyType1
from ...models.getv_3_users_metadatavalue_type_1 import Getv3UsersMetadatavalueType1
from ...models.getv_3_users_role_type_1 import Getv3UsersRoleType1
from ...models.getv_3_users_tag_type_1 import Getv3UsersTagType1
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.user_dto import UserDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    role: Union[Getv3UsersRoleType1, None, Unset, str] = UNSET,
    user_type: Union[Unset, None, str] = UNSET,
    email: Union[Getv3UsersEmailType1, None, Unset, str] = UNSET,
    company: Union[Getv3UsersCompanyType1, None, Unset, str] = UNSET,
    tag: Union[Getv3UsersTagType1, None, Unset, str] = UNSET,
    tags: Union[Unset, None, List[str]] = UNSET,
    metadatakey: Union[Getv3UsersMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3UsersMetadatavalueType1, None, Unset, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    activationapp_version: Union[Getv3UsersActivationappVersionType1, None, Unset, str] = UNSET,
    created_at: Union[Getv3UsersCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    last_seen_at: Union[Getv3UsersLastSeenAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/users".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_role: Union[Dict[str, Any], None, Unset, str]
    if isinstance(role, Unset):
        json_role = UNSET
    elif role is None:
        json_role = None
    elif isinstance(role, Getv3UsersRoleType1):
        json_role = UNSET
        if not isinstance(role, Unset):
            json_role = role.to_dict()

    else:
        json_role = role

    json_email: Union[Dict[str, Any], None, Unset, str]
    if isinstance(email, Unset):
        json_email = UNSET
    elif email is None:
        json_email = None
    elif isinstance(email, Getv3UsersEmailType1):
        json_email = UNSET
        if not isinstance(email, Unset):
            json_email = email.to_dict()

    else:
        json_email = email

    json_company: Union[Dict[str, Any], None, Unset, str]
    if isinstance(company, Unset):
        json_company = UNSET
    elif company is None:
        json_company = None
    elif isinstance(company, Getv3UsersCompanyType1):
        json_company = UNSET
        if not isinstance(company, Unset):
            json_company = company.to_dict()

    else:
        json_company = company

    json_tag: Union[Dict[str, Any], None, Unset, str]
    if isinstance(tag, Unset):
        json_tag = UNSET
    elif tag is None:
        json_tag = None
    elif isinstance(tag, Getv3UsersTagType1):
        json_tag = UNSET
        if not isinstance(tag, Unset):
            json_tag = tag.to_dict()

    else:
        json_tag = tag

    json_tags: Union[Unset, None, List[str]] = UNSET
    if not isinstance(tags, Unset):
        if tags is None:
            json_tags = None
        else:
            json_tags = tags

    json_metadatakey: Union[Dict[str, Any], None, Unset, str]
    if isinstance(metadatakey, Unset):
        json_metadatakey = UNSET
    elif metadatakey is None:
        json_metadatakey = None
    elif isinstance(metadatakey, Getv3UsersMetadatakeyType1):
        json_metadatakey = UNSET
        if not isinstance(metadatakey, Unset):
            json_metadatakey = metadatakey.to_dict()

    else:
        json_metadatakey = metadatakey

    json_metadatavalue: Union[Dict[str, Any], None, Unset, str]
    if isinstance(metadatavalue, Unset):
        json_metadatavalue = UNSET
    elif metadatavalue is None:
        json_metadatavalue = None
    elif isinstance(metadatavalue, Getv3UsersMetadatavalueType1):
        json_metadatavalue = UNSET
        if not isinstance(metadatavalue, Unset):
            json_metadatavalue = metadatavalue.to_dict()

    else:
        json_metadatavalue = metadatavalue

    json_activationapp_version: Union[Dict[str, Any], None, Unset, str]
    if isinstance(activationapp_version, Unset):
        json_activationapp_version = UNSET
    elif activationapp_version is None:
        json_activationapp_version = None
    elif isinstance(activationapp_version, Getv3UsersActivationappVersionType1):
        json_activationapp_version = UNSET
        if not isinstance(activationapp_version, Unset):
            json_activationapp_version = activationapp_version.to_dict()

    else:
        json_activationapp_version = activationapp_version

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

    json_last_seen_at: Union[Dict[str, Any], None, Unset, str]
    if isinstance(last_seen_at, Unset):
        json_last_seen_at = UNSET
    elif last_seen_at is None:
        json_last_seen_at = None
    elif isinstance(last_seen_at, datetime.datetime):
        json_last_seen_at = UNSET
        if not isinstance(last_seen_at, Unset):
            json_last_seen_at = last_seen_at.isoformat()

    else:
        json_last_seen_at = UNSET
        if not isinstance(last_seen_at, Unset):
            json_last_seen_at = last_seen_at.to_dict()

    params: Dict[str, Any] = {
        "page": page,
        "limit": limit,
        "sort": sort,
        "role": json_role,
        "userType": user_type,
        "email": json_email,
        "company": json_company,
        "tag": json_tag,
        "tags": json_tags,
        "metadata.key": json_metadatakey,
        "metadata.value": json_metadatavalue,
        "productId": product_id,
        "activation.appVersion": json_activationapp_version,
        "createdAt": json_created_at,
        "lastSeenAt": json_last_seen_at,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, List[UserDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserDto.from_dict(response_200_item_data)

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, List[UserDto]]]:
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
    role: Union[Getv3UsersRoleType1, None, Unset, str] = UNSET,
    user_type: Union[Unset, None, str] = UNSET,
    email: Union[Getv3UsersEmailType1, None, Unset, str] = UNSET,
    company: Union[Getv3UsersCompanyType1, None, Unset, str] = UNSET,
    tag: Union[Getv3UsersTagType1, None, Unset, str] = UNSET,
    tags: Union[Unset, None, List[str]] = UNSET,
    metadatakey: Union[Getv3UsersMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3UsersMetadatavalueType1, None, Unset, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    activationapp_version: Union[Getv3UsersActivationappVersionType1, None, Unset, str] = UNSET,
    created_at: Union[Getv3UsersCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    last_seen_at: Union[Getv3UsersLastSeenAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[UserDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        role=role,
        user_type=user_type,
        email=email,
        company=company,
        tag=tag,
        tags=tags,
        metadatakey=metadatakey,
        metadatavalue=metadatavalue,
        product_id=product_id,
        activationapp_version=activationapp_version,
        created_at=created_at,
        last_seen_at=last_seen_at,
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
    role: Union[Getv3UsersRoleType1, None, Unset, str] = UNSET,
    user_type: Union[Unset, None, str] = UNSET,
    email: Union[Getv3UsersEmailType1, None, Unset, str] = UNSET,
    company: Union[Getv3UsersCompanyType1, None, Unset, str] = UNSET,
    tag: Union[Getv3UsersTagType1, None, Unset, str] = UNSET,
    tags: Union[Unset, None, List[str]] = UNSET,
    metadatakey: Union[Getv3UsersMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3UsersMetadatavalueType1, None, Unset, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    activationapp_version: Union[Getv3UsersActivationappVersionType1, None, Unset, str] = UNSET,
    created_at: Union[Getv3UsersCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    last_seen_at: Union[Getv3UsersLastSeenAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[UserDto]]]:
    """Returns a list of users. The users are returned sorted by creation date in ascending order."""

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        role=role,
        user_type=user_type,
        email=email,
        company=company,
        tag=tag,
        tags=tags,
        metadatakey=metadatakey,
        metadatavalue=metadatavalue,
        product_id=product_id,
        activationapp_version=activationapp_version,
        created_at=created_at,
        last_seen_at=last_seen_at,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    role: Union[Getv3UsersRoleType1, None, Unset, str] = UNSET,
    user_type: Union[Unset, None, str] = UNSET,
    email: Union[Getv3UsersEmailType1, None, Unset, str] = UNSET,
    company: Union[Getv3UsersCompanyType1, None, Unset, str] = UNSET,
    tag: Union[Getv3UsersTagType1, None, Unset, str] = UNSET,
    tags: Union[Unset, None, List[str]] = UNSET,
    metadatakey: Union[Getv3UsersMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3UsersMetadatavalueType1, None, Unset, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    activationapp_version: Union[Getv3UsersActivationappVersionType1, None, Unset, str] = UNSET,
    created_at: Union[Getv3UsersCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    last_seen_at: Union[Getv3UsersLastSeenAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[UserDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        role=role,
        user_type=user_type,
        email=email,
        company=company,
        tag=tag,
        tags=tags,
        metadatakey=metadatakey,
        metadatavalue=metadatavalue,
        product_id=product_id,
        activationapp_version=activationapp_version,
        created_at=created_at,
        last_seen_at=last_seen_at,
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
    role: Union[Getv3UsersRoleType1, None, Unset, str] = UNSET,
    user_type: Union[Unset, None, str] = UNSET,
    email: Union[Getv3UsersEmailType1, None, Unset, str] = UNSET,
    company: Union[Getv3UsersCompanyType1, None, Unset, str] = UNSET,
    tag: Union[Getv3UsersTagType1, None, Unset, str] = UNSET,
    tags: Union[Unset, None, List[str]] = UNSET,
    metadatakey: Union[Getv3UsersMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3UsersMetadatavalueType1, None, Unset, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    activationapp_version: Union[Getv3UsersActivationappVersionType1, None, Unset, str] = UNSET,
    created_at: Union[Getv3UsersCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    last_seen_at: Union[Getv3UsersLastSeenAtType1, None, Unset, datetime.datetime] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[UserDto]]]:
    """Returns a list of users. The users are returned sorted by creation date in ascending order."""

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            sort=sort,
            role=role,
            user_type=user_type,
            email=email,
            company=company,
            tag=tag,
            tags=tags,
            metadatakey=metadatakey,
            metadatavalue=metadatavalue,
            product_id=product_id,
            activationapp_version=activationapp_version,
            created_at=created_at,
            last_seen_at=last_seen_at,
            query=query,
        )
    ).parsed
