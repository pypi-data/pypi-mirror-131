"""Declares :class:`AccessToken`."""
from .iaccesstoken import IAccessToken
from .icredentials import ICredentials


class AccessToken:

    def __init__(self, credentials: ICredentials, audience: str, token: str):
        self.credentials = credentials
        self.audience = audience
        self.value = token

    async def refresh(self):
        self.value = str(await self.credentials.exchange(self.audience))


    def __str__(self) -> str:
        return self.value
