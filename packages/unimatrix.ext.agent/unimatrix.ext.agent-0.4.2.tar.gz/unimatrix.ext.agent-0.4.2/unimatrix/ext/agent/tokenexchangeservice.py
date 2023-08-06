"""Declares :class:`TokenExchangeService`."""
import urllib.parse

import aiohttp
from unimatrix.conf import settings
from unimatrix.ext.model import CanonicalException


class TokenExchangeService:
    """Provides an interface to exchange access tokens."""
    grant_type = "urn:ietf:params:oauth:grant-type:token-exchange"
    token_type = "urn:ietf:params:oauth:token-type:access_token"

    @property
    def audience(self) -> str:
        """Return the audience that the Security Token Service (STS)
        accepts.
        """
        return self._audience

    @property
    def params(self) -> dict:
        """Return the input parameters for the Security Token
        Service (STS).
        """
        return {
            'grant_type': self.grant_type,
            'requested_token_type': self.token_type
        }

    @property
    def session(self) -> aiohttp.ClientSession:
        """Return a session configured for the external
        service.
        """
        return aiohttp.ClientSession(
            timeout=self.timeout
        )

    @property
    def timeout(self) -> aiohttp.ClientTimeout:
        """Return a :class:`aiohttp.ClientTimeout` instance
        specifying the timeout when requesting a new token.
        """
        return aiohttp.ClientTimeout(total=60)

    def __init__(self, url):
        self._url = url
        self._audience = '://'.join(urllib.parse.urlparse(url)[:2])

    async def exchange(self,
        audience: str,
        scope: str,
        token: str,
    ) -> str:
        """Invoke the Security Token Service (STS) and exchange
        the given token.
        """
        params = {
            **self.params,
            'audience': audience,
            'scope' :scope,
            'subject_token_type': "urn:ietf:params:oauth:token-type:jwt",
            'subject_token': token
        }
        async with self.session as session:
            response = await session.post(
                self._url,
                json=params,
                ssl=False
            )
            if 'x-canonical-exception' in response.headers:
                raise CanonicalException(**await response.json())
            response.raise_for_status()
            result = await response.json()
        return result['access_token']
