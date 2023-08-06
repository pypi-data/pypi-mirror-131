"""Declares :class:`IRequest`."""
from unimatrix.lib import timezone


class IRequest:
    """Represents the request context when determining the granted
    permissions to a subject.
    """

    @property
    def timestamp(self) -> int:
        """Return the timestamp of the request."""
        return timezone.now()
