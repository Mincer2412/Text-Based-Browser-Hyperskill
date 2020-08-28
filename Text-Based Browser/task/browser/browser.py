# -*- coding: utf-8 -*-
import os
import sys
import requests
from bs4 import BeautifulSoup
from _collections import deque
from colorama import Fore

https_start = 'https://'

created_files = []
appropriate_tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li']

my_stack = deque()

# TODO
# Стоит переработать логику, так чтобы страница записывалась в файл и уже оттуда читалась. Хотя сейчас вроде так уже и работает


# ---------- Functions block ----------

def transform_url_to_filename(dirty_filename):
    result = dirty_filename

    if '.' in dirty_filename:
        result = ('.'.join(dirty_filename.split('.')[:-1]))  # отрбрасывает всё после последней точки

    result = result.split(https_start)[1]

    return result


def print_page_from_folder(subdir_name):
    with open(dir_name + '/' + subdir_name) as file:
        for line in file:
            print(line.strip())


def create_folder_with_file(_filename, request):
    with open(dir_name + '/' + _filename, 'w') as file:
        write_clear_page(request.content, file)
        file.close()


def write_to_file_and_print(_filename, _request):
    created_files.append(_filename)
    create_folder_with_file(_filename, _request)
    my_stack.append(_filename)
    print_page_from_folder(_filename)


def write_clear_page(content, _file):
    soup = BeautifulSoup(content, 'html.parser')
    all_tags = soup.find_all(appropriate_tags)
    #   tag.name
    # result = [el.text.replace('\n', '') for el in all_tags]
    result = [Fore.BLUE + el.text.replace('\n', '') if el.name == "a" else  Fore.BLACK + el.text.replace('\n', '') for el in all_tags]
    _file.write('\n'.join(result))


# ---------- End of Functions block ----------


# Читает аргумент командной строки с директорией для хранения страниц
dir_name = sys.argv[1]

# Если директория, указанная выше, не сущетсвует, то создаёт её
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

url = ''
while True:
    url = input()

    if url == 'exit':
        break

    if url == 'back':
        if len(my_stack) == 0:
            continue

        my_stack.pop()  # <- pop one element to skip current page
        print_page_from_folder(my_stack.pop())
        continue

    if 'https://' not in url:
        url = https_start + url

    if '.' not in url:
        url = transform_url_to_filename(url)
        if url in created_files:
            print_page_from_folder(url)
            continue
        else:
            print('Error: Incorrect URL')
            continue

    request = requests.get(url)

    # Запись в файл
    filename = transform_url_to_filename(url)
    write_to_file_and_print(filename, request)
    my_stack.append(filename)
