import asyncio

from unimatrix.ext.client.signer import DebugTokenSigner


async def main():
    signer = DebugTokenSigner('https://127.0.0.1:8001',
        kid='actor-signing', algorithm='RSAPKCS1v15SHA256'
    )
    print( await signer.sign(['foo.com'], foo='bar'))


if __name__ == '__main__':
    asyncio.run(main())
