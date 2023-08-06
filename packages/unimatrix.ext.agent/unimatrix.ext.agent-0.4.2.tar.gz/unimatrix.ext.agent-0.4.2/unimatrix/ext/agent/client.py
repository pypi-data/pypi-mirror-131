"""Declares :class:`Client`."""
import abc
import contextlib

import aiohttp
from unimatrix.conf import settings
from unimatrix.ext.model import CanonicalException
from unimatrix.lib.datastructures import ImmutableDTO

from .credentials.icredentials import ICredentials


class Client(metaclass=abc.ABCMeta):
    audience: str = abc.abstractproperty()
    scope: set = abc.abstractproperty()

    def __init__(self, credentials: ICredentials):
        self.credentials = credentials

    async def fromjson(self, response: aiohttp.ClientResponse) -> ImmutableDTO:
        """Await the response body and deserialize it."""
        return ImmutableDTO.fromdict(await response.json())

    async def request(self, fn, *args, **kwargs):
        retry = kwargs.pop('retry', False)
        deserialize = kwargs.pop('deserialize', True)
        kwargs.setdefault('ssl', settings.ENABLE_SSL)
        response = await fn(*args, **kwargs)
        if 'X-Canonical-Exception' in response.headers:
            dto = await self.fromjson(response)
            if retry or dto.code != 'CREDENTIAL_EXPIRED':
                exception = CanonicalException(**dto)
                exception.http_status_code = response.status
                raise exception

            # If the code is CREDENTIAL_EXPIRED, then refresh the
            # access token and retry the request.
            kwargs['retry'] = True
            await self.refresh_credentials()
            return await self.request(fn, *args, **kwargs)
        response.raise_for_status()
        if deserialize:
            response = await self.fromjson(response)
        return response

    async def get(self, *args, **kwargs):
        return await self.request(self.session.get, *args, **kwargs)

    async def patch(self, *args, **kwargs):
        return await self.request(self.session.patch, *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self.request(self.session.post, *args, **kwargs)

    async def put(self, *args, **kwargs):
        return await self.request(self.session.put, *args, **kwargs)

    async def refresh_credentials(self):
        await self.credentials.apply(
            audience=self.audience,
            scope=self.scope,
            session=self.session,
            force_refresh=True
        )

    async def __aenter__(self):
        self.session = await self.credentials.apply(self.audience, self.scope)
        await self.session.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.__aexit__(*args, **kwargs)
        self.session = None
