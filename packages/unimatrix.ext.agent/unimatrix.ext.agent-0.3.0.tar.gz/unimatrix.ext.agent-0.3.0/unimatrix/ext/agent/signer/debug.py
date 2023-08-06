"""Declares :class:`DebugTokenSigner`."""
import typing

import aiohttp

from .itokensigner import ITokenSigner


class DebugTokenSigner(ITokenSigner):
    """Sign a JSON Web Token (JWT) using the debug endpoint
    exposed by a Unimatrix API.
    """

    def __init__(self, endpoint: str, kid: str = None, algorithm: str = None):
        self.issuer = endpoint
        self.endpoint = endpoint
        self.token_url = f'{endpoint}/debug/token'
        self.kid = kid
        self.algorithm = algorithm
        if self.kid and self.algorithm:
            self.token_url = f'{self.token_url}?keyid={self.kid}&alg={self.algorithm}' # pylint: disable=line-too-long

    def get_default_audience(self) -> typing.Union[typing.List[str], str]:
        """Return the default audience for tokens signed by this
        signer.
        """
        return self.endpoint

    def get_default_issuer(self) -> str:
        """Return the default issuer for tokens signed by this
        signer.
        """
        return self.endpoint

    async def sign(self,
        audiences: list,
        now: int = None,
        ttl: int = None,
        **claims
    ) -> str:
        """Signs a JSON Web Token (JWT) with the given audiences
        and additional claims.
        """
        self.set_defaults(claims, ttl=ttl, now=now)
        claims['aud'] = audiences
        timeout = aiohttp.ClientTimeout(total=self.default_timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            response = await session.post(
                self.token_url,
                json=claims,
                ssl=False
            )
            response.raise_for_status()
            return await response.text()