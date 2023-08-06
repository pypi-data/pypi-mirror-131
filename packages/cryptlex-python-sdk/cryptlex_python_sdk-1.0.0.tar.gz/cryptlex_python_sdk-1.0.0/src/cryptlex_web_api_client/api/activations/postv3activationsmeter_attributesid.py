from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.activation_meter_attribute_increment_response_dto import ActivationMeterAttributeIncrementResponseDto
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.postv_3_activationsmeter_attributesid_json_body import Postv3ActivationsmeterAttributesidJsonBody
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: Postv3ActivationsmeterAttributesidJsonBody,
) -> Dict[str, Any]:
    url = "{}/v3/activations/meter-attributes/{id}".format(client.base_url, id=id)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ActivationMeterAttributeIncrementResponseDto, HttpErrorResponseDto]]:
    if response.status_code == 200:
        response_200 = ActivationMeterAttributeIncrementResponseDto.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = HttpErrorResponseDto.from_dict(response.json())

        return response_404
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


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ActivationMeterAttributeIncrementResponseDto, HttpErrorResponseDto]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    json_body: Postv3ActivationsmeterAttributesidJsonBody,
) -> Response[Union[ActivationMeterAttributeIncrementResponseDto, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    id: str,
    *,
    client: Client,
    json_body: Postv3ActivationsmeterAttributesidJsonBody,
) -> Optional[Union[ActivationMeterAttributeIncrementResponseDto, HttpErrorResponseDto]]:
    """Increments the activation meter attribute uses."""

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: Postv3ActivationsmeterAttributesidJsonBody,
) -> Response[Union[ActivationMeterAttributeIncrementResponseDto, HttpErrorResponseDto]]:
    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: Postv3ActivationsmeterAttributesidJsonBody,
) -> Optional[Union[ActivationMeterAttributeIncrementResponseDto, HttpErrorResponseDto]]:
    """Increments the activation meter attribute uses."""

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
