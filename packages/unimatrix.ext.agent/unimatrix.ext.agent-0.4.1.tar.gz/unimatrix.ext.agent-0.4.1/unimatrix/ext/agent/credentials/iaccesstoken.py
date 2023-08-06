"""Declares :class:`IAccessToken`."""
import abc


class IAccessToken(metaclass=abc.ABCMeta):

    async def refresh(self) -> None:
        """Refreshes the access token with the Security Token
        Service (STS).
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self._value
