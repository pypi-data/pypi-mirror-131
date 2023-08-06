"""Declares :class:`ICredentials`."""


class ICredentials:
    """Specifies the interface of credentials implementations."""

    def is_available(self) -> bool:
        """Indicate if the credentials are available for the
        current runtime.
        """
        raise NotImplementedError

    def must_refresh(self) -> bool:
        """Return a boolean indicating if the credentials must refresh."""
        raise NotImplementedError

    async def refresh(self) -> None:
        """Refreshes the credentials."""
        raise NotImplementedError

    async def __await__(self):
        if self.must_refresh():
            await self.refresh()
