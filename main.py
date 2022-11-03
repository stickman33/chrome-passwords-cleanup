import asyncio
import csv
import sys

import aiohttp


def csv_dict():
    with open('C:\\Users\\ussre\\Documents\\ChromePasswords.csv') as csvfile:
        pwd_list = []

        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            pwd_list.append(row['url'])
        return pwd_list


async def check(url, session):
    session: aiohttp.ClientSession
    try:
        async with session.get(url) as response:
            if str(response.status).startswith('5'):
                with open('bad_sites.txt', 'a+') as file:
                    file.write(f'Web site {url} does not exists. Returned response code: {response.status}\n')
            else:
                print(f'Website {url} exists. Returned response code: {response.status}')
            return response.status
    except:
        with open('bad_sites.txt', 'a+') as file:
            file.write(f'Web site {url} does not exists. {str(sys.exc_info()[0])}\n')


async def multiprocessing_func(url_list):
    tasks = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        for i in url_list:
            tasks.append(asyncio.create_task(check(i, session)))
        return await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(multiprocessing_func(csv_dict()))
