import asyncio
import csv
import sys

import aiohttp
import settings

# path_to_csv = 'C:\\Users\\ussre\\Documents\\ChromePasswords.csv'
# path_to_new_csv = "D:\\Documents\\new_ChromePasswords.csv"


def csv_list(path_to_csv):
    with open(path_to_csv) as csvfile:
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


async def check(url, session, length, exm, bad_sites):


    session: aiohttp.ClientSession
    try:
        async with session.get(url, timeout=180) as response:
            status_code = str(response.status)

            # print(url + ' ' + status_code)
            if status_code.startswith('5') | int(status_code) == 404:
                append_dict(bad_sites, status_code, url)

            return status_code
    except:
        exc_msg = str(sys.exc_info()[0])
        # print(url + ' ' + exc_msg)
        append_dict(bad_sites, exc_msg, url)

    return bad_sites


async def multiprocessing_func(url_list, exm, bad_sites, length):
    global counter
    counter = 0

    tasks = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        for i in url_list:
            tasks.append(asyncio.create_task(check(i, session, length, exm, bad_sites)))
            # tasks.append(asyncio.create_task(check(i, session, len(url_list))))
            counter += 1
            exm.text_browser.append(f'{counter} of {length} sites answered')
            print(f'{counter} of {length} sites answered')

        return await asyncio.gather(*tasks)


def get_list_of_check_sites(bad_sites):
    bad_urls_list = list()
    list_to_check = dict()
    i = 1
    for err, urls in bad_sites.items():
        if err not in settings.critical_errs:
            for url in urls:
                if url not in list_to_check.items():
                    list_to_check[i] = url
        else:
            for url in urls:
                if url not in bad_urls_list:
                    bad_urls_list.append(url)
    return list_to_check


def remove_invalid_sites(exm, path_to_csv):


    list_of_check_sites = get_list_of_check_sites()

    if len(list_of_check_sites.values()) != 0:
        print('Check the following web-sites manually and input not working ones by their indexes:')
        exm.text_browser.append('Check the following web-sites manually and input not working ones by their indexes:')

    print()

    for index_of_site, site_url in list_of_check_sites.items():
        print(f'{index_of_site}. {site_url}')
        exm.text_browser.append(f'{index_of_site}. <a href=\'{site_url}\'>{site_url}</a>')
        # exm.text_browser.append(f"<a href='{site_url}'>{site_url}</a>")


    def remove_indexes():
        def check_int(s):
            if s[0] in ('-', '+'):
                return s[1:].isdigit()
            return s.isdigit()

        for index_of_site, site_url in list_of_check_sites.items():
            print(f'{index_of_site}. {site_url}')
            exm.text_browser.append(f'{index_of_site}. {site_url}')


        print('Input indexes (empty str to exit): ')
        i = 0
        while i < len(list_of_check_sites.keys()):
            try:
                input_num = input()
                if not check_int(input_num):
                    print('Wrong index')
                    i = 0
                elif int(input_num) > len(list_of_check_sites):
                    print('Wrong index')
                    i = 0
                else:
                    print(input_num)
                    del list_of_check_sites[int(input_num)]
                    i += 1
            except (EOFError, IndexError):
                break

        return list_of_check_sites

    # remove_indexes()

    # for url in list_of_check_sites.values():
    #     bad_urls_list.append(url)
    #
    # with open(path_to_csv, 'r') as input_csv_file:
    #     csv_into_list = []
    #     reader = csv.reader(input_csv_file)
    #     for row in reader:
    #         csv_into_list.append(row)
    #
    # with open(path_to_new_csv, 'w', newline='',
    #           encoding='utf-8') as output_csv_file:
    #     writer = csv.writer(output_csv_file)
    #     for rows in csv_into_list:
    #         if rows[1] not in bad_urls_list:
    #             writer.writerow(rows)
    exm.text_browser.append('Done')




# start_time = time.time()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(multiprocessing_func(csv_list()))
# remove_invalid_sites()

# print(f'--- {round((time.time() - start_time) / 60, 2)} minutes ---')

