# pylint: skip-file
import dataclasses
from typing import Union

from unimatrix.conf import settings
from unimatrix.lib import wildcard

from ..iprincipal import IPrincipal
from .irequest import IRequest


__all__ = ['PermissionService']


class PermissionService:
    """Provides an interface to determine permissions for a request."""
    services = getattr(
        settings, 'SERVICE_PERMISSIONS', {}
    )

    async def has(self,
        request: IRequest,
        principal: IPrincipal,
        asked: Union[set, str]
    ) -> bool:
        """Return a boolean indicating if the given `asked` are granted
        to the request and principal.
        """
        if isinstance(asked, str):
            asked = {asked}

        # If there is no sub attribute or it is None, then
        # nobody was authenticated.
        if not getattr(principal, 'sub', None):
            return False

        if str.startswith(principal.sub, "https://"):
            granted = await self.get_service_permissions(
                asked=asked,
                service=principal.sub
            )
        else:
            granted = await self.get_subject_permissions(
                request,
                principal=principal,
                asked=asked
            )
        return asked == granted

    async def get_service_permissions(self,
        asked: set,
        service: str
    ) -> set:
        """Return a set of permissions that are granted to the service. If
        the service has all asked permissions, then the return value is
        equal to `asked`.
        """
        return wildcard.matches(self.services.get(service) or set(), asked)

    async def get_subject_permissions(self,
        request: IRequest,
        principal: IPrincipal,
        asked: set,
    ) -> set:
        """Return the set of permissions that are granted to the
        subject. If the subject has all asked permissions, then
        the return value is equal to `asked`.
        """
        raise NotImplementedError
