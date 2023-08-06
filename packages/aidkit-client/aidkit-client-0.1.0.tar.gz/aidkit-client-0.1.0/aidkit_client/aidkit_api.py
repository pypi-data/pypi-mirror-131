import json
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from posixpath import join as join_url  # both urls and posix paths use `/` as seperator
from types import TracebackType
from typing import Any, Dict, Optional

import httpx


@dataclass
class Request:
    headers: Optional[dict]
    path: str
    parameters: Optional[Dict[str, Any]]
    body: Optional[dict]


@dataclass
class Response:
    status_code: int
    body: dict

    @property
    def is_success(self) -> bool:
        return self.status_code in (200, 201)

    @property
    def is_not_found(self) -> bool:
        return self.status_code == 404

    @property
    def is_bad(self) -> bool:
        return self.status_code == 400


class HTTPService(ABC):
    @abstractmethod
    async def get(self, path: str, parameters: Optional[Dict[str, Any]]) -> Response:
        pass

    @abstractmethod
    async def post_json(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]],
        body: Optional[dict],
    ) -> Response:
        pass

    @abstractmethod
    async def post_multipart_data(
        self,
        path: str,
        data: Optional[dict],
        files: Optional[dict],
    ) -> Response:
        pass

    @abstractmethod
    async def patch(
        self, path: str, parameters: Optional[Dict[str, Any]], body: Optional[dict]
    ) -> Response:
        pass

    @abstractmethod
    async def delete(
        self, path: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Response:
        pass


class AidkitApi(HTTPService):
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self.auth_token}"},
            # TODO: make configurable
            # see https://neurocats.atlassian.net/browse/AK-2759
            timeout=60 * 5,
        )

    async def __aenter__(self) -> "AidkitApi":
        await self.client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        await self.client.__aexit__(
            exc_type=exc_type, exc_value=exc_value, traceback=traceback
        )

    async def get(self, path: str, parameters: Optional[Dict[str, Any]]) -> Response:
        response = await self.client.get(
            url=self._with_base_url(path), params=parameters
        )
        return self._to_aidkit_response(response)

    async def post_json(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]],
        body: Optional[Dict[str, Any]],
    ) -> Response:
        response = await self.client.post(
            url=self._with_base_url(path), params=parameters, json=body
        )
        return self._to_aidkit_response(response)

    async def post_multipart_data(
        self,
        path: str,
        data: Optional[dict],
        files: Optional[dict],
    ) -> Response:
        response = await self.client.post(
            url=self._with_base_url(path), data=data, files=files
        )
        return self._to_aidkit_response(response)

    async def patch(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]],
        body: Optional[Dict[str, Any]],
    ) -> Response:
        response = await self.client.patch(
            url=self._with_base_url(path), params=parameters, json=body
        )
        return self._to_aidkit_response(response)

    async def delete(
        self,
        path: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Response:
        response = await self.client.delete(
            url=self._with_base_url(path), params=parameters
        )
        return self._to_aidkit_response(response)

    def _with_base_url(self, path: str) -> str:
        return join_url(self.base_url, path)

    @classmethod
    def _to_aidkit_response(cls, res: httpx.Response) -> Response:
        try:
            return Response(status_code=res.status_code, body=res.json())
        except json.decoder.JSONDecodeError:
            return Response(
                status_code=res.status_code, body={"not_json_decodable": res.content}
            )
