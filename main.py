import aiohttp
import asyncio
from pprint import pprint
from more_itertools import chunked


async def get_people(id):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        response = await client.get(f'https://swapi.dev/api/people/{id}')
        json_data = await response.json()
        return json_data

async def main():
    for i in chunked(range(1, 21), 10):
        person_coros = []
        for id in i:
            person_coro = get_people(id)
            person_coros.append(person_coro)
        result = await asyncio.gather(*person_coros)
        pprint(result)
    return

if __name__ == '__main__':
    asyncio.run(main())
