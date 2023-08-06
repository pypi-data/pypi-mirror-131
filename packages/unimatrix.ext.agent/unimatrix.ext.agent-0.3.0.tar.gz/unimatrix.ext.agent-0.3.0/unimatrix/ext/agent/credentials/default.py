# pylint: disable=line-too-long
"""Declares :class:`DefaultCredentials`."""
import contextlib
import logging
import os
import sys

import aiohttp
from unimatrix.conf import settings
from unimatrix.ext.crypto import Signer
from unimatrix.ext.model import CanonicalException
from ..signer import ITokenSigner
from ..signer import ServiceIdentitySigner


class DefaultCredentials:
    """The default implementation for credentials. Discovers credentials
    based on environment variables and other system configuration.
    """
    logger: logging.Logger = logging.getLogger('uvicorn')

    exchange_url: str = settings.OAUTH2_TOKEN_EXCHANGE_URL\
        or "https://sts.unimatrixapis.com/token/exchange"

    def __init__(self,
        issuer: str = None,
        signer: ITokenSigner = None,
        logger: logging.Logger = None,
        token: str = None,
        verify_ssl: bool = True
    ):
        """Initialize a new :class:`BaseCredentials` instance."""
        self.issuer = issuer
        self.signer = signer or ServiceIdentitySigner()
        self.logger = logger or self.logger
        self.verify_ssl = verify_ssl

    async def exchange(self, issuer: str, audience: str, sub: str, scope: set) -> str:
        """Contact the OAuth 2.0 Token Exchange service and receive
        a signed token for the specified audience.
        """
        timeout = aiohttp.ClientTimeout(total=30)
        token = await self.signer.sign(
            audience,
            iss=issuer,
            sub=sub,
            ttl=600
        )
        async with aiohttp.ClientSession(timeout=timeout) as session:
            response = await session.post(
                self.exchange_url,
                json={
                    'grant_type': "urn:ietf:params:oauth:grant-type:token-exchange",
                    'audience': audience,
                    'scope': str.join(' ', list(sorted(set(scope)))),
                    'requested_token_type': "urn:ietf:params:oauth:token-type:access_token",
                    'subject_token_type': "urn:ietf:params:oauth:token-type:jwt",
                    'subject_token': token
                },
                ssl=self.verify_ssl
            )
            if response.status != 200:
                if 'X-Canonical-Exception' in response.headers:
                    raise CanonicalException(**await response.json())
                response.raise_for_status()
            dto = await response.json()
        return dto['access_token']

    async def apply(self,
        issuer: str,
        endpoint: str,
        scope: str,
        token: str = None
    ):
        """Create an :class:`aiohttp.ClientSession` configured for the given
        endpoint.
        """
        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers = {
                'Authorization': 'Bearer ' + await self.exchange(
                    issuer=issuer,
                    audience=endpoint,
                    sub=issuer,
                    scope=scope
                ),
                'Accept': "application/json",
                'User-Agent': issuer
            }
        )

    @contextlib.asynccontextmanager
    async def consume(self, issuer: str, service_endpoint: str, scope: set):
        """Create a context with the current service as the consumer i.e.
        the subject of a request.
        """
        timeout = aiohttp.ClientTimeout(total=30)
        token = await self.exchange(
            issuer=issuer,
            audience=service_endpoint,
            sub=issuer,
            scope=scope
        )
        headers = {
            'Authorization': f"Bearer {token}",
            'Accept': "application/json",
            'User-Agent': issuer
        }
        try:
            session = aiohttp.ClientSession(headers=headers, timeout=timeout)
            await session.__aenter__()
            yield session
        finally:
            await session.__aexit__(*sys.exc_info())
