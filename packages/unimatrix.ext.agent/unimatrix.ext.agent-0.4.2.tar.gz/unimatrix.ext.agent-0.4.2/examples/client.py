import asyncio

import yaml
from unimatrix.ext import agent
from unimatrix.ext.agent.signer import DebugTokenSigner


class IAMClient(agent.Client):
    endpoint: str   = "https://127.0.0.1:8001"
    scope: str      = {"unimatrixone.io/cloud-platform"}

    def __init__(self, issuer, *args, **kwargs):
        super().__init__(issuer, self.endpoint, self.scope, *args, **kwargs)

    async def get_roles(self):
        return await self.get('roles')


async def main():
    signer = DebugTokenSigner(
        "https://127.0.0.1:8000",
        kid='actor-signing', algorithm='RSAPKCS1v15SHA256'
    )
    async with IAMClient("https://127.0.0.1:8000", signer=signer) as api:
        print(yaml.safe_dump((await api.get_roles()).as_dict(), indent=2, default_flow_style=False))


if __name__ == '__main__':
    asyncio.run(main())
