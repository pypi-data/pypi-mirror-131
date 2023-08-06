"""Declares :class:`Client`."""
import abc
import contextlib

from unimatrix.conf import settings
from unimatrix.ext.model import CanonicalException
from unimatrix.lib.datastructures import ImmutableDTO

from .credentials.icredentials import ICredentials


class Client(metaclass=abc.ABCMeta):
    audience: str = abc.abstractproperty()
    scope: set = abc.abstractproperty()

    def __init__(self, credentials: ICredentials):
        self.credentials = credentials

    async def request(self, fn, *args, **kwargs):
        deserialize = kwargs.pop('deserialize', True)
        kwargs.setdefault('ssl', settings.ENABLE_SSL)
        response = await fn(*args, **kwargs)
        if 'X-Canonical-Exception' in response.headers:
            exception = CanonicalException(**await response.json())
            exception.http_status_code = response.status_code
            raise exception
        response.raise_for_status()
        if deserialize:
            response = ImmutableDTO.fromdict(await response.json())
        return response

    async def get(self, *args, **kwargs):
        return await self.request(self.session.get, *args, **kwargs)

    async def patch(self, *args, **kwargs):
        return await self.request(self.session.patch, *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self.request(self.session.post, *args, **kwargs)

    async def put(self, *args, **kwargs):
        return await self.request(self.session.put, *args, **kwargs)

    async def __aenter__(self):
        self.session = await self.credentials.apply(self.audience, self.scope)
        await self.session.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.__aexit__(*args, **kwargs)
        self.session = None
