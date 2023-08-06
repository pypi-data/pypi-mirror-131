"""Declares :class:`IPrincipal`."""
import abc


class IPrincipal(metaclass=abc.ABCMeta):
    """Specifies the interface of principal objects."""

    @abc.abstractproperty
    def sub(self) -> str:
        """Return the subject identifier of a principal."""
        raise NotImplementedError

    @abc.abstractproperty
    def asp(self) -> str:
        """Return the Authenticated Session Principal (ASP)
        that the :attr:`sub` used to authenticate, or ``None``
        if there is none.
        """
        raise NotImplementedError
