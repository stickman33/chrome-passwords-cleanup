import asyncio
import csv
import sys
import time

import aiohttp

import settings

path_to_csv = 'C:\\Users\\ussre\\Documents\\ChromePasswords.csv'
path_to_new_csv = 'C:\\Users\\ussre\\Documents\\new_ChromePasswords.csv'


def csv_dict():
    with open(path_to_csv) as csvfile:
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
        async with session.get(url, timeout=180) as response:
            status_code = str(response.status)
            if status_code.startswith('5'):
                append_dict(bad_sites, status_code, url)
            return status_code
    except:
        exc_msg = str(sys.exc_info()[0])
        append_dict(bad_sites, exc_msg, url)


async def multiprocessing_func(url_list):
    tasks = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        for i in url_list:
            tasks.append(asyncio.create_task(check(i, session)))

        return await asyncio.gather(*tasks)


def remove_invalid_sites():
    print('Check the following web-sites manually and input not working ones by their indexes:')
    bad_urls_list = list()

    def get_list_of_check_sites():
        list_to_check = list()
        for err, urls in bad_sites.items():
            if err not in settings.critical_errs:
                for url in urls:
                    if url not in list_to_check:
                        list_to_check.append(url)
            else:
                for url in urls:
                    if url not in bad_urls_list:
                        bad_urls_list.append(url)
        return list_to_check

    list_of_check_sites = get_list_of_check_sites()
    for site in list_of_check_sites:
        print(f'{list_of_check_sites.index(site) + 1}. {site}')
    print()

    def get_remove_indexes():
        def check_int(s):
            if s[0] in ('-', '+'):
                return s[1:].isdigit()
            return s.isdigit()

        remove_indexes = []
        print('Input indexes (empty str to exit): ')
        i = 0
        while i < len(list_of_check_sites):
            try:
                input_num = input()

                if not check_int(input_num):
                    print('Wrong index')
                    i = 0
                elif int(input_num) > len(list_of_check_sites):
                    print('Wrong index')
                    i = 0
                else:
                    remove_indexes.append(int(input_num))
                    i += 1
            except (EOFError, IndexError):
                break
        return remove_indexes

    indexes_to_remove = get_remove_indexes()
    if indexes_to_remove is not None:
        for index in indexes_to_remove:
            del(list_of_check_sites[index - 1])

    for url in list_of_check_sites:
        if indexes_to_remove is not None:
            if list_of_check_sites.index(url) in indexes_to_remove:
                bad_urls_list.append(url)
        else:
            bad_urls_list.append(url)


    with open(path_to_csv, 'r') as input_csv_file:
        csv_into_list = []
        reader = csv.reader(input_csv_file)
        for row in reader:
            csv_into_list.append(row)

    with open(path_to_new_csv, 'w', newline='',
              encoding='utf-8') as output_csv_file:
        writer = csv.writer(output_csv_file)
        for rows in csv_into_list:
            if rows[1] not in bad_urls_list:
                writer.writerow(rows)


start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(multiprocessing_func(csv_dict()))
remove_invalid_sites()

print(f'--- {round((time.time() - start_time) / 60, 2)} minutes ---')
