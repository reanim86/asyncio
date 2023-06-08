import aiohttp
import asyncio
from pprint import pprint
from more_itertools import chunked

from models import Base, Session, SwapiPeople, engine


async def get_people(id):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        response = await client.get(f'https://swapi.dev/api/people/{id}')
        json_data = await response.json()
        return json_data

async def get_number_person():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        response = await client.get('https://swapi.dev/api/people/')
        json_data = await response.json()
        return json_data['count']

async def paste_to_db(people_list):
    async with Session() as session:
        for people in people_list:
            if 'detail' in people:
                print(f'id {people} unknow')
            else:
                new_people = SwapiPeople(
                    name=people['name'],
                    birth_year=people['birth_year'],
                    eye_color=people['eye_color'],
                    gender=people['gender'],
                    hair_color=people['hair_color'],
                    height=people['height'],
                    homeworld=people['homeworld'],
                    mass=people['mass'],
                    skin_color=people['skin_color']
                )
                session.add(new_people)
                await session.commit()
        return

async def main():

    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    number_persons = await get_number_person()
    for i in chunked(range(1, (number_persons + 1)), 10):
    # for i in chunked(range(1, 2), 10):
        person_coros = []
        for id in i:
            person_coro = get_people(id)
            person_coros.append(person_coro)
        result = await asyncio.gather(*person_coros)
        # pprint(result)
        await paste_to_db(result)
    return

if __name__ == '__main__':
    asyncio.run(main())
