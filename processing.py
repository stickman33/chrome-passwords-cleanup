import asyncio
import csv
import os
import sys

import aiohttp
import settings


# path_to_csv = 'C:\\Users\\ussre\\Documents\\ChromePasswords.csv'
# path_to_new_csv = "D:\\Documents\\new_ChromePasswords.csv"

# sem = asyncio.Semaphore(180)

def csv_list(path_to_csv):
    with open(path_to_csv, 'r', encoding='utf-8') as csvfile:
        pwd_list = []

        reader = csv.DictReader(csvfile)
        for row in reader:
            pwd_list.append(row['url'])
        return pwd_list


def append_dict(dictionary, key, value):
    if key in dictionary.keys():
        dictionary[key].append(value)
    else:
        values = [value]
        dictionary[key] = values


async def check(url, session, bad_sites, exm, length):
    global counter
    counter = 0
    session: aiohttp.ClientSession
    try:
        async with session.get(url, timeout=180) as response:
            counter += 1
            status_code = str(response.status)

            # if status_code.startswith('5') | int(status_code) == 404:
            if status_code.startswith('5'):
                append_dict(bad_sites, status_code, url)

            print(f'{counter} of {length} sites answered. {url}')
            exm.signal_accept(counter * 100 / length)
    except:
        exc_msg = str(sys.exc_info()[0])
        append_dict(bad_sites, exc_msg, url)
        counter += 1

        print(f'{counter} of {length} sites answered. {url} {exc_msg}')

    # print(f'{counter} of {length} sites answered. {url}')
    # exm.signal_accept(counter * 100/length)
    return bad_sites


async def multiprocessing_func(url_list, exm, bad_sites, length):
    # global counter
    # counter = 0
    tasks = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        for i in url_list:
            future = asyncio.ensure_future(check(i, session, bad_sites, exm, length))
            tasks.append(future)
            while future.done():
                print(future.result())

            # tasks.append(asyncio.create_task(check(i, session, bad_sites, exm, length)))

            # counter += 1
            # exm.text_browser.append(f'{counter} of {length} sites answered')
            # print(f'{counter} of {length} sites answered')

        return await asyncio.gather(*tasks)


def get_list_of_check_sites(bad_sites):
    bad_urls_list = list()
    list_to_check = list()
    # list_to_check = dict()
    # i = 1
    for err, urls in bad_sites.items():
        if err not in settings.critical_errs:
            for url in urls:
                if url not in list_to_check:
                    # list_to_check[i] = url
                    list_to_check.append(url)
        else:
            for url in urls:
                if url not in bad_urls_list:
                    bad_urls_list.append(url)
    return list_to_check, bad_urls_list


def remove_invalid_sites(bad_urls_list, path_to_csv):
    def newFilePath(file_path):
        head, tail = os.path.split(file_path)
        new_file_path = head + '/new_' + tail
        return new_file_path

    with open(path_to_csv, 'r', encoding='utf-8') as input_csv_file:
        csv_into_list = []
        reader = csv.reader(input_csv_file)
        for row in reader:
            csv_into_list.append(row)

    with open(newFilePath(path_to_csv), 'w', newline='',
              encoding='utf-8') as output_csv_file:
        writer = csv.writer(output_csv_file)
        for rows in csv_into_list:
            if rows[1] not in bad_urls_list:
                writer.writerow(rows)

# start_time = time.time()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(multiprocessing_func(csv_list()))
# remove_invalid_sites()

# print(f'--- {round((time.time() - start_time) / 60, 2)} minutes ---')
