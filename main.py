import asyncio
import csv
import sys

import aiohttp


def csv_dict():
    with open('D:\\Documents\\ChromePasswords.csv') as csvfile:
        pwd_list = []

        reader = csv.DictReader(csvfile)
        for row in reader:
            pwd_list.append(row['url'])
        return pwd_list


bad_sites = {}


async def check(url, session):
    session: aiohttp.ClientSession

    def append_dict(dictionary, key, value):
        if key in dictionary.keys():
            dictionary[key].append(value)
        else:
            values = [value]
            dictionary[key] = values

    try:
        async with session.get(url) as response:
            status_code = str(response.status)
            if status_code.startswith('5'):
                append_dict(bad_sites, status_code, url)

                # with open('bad_sites.txt', 'a+') as file:
                #     file.write(f'Web site {url} does not exists; {response.status}\n')
            # else:
            #     print(f'Website {url} exists. Returned response code: {response.status}')
            return status_code
    except:
        exc_msg = str(sys.exc_info()[0])
        append_dict(bad_sites, exc_msg, url)

        # with open('bad_sites.txt', 'a+') as file:
        #     file.write(f'Web site {url} does not exists; {str(sys.exc_info()[0])}\n')


async def multiprocessing_func(url_list):
    tasks = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        for i in url_list:
            tasks.append(asyncio.create_task(check(i, session)))

        return await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(multiprocessing_func(csv_dict()))

with open('bad_sites.txt', 'a+') as file:
    for error, urls in bad_sites.items():
        for url in urls:
            file.write(f'Web-site: {url}. {error}\n')

lines_output = list()

with open('D:\\Documents\\ChromePasswords.csv', 'r') as input_csv_file:
    reader = csv.reader(input_csv_file)
    for row in reader:
        for item in bad_sites.values():
            if row[1] not in item:
                lines_output.append(row)


with open('D:\\Documents\\new_ChromePasswords.csv', 'w', newline='', encoding='utf-8') as output_csv_file:
    writer = csv.writer(output_csv_file)
    for line in lines_output:
        writer.writerow(line)

