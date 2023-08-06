"""Declares :class:`ServiceIdentitySigner`."""
from unimatrix.conf import settings
from unimatrix.ext import crypto
from unimatrix.ext import jose
from unimatrix.ext.crypto.algorithms.signing import SigningAlgorithm

from .itokensigner import ITokenSigner


class ServiceIdentitySigner(ITokenSigner):
    """A signer implementation that using the default signing
    key of an application, discovered from the environment.
    """

    @staticmethod
    def get_default_signing_algorithm(self):
        try:
            return [
                x for x in self.capabilities
                if isinstance(x, SigningAlgorithm)
            ][0]
        except IndexError:
            raise TypeError("Key does not support signing.")

    def __init__(self):
        self.key = crypto.fromfile(settings.OAUTH2_ACTOR_KEY, public=False)
        self.algorithm = self.get_default_signing_algorithm(self.key)
        self.signer = crypto.GenericSigner(self.algorithm, self.key)

    def get_default_issuer(self) -> str:
        """Return the default issuer for tokens signed by this
        signer.
        """
        return None

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
        return str(await jose.jwt(claims, signer=self.signer))
