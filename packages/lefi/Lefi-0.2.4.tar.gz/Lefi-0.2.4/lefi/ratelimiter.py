from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Optional, Union

from .errors import HTTPException

if TYPE_CHECKING:
    from .http import HTTPClient, Route

__all__ = ("Ratelimiter",)

logger = logging.getLogger(__name__)


class Ratelimiter:
    """A class which acts as a ratelimiter for the API.

    This class is used to create semaphores and handle said semaphores.
    This is used for concurrent requests.

    .. warning::

        This class is used internally and isn't meant to be used directly.
        Any modifications to this class can break request handling.

    Parameters
    ----------
    http: :class:`.HTTPClient`
        The HTTPClient to handle requests for

    route: :class:`.Route`
        The route which is being called upon by the HTTPClient

    method: :class:`str`
        The method to request with E.g `POST` and `GET`

    **kwargs: Any
        Extra options to pass to :meth:`aiohttp.ClientSession.request`

    Attributes
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop being used

    global_: :class:`asyncio.Event`
        The global ratelimit event

    http: :class:`.HTTPClient`
        The HTTPClient being used

    bucket: :class:`str`
        The :class:`.Route`'s bucket

    route: :class:`.Route`
        The route being request upon

    method: :class:`str`
        The method to request with

    kwargs: Any
        Extra options passed to :class:`.Ratelimiter`'s constructor

    return_data: Union[:class:`dict`, :class:`str`]
        The returned data after requesting is finished

    error_return: Optional[HTTPException]:
        Same as ``return_data`` except for errors
    """

    def __init__(self, http: HTTPClient, route: Route, method: str, **kwargs) -> None:
        self.loop: asyncio.AbstractEventLoop = http.loop
        self.global_: asyncio.Event = asyncio.Event()
        self.http: HTTPClient = http
        self.bucket: str = route.bucket
        self.route: Route = route
        self.method: str = method
        self.kwargs = kwargs

        self.return_data: Union[dict, str]
        self.error_return: Optional[HTTPException] = None
        self.global_.set()

    async def set_semaphore(self) -> asyncio.Semaphore:
        """Sets the semaphore for the bucket.

        Returns
        -------
        :class:`asyncio.Semaphore`
            The newly created semaphore set on the bucket
        """
        if semaphore := self.http.semaphores.get(self.bucket):
            return semaphore

        resp = await self.http.session.request(
            "HEAD",
            self.route.url,
            headers={"Authorization": f"Bot {self.http.token}"},
        )
        semaphore = asyncio.Semaphore(int(resp.headers.get("X-Ratelimit-Limit", 1)))
        self.http.semaphores[self.bucket] = semaphore

        return semaphore

    async def release(self, semaphore: asyncio.Semaphore, delay: float) -> None:
        """Releases the semaphore after a delay.

        Parameters
        ----------
        semaphore: :class:`asyncio.Semaphore`
            The semaphore to release after a delay

        delay: :class:`float`
            The time to wait in seconds before releasing
        """
        await asyncio.sleep(delay)
        semaphore.release()

    def global_ratelimit_set(self, delay: float) -> None:
        """Sets the global ratelimit.

        This is used when the handler encounters a global ratelimit.

        Parameters
        ----------
        delay: :class:`float`
            How long in seconds to wait before setting the event
        """
        self.loop.call_later(delay, self.global_.set)

    async def request(self) -> Any:
        """Makes a request to the route.

        Returns
        -------
        Any
            The returned data from the request
        """
        semaphore = self.http.semaphores.get(self.bucket, await self.set_semaphore())
        session = self.http.session

        await asyncio.gather(self.global_.wait(), semaphore.acquire(), self.route.lock.acquire())
        resp = await session.request(self.method, self.route.url, **self.kwargs)
        data = await self.http.json_or_text(resp)

        reset_after: float = float(resp.headers.get("X-Ratelimit-Reset-After", 0))
        remaining: int = int(resp.headers.get("X-Ratelimit-Remaining", 1))

        if resp.status != 429 and remaining == 0:
            logger.info(f"BUCKET DEPLETED: {self.bucket} RETRY: {reset_after}s")
            self.loop.call_later(reset_after, self.route.lock.release)
            await self.release(semaphore, reset_after)
            await self.request()

        if 300 > resp.status >= 200:
            logger.info(f"{resp.status}: {self.method} ROUTE: {self.route.url} REMAINING: {remaining}")
            return data

        if resp.status == 429:
            retry_after: float = data["retry_after"]  # type: ignore
            logger.info(f"RATELIMITED: {self.method} ROUTE: {self.route.url} RETRY: {retry_after}")
            if data.get("global", False):  # type: ignore
                self.global_.clear()

            self.global_ratelimit_set(retry_after)
            await asyncio.sleep(retry_after)
            await self.request()

        if not 300 > resp.status >= 200:
            logger.info(f"FAILED: {self.method} : ROUTE: {self.route.url} STATUS: {resp.status}")
            raise self.http.ERRORS.get(resp.status, HTTPException)(data)

    async def __aenter__(self) -> Ratelimiter:
        return self

    async def __aexit__(self, *_) -> None:
        self.http.semaphores.pop(self.bucket, None)
