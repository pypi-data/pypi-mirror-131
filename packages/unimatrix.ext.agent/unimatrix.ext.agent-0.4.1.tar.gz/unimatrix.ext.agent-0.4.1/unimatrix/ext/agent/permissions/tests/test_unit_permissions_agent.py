# pylint: skip-file
import dataclasses

import pytest
from unimatrix.lib.datastructures import DTO

from .. import PermissionService


@dataclasses.dataclass
class Principal:
    sub: str


@pytest.fixture(scope='function')
def permissions():
    return PermissionService()


@pytest.fixture(scope='function')
def principal():
    return Principal(sub="https://example.com")


@pytest.mark.asyncio
async def test_service_has_permissions(permissions, principal):
    permissions.services = {
        'https://example.com': {
            "foo.*"
        }
    }
    assert await permissions.has(None, principal, {"foo.bar"})
    assert not await permissions.has(None, principal, {"bar.baz"})


@pytest.mark.asyncio
async def test_service_has_permissions_string(permissions, principal):
    permissions.services = {
        'https://example.com': {
            "foo.*"
        }
    }
    assert await permissions.has(None, principal, "foo.bar")
    assert not await permissions.has(None, principal, "bar.baz")


@pytest.mark.asyncio
async def test_service_has_permissions_subset(permissions, principal):
    permissions.services = {
        'https://example.com': {
            "foo.*",
            "taz.*",
        }
    }
    assert await permissions.has(None, principal, {"foo.bar"})
    assert not await permissions.has(None, principal, {"bar.baz"})
