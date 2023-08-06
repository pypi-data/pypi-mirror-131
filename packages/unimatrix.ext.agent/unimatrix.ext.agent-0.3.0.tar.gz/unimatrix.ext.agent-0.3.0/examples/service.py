import asyncio

from unimatrix.ext.client.signer import ServiceIdentitySigner


async def main():
    signer = ServiceIdentitySigner()
    print( await signer.sign(['foo.com'], foo='bar'))


if __name__ == '__main__':
    asyncio.run(main())
