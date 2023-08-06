import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.getv_3_licenses_allowed_activations_type_1 import Getv3LicensesAllowedActivationsType1
from ...models.getv_3_licenses_allowed_deactivations_type_1 import Getv3LicensesAllowedDeactivationsType1
from ...models.getv_3_licenses_created_at_type_1 import Getv3LicensesCreatedAtType1
from ...models.getv_3_licenses_key_type_1 import Getv3LicensesKeyType1
from ...models.getv_3_licenses_metadatakey_type_1 import Getv3LicensesMetadatakeyType1
from ...models.getv_3_licenses_metadatavalue_type_1 import Getv3LicensesMetadatavalueType1
from ...models.getv_3_licenses_tag_type_1 import Getv3LicensesTagType1
from ...models.getv_3_licenses_total_activations_type_1 import Getv3LicensesTotalActivationsType1
from ...models.getv_3_licenses_total_deactivations_type_1 import Getv3LicensesTotalDeactivationsType1
from ...models.getv_3_licenses_usercompany_type_1 import Getv3LicensesUsercompanyType1
from ...models.getv_3_licenses_useremail_type_1 import Getv3LicensesUseremailType1
from ...models.getv_3_licenses_validity_type_1 import Getv3LicensesValidityType1
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.license_dto import LicenseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    product_version_id: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    reseller_id: Union[Unset, None, str] = UNSET,
    useremail: Union[Getv3LicensesUseremailType1, None, Unset, str] = UNSET,
    usercompany: Union[Getv3LicensesUsercompanyType1, None, Unset, str] = UNSET,
    key: Union[Getv3LicensesKeyType1, None, Unset, str] = UNSET,
    revoked: Union[Unset, None, bool] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    validity: Union[Getv3LicensesValidityType1, None, Unset, int] = UNSET,
    allowed_activations: Union[Getv3LicensesAllowedActivationsType1, None, Unset, int] = UNSET,
    allowed_deactivations: Union[Getv3LicensesAllowedDeactivationsType1, None, Unset, int] = UNSET,
    total_activations: Union[Getv3LicensesTotalActivationsType1, None, Unset, int] = UNSET,
    total_deactivations: Union[Getv3LicensesTotalDeactivationsType1, None, Unset, int] = UNSET,
    allow_vm_activation: Union[Unset, None, bool] = UNSET,
    user_locked: Union[Unset, None, bool] = UNSET,
    expired: Union[Unset, None, bool] = UNSET,
    expiration_strategy: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3LicensesCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    tag: Union[Getv3LicensesTagType1, None, Unset, str] = UNSET,
    metadatakey: Union[Getv3LicensesMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3LicensesMetadatavalueType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/v3/licenses".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_useremail: Union[Dict[str, Any], None, Unset, str]
    if isinstance(useremail, Unset):
        json_useremail = UNSET
    elif useremail is None:
        json_useremail = None
    elif isinstance(useremail, Getv3LicensesUseremailType1):
        json_useremail = UNSET
        if not isinstance(useremail, Unset):
            json_useremail = useremail.to_dict()

    else:
        json_useremail = useremail

    json_usercompany: Union[Dict[str, Any], None, Unset, str]
    if isinstance(usercompany, Unset):
        json_usercompany = UNSET
    elif usercompany is None:
        json_usercompany = None
    elif isinstance(usercompany, Getv3LicensesUsercompanyType1):
        json_usercompany = UNSET
        if not isinstance(usercompany, Unset):
            json_usercompany = usercompany.to_dict()

    else:
        json_usercompany = usercompany

    json_key: Union[Dict[str, Any], None, Unset, str]
    if isinstance(key, Unset):
        json_key = UNSET
    elif key is None:
        json_key = None
    elif isinstance(key, Getv3LicensesKeyType1):
        json_key = UNSET
        if not isinstance(key, Unset):
            json_key = key.to_dict()

    else:
        json_key = key

    json_validity: Union[Dict[str, Any], None, Unset, int]
    if isinstance(validity, Unset):
        json_validity = UNSET
    elif validity is None:
        json_validity = None
    elif isinstance(validity, Getv3LicensesValidityType1):
        json_validity = UNSET
        if not isinstance(validity, Unset):
            json_validity = validity.to_dict()

    else:
        json_validity = validity

    json_allowed_activations: Union[Dict[str, Any], None, Unset, int]
    if isinstance(allowed_activations, Unset):
        json_allowed_activations = UNSET
    elif allowed_activations is None:
        json_allowed_activations = None
    elif isinstance(allowed_activations, Getv3LicensesAllowedActivationsType1):
        json_allowed_activations = UNSET
        if not isinstance(allowed_activations, Unset):
            json_allowed_activations = allowed_activations.to_dict()

    else:
        json_allowed_activations = allowed_activations

    json_allowed_deactivations: Union[Dict[str, Any], None, Unset, int]
    if isinstance(allowed_deactivations, Unset):
        json_allowed_deactivations = UNSET
    elif allowed_deactivations is None:
        json_allowed_deactivations = None
    elif isinstance(allowed_deactivations, Getv3LicensesAllowedDeactivationsType1):
        json_allowed_deactivations = UNSET
        if not isinstance(allowed_deactivations, Unset):
            json_allowed_deactivations = allowed_deactivations.to_dict()

    else:
        json_allowed_deactivations = allowed_deactivations

    json_total_activations: Union[Dict[str, Any], None, Unset, int]
    if isinstance(total_activations, Unset):
        json_total_activations = UNSET
    elif total_activations is None:
        json_total_activations = None
    elif isinstance(total_activations, Getv3LicensesTotalActivationsType1):
        json_total_activations = UNSET
        if not isinstance(total_activations, Unset):
            json_total_activations = total_activations.to_dict()

    else:
        json_total_activations = total_activations

    json_total_deactivations: Union[Dict[str, Any], None, Unset, int]
    if isinstance(total_deactivations, Unset):
        json_total_deactivations = UNSET
    elif total_deactivations is None:
        json_total_deactivations = None
    elif isinstance(total_deactivations, Getv3LicensesTotalDeactivationsType1):
        json_total_deactivations = UNSET
        if not isinstance(total_deactivations, Unset):
            json_total_deactivations = total_deactivations.to_dict()

    else:
        json_total_deactivations = total_deactivations

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

    json_tag: Union[Dict[str, Any], None, Unset, str]
    if isinstance(tag, Unset):
        json_tag = UNSET
    elif tag is None:
        json_tag = None
    elif isinstance(tag, Getv3LicensesTagType1):
        json_tag = UNSET
        if not isinstance(tag, Unset):
            json_tag = tag.to_dict()

    else:
        json_tag = tag

    json_metadatakey: Union[Dict[str, Any], None, Unset, str]
    if isinstance(metadatakey, Unset):
        json_metadatakey = UNSET
    elif metadatakey is None:
        json_metadatakey = None
    elif isinstance(metadatakey, Getv3LicensesMetadatakeyType1):
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
    elif isinstance(metadatavalue, Getv3LicensesMetadatavalueType1):
        json_metadatavalue = UNSET
        if not isinstance(metadatavalue, Unset):
            json_metadatavalue = metadatavalue.to_dict()

    else:
        json_metadatavalue = metadatavalue

    params: Dict[str, Any] = {
        "page": page,
        "limit": limit,
        "sort": sort,
        "productId": product_id,
        "productVersionId": product_version_id,
        "userId": user_id,
        "resellerId": reseller_id,
        "user.email": json_useremail,
        "user.company": json_usercompany,
        "key": json_key,
        "revoked": revoked,
        "suspended": suspended,
        "type": type,
        "validity": json_validity,
        "allowedActivations": json_allowed_activations,
        "allowedDeactivations": json_allowed_deactivations,
        "totalActivations": json_total_activations,
        "totalDeactivations": json_total_deactivations,
        "allowVmActivation": allow_vm_activation,
        "userLocked": user_locked,
        "expired": expired,
        "expirationStrategy": expiration_strategy,
        "createdAt": json_created_at,
        "tag": json_tag,
        "metadata.key": json_metadatakey,
        "metadata.value": json_metadatavalue,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, List[LicenseDto]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = LicenseDto.from_dict(response_200_item_data)

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


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, List[LicenseDto]]]:
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
    product_version_id: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    reseller_id: Union[Unset, None, str] = UNSET,
    useremail: Union[Getv3LicensesUseremailType1, None, Unset, str] = UNSET,
    usercompany: Union[Getv3LicensesUsercompanyType1, None, Unset, str] = UNSET,
    key: Union[Getv3LicensesKeyType1, None, Unset, str] = UNSET,
    revoked: Union[Unset, None, bool] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    validity: Union[Getv3LicensesValidityType1, None, Unset, int] = UNSET,
    allowed_activations: Union[Getv3LicensesAllowedActivationsType1, None, Unset, int] = UNSET,
    allowed_deactivations: Union[Getv3LicensesAllowedDeactivationsType1, None, Unset, int] = UNSET,
    total_activations: Union[Getv3LicensesTotalActivationsType1, None, Unset, int] = UNSET,
    total_deactivations: Union[Getv3LicensesTotalDeactivationsType1, None, Unset, int] = UNSET,
    allow_vm_activation: Union[Unset, None, bool] = UNSET,
    user_locked: Union[Unset, None, bool] = UNSET,
    expired: Union[Unset, None, bool] = UNSET,
    expiration_strategy: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3LicensesCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    tag: Union[Getv3LicensesTagType1, None, Unset, str] = UNSET,
    metadatakey: Union[Getv3LicensesMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3LicensesMetadatavalueType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[LicenseDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        product_version_id=product_version_id,
        user_id=user_id,
        reseller_id=reseller_id,
        useremail=useremail,
        usercompany=usercompany,
        key=key,
        revoked=revoked,
        suspended=suspended,
        type=type,
        validity=validity,
        allowed_activations=allowed_activations,
        allowed_deactivations=allowed_deactivations,
        total_activations=total_activations,
        total_deactivations=total_deactivations,
        allow_vm_activation=allow_vm_activation,
        user_locked=user_locked,
        expired=expired,
        expiration_strategy=expiration_strategy,
        created_at=created_at,
        tag=tag,
        metadatakey=metadatakey,
        metadatavalue=metadatavalue,
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
    product_version_id: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    reseller_id: Union[Unset, None, str] = UNSET,
    useremail: Union[Getv3LicensesUseremailType1, None, Unset, str] = UNSET,
    usercompany: Union[Getv3LicensesUsercompanyType1, None, Unset, str] = UNSET,
    key: Union[Getv3LicensesKeyType1, None, Unset, str] = UNSET,
    revoked: Union[Unset, None, bool] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    validity: Union[Getv3LicensesValidityType1, None, Unset, int] = UNSET,
    allowed_activations: Union[Getv3LicensesAllowedActivationsType1, None, Unset, int] = UNSET,
    allowed_deactivations: Union[Getv3LicensesAllowedDeactivationsType1, None, Unset, int] = UNSET,
    total_activations: Union[Getv3LicensesTotalActivationsType1, None, Unset, int] = UNSET,
    total_deactivations: Union[Getv3LicensesTotalDeactivationsType1, None, Unset, int] = UNSET,
    allow_vm_activation: Union[Unset, None, bool] = UNSET,
    user_locked: Union[Unset, None, bool] = UNSET,
    expired: Union[Unset, None, bool] = UNSET,
    expiration_strategy: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3LicensesCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    tag: Union[Getv3LicensesTagType1, None, Unset, str] = UNSET,
    metadatakey: Union[Getv3LicensesMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3LicensesMetadatavalueType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[LicenseDto]]]:
    """Returns a list of licenses. The licenses are returned sorted by creation date in ascending order."""

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        product_version_id=product_version_id,
        user_id=user_id,
        reseller_id=reseller_id,
        useremail=useremail,
        usercompany=usercompany,
        key=key,
        revoked=revoked,
        suspended=suspended,
        type=type,
        validity=validity,
        allowed_activations=allowed_activations,
        allowed_deactivations=allowed_deactivations,
        total_activations=total_activations,
        total_deactivations=total_deactivations,
        allow_vm_activation=allow_vm_activation,
        user_locked=user_locked,
        expired=expired,
        expiration_strategy=expiration_strategy,
        created_at=created_at,
        tag=tag,
        metadatakey=metadatakey,
        metadatavalue=metadatavalue,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    sort: Union[Unset, None, str] = UNSET,
    product_id: Union[Unset, None, str] = UNSET,
    product_version_id: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    reseller_id: Union[Unset, None, str] = UNSET,
    useremail: Union[Getv3LicensesUseremailType1, None, Unset, str] = UNSET,
    usercompany: Union[Getv3LicensesUsercompanyType1, None, Unset, str] = UNSET,
    key: Union[Getv3LicensesKeyType1, None, Unset, str] = UNSET,
    revoked: Union[Unset, None, bool] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    validity: Union[Getv3LicensesValidityType1, None, Unset, int] = UNSET,
    allowed_activations: Union[Getv3LicensesAllowedActivationsType1, None, Unset, int] = UNSET,
    allowed_deactivations: Union[Getv3LicensesAllowedDeactivationsType1, None, Unset, int] = UNSET,
    total_activations: Union[Getv3LicensesTotalActivationsType1, None, Unset, int] = UNSET,
    total_deactivations: Union[Getv3LicensesTotalDeactivationsType1, None, Unset, int] = UNSET,
    allow_vm_activation: Union[Unset, None, bool] = UNSET,
    user_locked: Union[Unset, None, bool] = UNSET,
    expired: Union[Unset, None, bool] = UNSET,
    expiration_strategy: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3LicensesCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    tag: Union[Getv3LicensesTagType1, None, Unset, str] = UNSET,
    metadatakey: Union[Getv3LicensesMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3LicensesMetadatavalueType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Response[Union[HttpErrorResponseDto, List[LicenseDto]]]:
    kwargs = _get_kwargs(
        client=client,
        page=page,
        limit=limit,
        sort=sort,
        product_id=product_id,
        product_version_id=product_version_id,
        user_id=user_id,
        reseller_id=reseller_id,
        useremail=useremail,
        usercompany=usercompany,
        key=key,
        revoked=revoked,
        suspended=suspended,
        type=type,
        validity=validity,
        allowed_activations=allowed_activations,
        allowed_deactivations=allowed_deactivations,
        total_activations=total_activations,
        total_deactivations=total_deactivations,
        allow_vm_activation=allow_vm_activation,
        user_locked=user_locked,
        expired=expired,
        expiration_strategy=expiration_strategy,
        created_at=created_at,
        tag=tag,
        metadatakey=metadatakey,
        metadatavalue=metadatavalue,
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
    product_version_id: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    reseller_id: Union[Unset, None, str] = UNSET,
    useremail: Union[Getv3LicensesUseremailType1, None, Unset, str] = UNSET,
    usercompany: Union[Getv3LicensesUsercompanyType1, None, Unset, str] = UNSET,
    key: Union[Getv3LicensesKeyType1, None, Unset, str] = UNSET,
    revoked: Union[Unset, None, bool] = UNSET,
    suspended: Union[Unset, None, bool] = UNSET,
    type: Union[Unset, None, str] = UNSET,
    validity: Union[Getv3LicensesValidityType1, None, Unset, int] = UNSET,
    allowed_activations: Union[Getv3LicensesAllowedActivationsType1, None, Unset, int] = UNSET,
    allowed_deactivations: Union[Getv3LicensesAllowedDeactivationsType1, None, Unset, int] = UNSET,
    total_activations: Union[Getv3LicensesTotalActivationsType1, None, Unset, int] = UNSET,
    total_deactivations: Union[Getv3LicensesTotalDeactivationsType1, None, Unset, int] = UNSET,
    allow_vm_activation: Union[Unset, None, bool] = UNSET,
    user_locked: Union[Unset, None, bool] = UNSET,
    expired: Union[Unset, None, bool] = UNSET,
    expiration_strategy: Union[Unset, None, str] = UNSET,
    created_at: Union[Getv3LicensesCreatedAtType1, None, Unset, datetime.datetime] = UNSET,
    tag: Union[Getv3LicensesTagType1, None, Unset, str] = UNSET,
    metadatakey: Union[Getv3LicensesMetadatakeyType1, None, Unset, str] = UNSET,
    metadatavalue: Union[Getv3LicensesMetadatavalueType1, None, Unset, str] = UNSET,
    query: Union[Unset, None, str] = UNSET,
) -> Optional[Union[HttpErrorResponseDto, List[LicenseDto]]]:
    """Returns a list of licenses. The licenses are returned sorted by creation date in ascending order."""

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            sort=sort,
            product_id=product_id,
            product_version_id=product_version_id,
            user_id=user_id,
            reseller_id=reseller_id,
            useremail=useremail,
            usercompany=usercompany,
            key=key,
            revoked=revoked,
            suspended=suspended,
            type=type,
            validity=validity,
            allowed_activations=allowed_activations,
            allowed_deactivations=allowed_deactivations,
            total_activations=total_activations,
            total_deactivations=total_deactivations,
            allow_vm_activation=allow_vm_activation,
            user_locked=user_locked,
            expired=expired,
            expiration_strategy=expiration_strategy,
            created_at=created_at,
            tag=tag,
            metadatakey=metadatakey,
            metadatavalue=metadatavalue,
            query=query,
        )
    ).parsed
