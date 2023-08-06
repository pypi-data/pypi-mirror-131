from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.http_error_response_dto import HttpErrorResponseDto
from ...models.trial_policy_dto import TrialPolicyDto
from ...models.trial_policy_request_model import TrialPolicyRequestModel
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: TrialPolicyRequestModel,
) -> Dict[str, Any]:
    url = "{}/v3/trial-policies/{id}".format(client.base_url, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HttpErrorResponseDto, TrialPolicyDto]]:
    if response.status_code == 200:
        response_200 = TrialPolicyDto.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = HttpErrorResponseDto.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = HttpErrorResponseDto.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = HttpErrorResponseDto.from_dict(response.json())

        return response_404
    if response.status_code == 400:
        response_400 = HttpErrorResponseDto.from_dict(response.json())

        return response_400
    if response.status_code == 429:
        response_429 = HttpErrorResponseDto.from_dict(response.json())

        return response_429
    if response.status_code == 500:
        response_500 = HttpErrorResponseDto.from_dict(response.json())

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HttpErrorResponseDto, TrialPolicyDto]]:
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
    json_body: TrialPolicyRequestModel,
) -> Response[Union[HttpErrorResponseDto, TrialPolicyDto]]:
    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.patch(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    id: str,
    *,
    client: Client,
    json_body: TrialPolicyRequestModel,
) -> Optional[Union[HttpErrorResponseDto, TrialPolicyDto]]:
    """Updates the specified trial policy by setting the values of the parameters passed. Any parameters not provided will be left unchanged."""

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: TrialPolicyRequestModel,
) -> Response[Union[HttpErrorResponseDto, TrialPolicyDto]]:
    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: TrialPolicyRequestModel,
) -> Optional[Union[HttpErrorResponseDto, TrialPolicyDto]]:
    """Updates the specified trial policy by setting the values of the parameters passed. Any parameters not provided will be left unchanged."""

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
