"""Declares :class:`Session`."""
import aiohttp


class Session:
    """Wraps a :class:`aiohttp.ClientSession` to request new credentials
    if the token has expired.
    """

    def __init__(self, credentials, session: aiohttp.ClientSession):
        self.credentials = credentials
        self.session = session
