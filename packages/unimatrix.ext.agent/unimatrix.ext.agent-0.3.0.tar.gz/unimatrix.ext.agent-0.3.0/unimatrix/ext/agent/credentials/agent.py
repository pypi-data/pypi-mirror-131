"""Declares :class:`AgentCredentials`."""
import asyncio
import os
import time
import urllib.parse

import aiohttp
from unimatrix.conf import settings
from unimatrix.ext import jose

from ..signer import ServiceIdentitySigner
from ..tokenexchangeservice import TokenExchangeService
from .accesstoken import AccessToken
from .icredentials import ICredentials


class AgentCredentials(ICredentials):
    """Use the credentials of the current system agent running
    the code.
    """
    __module__ = 'unimatrix.ext.agent.credentials'

    #: Maps audiences to access token to allow token reuse.
    _audiences: dict = {}

    #: The scope that these credentials will request by default.
    scope: set = {"cloud-platform"}

    def __init__(self, issuer: str = None):
        self.issuer = issuer or os.getenv('OAUTH2_ISSUER')
        if self.issuer is None:
            raise ValueError("The `issuer` parameter can not be None.")
        self.signer = ServiceIdentitySigner()
        self._lock = asyncio.Lock()
        self._audiences = AgentCredentials._audiences
        self._sts = TokenExchangeService(settings.OAUTH2_TOKEN_EXCHANGE_URL)

    def get_scope(self) -> str:
        """Return the scope to request for access tokens."""
        return str.join(' ', sorted(self.scope))

    async def apply(self, audience: str, scope: str):
        """Instantiate a session configured to access the service."""
        token = await self.get_access_token(audience, scope)
        return aiohttp.ClientSession(
            base_url=audience,
            headers={
                'Authorization': f'Bearer {token}',
                'Accept': "application/json"
            }
        )

    async def exchange(self, audience: str, scope: set) -> AccessToken:
        """Create a self-signed token and invoke the Security Token Service
        (STS) to exchange it with an access token for the given `audience`.
        """
        token = await self._sts.exchange(
            audience=audience,
            scope=str.join(' ', sorted(scope)),
            token=await self.get_agent_token(audience)
        )
        return AccessToken(self, audience, token)

    async def get_access_token(self, audience: str, scope: set) -> str:
        """Return an access token for the given `audience`."""
        async with self._lock:
            if audience in self._audiences:
                token = self._audiences.get(audience)
            else:
                self._audiences[audience] = token = await self.exchange(
                    audience=audience,
                    scope=scope
                )
        return str(token)

    async def get_agent_token(self, audience: str) -> str:
        """Return a string containing the token that the agent uses to
        identify itself.
        """
        aud = self._sts.audience or audience
        return await self.signer.sign([aud],
            ttl=60,
            sub=self.issuer,
            iss=self.issuer,
            scope=self.get_scope()
        )
