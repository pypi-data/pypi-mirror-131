from __future__ import annotations

import asyncio
import socket
from typing import Any, Mapping, Optional

import aiohttp
import async_timeout

from aioherepy.here_error import (
    HEREError,
    HEREInvalidRequestError,
    HERETimeOutError,
    HEREUnauthorizedError,
)


class AioHEREApi:
    """Main class for handling connections with HERE APIs."""

    def __init__(
        self,
        api_key: str,
        request_timeout: int = 10,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initializes connection. Creates an AioHEREApi object to communicate to the HERE APIs.
        Args:
          api_key (str):
            HERE API key.
          request_timeout (int):
            Max timeout to wait for a response from the API.
          session (Optional[aiohttp.ClientSession]):
            aiohttp client session.
        """

        self.api_key = api_key
        self.request_timeout = request_timeout
        self.api_url = "https://weather.cc.api.here.com/weather/1.0/report.json"
        self._session = session
        self._close_session = False

    def __read_error_from_response(json_data: Mapping[str, Any]) -> HEREError:
        """Return the correct error type."""

        if "error" in json_data:
            if json_data["error"] == "Unauthorized":
                return HEREUnauthorizedError(json_data["error_description"])
        error_type = json_data.get("Type")
        error_message = json_data.get("Message")
        if error_type == "Invalid Request":
            return HEREInvalidRequestError(error_message)
        return HEREError(error_message)

    async def request(
        self,
        method: str = "GET",
        data: Optional[Any] | None = None,
        json_data: Optional[dict] | None = None,
        params: Optional[Mapping[str, str]] | None = None,
    ) -> Any:
        """Makes a request to given HERE API with provided parameters.
        Args:
          method (str):
            HTTP method to use for the request e.g. GET, POST.
          data (Optional[Any]):
            RAW HTTP request data to send with the request.
          json_data (Optional[dict]):
            Dictionary of data to send as JSON with the request.
          params (Optional[Mapping[str, str]]):
            Mapping of request parameters to send with the request.
        Returns:
            The response from the API.
        Raises:
            HEREError.
        """

        headers = {
            "Accept": "application/json",
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    self.api_url,
                    data=data,
                    json=json_data,
                    params=params,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise HERETimeOutError(
                "Timeout occurred while connecting to the here API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise HEREError(
                "Error occurred while communicating with the here API."
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise self.__read_error_from_response(await response.json())
            raise HEREError(response.status, {"message": contents.decode("utf8")})

        if response.status == 204:
            response.close()
            return None

        if "application/json" in content_type:
            return await response.json()
