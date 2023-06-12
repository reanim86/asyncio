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

async def get_name(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        response = await client.get(url=url)
        json_data = await response.json()
        return json_data['name']

async def get_title(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        response = await client.get(url=url)
        json_data = await response.json()
        return json_data['title']

async def paste_to_db(people_list):
    i = 0
    async with Session() as session:
        for people in people_list:
            if 'detail' in people:
                i += 1
            else:
                species_list = []
                starships_list = []
                vehicles_list = []
                films_list = []
                for url in people['films']:
                    films_list.append(await get_title(url))
                for url in people['vehicles']:
                    vehicles_list.append(await get_name(url))
                for url in people['starships']:
                    starships_list.append(await get_name(url))
                for url in people['species']:
                    species_list.append(await get_name(url))
                films = ", ".join(films_list)
                vehicles = ", ".join(vehicles_list)
                species = ", ".join(species_list)
                starships = ", ".join(starships_list)
                new_people = SwapiPeople(
                    films=films,
                    vehicles=vehicles,
                    starships=starships,
                    species=species,
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
        return i

async def main():
    """
    Основная функция по записи данных в БД
    """

    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    number_persons = await get_number_person()
    unknow_persons = 0
    for i in chunked(range(1, (number_persons + 1)), 10):
        person_coros = []
        for id in i:
            person_coro = get_people(id)
            person_coros.append(person_coro)
        result = await asyncio.gather(*person_coros)
        unknow_persons = unknow_persons + await paste_to_db(result)

    if unknow_persons >= 1:
        person_coros2 = []
        for id in range((number_persons + 1), (number_persons + 1 + unknow_persons)):
            person_coro2 = get_people(id)
            person_coros2.append(person_coro2)
        result2 = await asyncio.gather(*person_coros2)
        await paste_to_db(result2)
    return


if __name__ == '__main__':
    asyncio.run(main())
