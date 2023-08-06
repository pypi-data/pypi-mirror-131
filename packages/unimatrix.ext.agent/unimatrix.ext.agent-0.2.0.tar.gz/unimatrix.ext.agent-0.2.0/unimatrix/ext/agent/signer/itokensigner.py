"""Declares :class:`ITokenSigner`."""
import abc
import time
import typing


class ITokenSigner(metaclass=abc.ABCMeta):
    """Specifies the interface for all token signer implementations."""
    default_ttl: int = 300
    default_timeout: int = 10

    def get_default_audience(self) -> typing.Union[typing.List[str], str]:
        """Return the default audience for tokens signed by this
        signer.
        """
        return None

    def get_default_issuer(self) -> str:
        """Return the default issuer for tokens signed by this
        signer.
        """
        return None

    def get_iat(self, now: int) -> int:
        """Return an integer representing the date and time at which
        the token was issued.
        """
        return now or int(time.time())

    def set_defaults(self, claims: dict, now: int, ttl: int) -> None:
        """Sets the default claims if they are not provided."""
        iat = claims.setdefault('iat', self.get_iat(now))
        claims.setdefault('nbf', iat)
        claims.setdefault('exp', iat + (ttl or self.default_ttl))
        aud = claims.setdefault('aud', self.get_default_audience())
        iss = claims.setdefault('iss', self.get_default_issuer())

    @abc.abstractmethod
    async def sign(self,
        audiences: list,
        now: int = None,
        ttl: int = None,
        **claims
    ) -> str:
        """Signs a JSON Web Token (JWT) with the given audiences
        and additional claims.
        """
        raise NotImplementedError
