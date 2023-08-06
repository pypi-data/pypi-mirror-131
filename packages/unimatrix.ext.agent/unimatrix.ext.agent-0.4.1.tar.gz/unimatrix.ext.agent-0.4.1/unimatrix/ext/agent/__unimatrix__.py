# pylint: skip-file
import ioc

from .permissions import PermissionService


async def on_setup(*args, **kwargs):
    if not ioc.is_satisfied('PermissionService'):
        ioc.provide('PermissionService', PermissionService())
