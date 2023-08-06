import asyncio

from unimatrix.ext import agent


class OAuth2Client(agent.Client):
    audience = "https://127.0.0.1:8021"
    scope = {"cloud-platform"}


async def main():
    credentials = agent.AgentCredentials("https://127.0.0.1:8020")
    async with OAuth2Client(credentials=credentials) as client:
        dto = await client.post('/sessions', json={
            'hostaddr': "1.2.3.4"
        })
        await client.patch(f'/sessions/{dto.id}',
            json={
                'patch': [
                    {'op': 'add', 'path': '/foo', 'value': 1},
                    {'op': 'add', 'path': '/baz', 'value': [2,3,4]}
                ]
            }
        )
        dto = await client.get('/sessions/2774bc68d89392f9b1d8984a10444a182451ab111eef779411a5f9f69605a517')
        print(dto)

if __name__ == '__main__':
    asyncio.run(main())
