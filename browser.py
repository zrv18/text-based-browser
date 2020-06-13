from sys import argv
from os import makedirs, getcwd
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init, reinit

history = []
stack = deque()
hard_links = ['bloomberg.com', 'bloomberg', 'nytimes.com', 'nytimes']


def make_dir(dir_name):
    # Create target directory & all intermediate directories if don't exists
    try:
        makedirs(dir_name)
    except FileExistsError:
        pass


def save_page(page, text):
    with open(f'{getcwd()}\\{argv[1]}\\{page[8:]}', 'w') as file:
        file.write(text)


def out_page(page):
    with open(f'{getcwd()}\\{argv[1]}\\{page[8:]}', 'r') as file:
        return file.read()


def stack_push(data):
    stack.append(data)


def stack_pop():
    if len(stack) != 0:
        out_page(stack.pop())
    else:
        pass


def get_page(url):
    response = requests.get(url)
    if response:
        save_page(url, parsing_out(response.text))
        print(parsing_out(response.text))
    else:
        print('error')


def input_correction(data):
    if data == 'bloomberg.com' or data == 'nytimes.com':
        return 'https://' + data
    elif data == 'bloomberg' or data == 'nytimes':
        return 'https://' + data + '.com'
    elif data.endswith('.org') and not data.startswith('https://'):
        return 'https://' + data
    else:
        return data


def parsing_out(raw_text):
    soup = BeautifulSoup(raw_text, 'lxml')
    tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li'])
    out_string = ''
    for tag in tags:
        if tag.name == 'a':
            out_string += (Fore.BLUE + "\n")
            out_string += (" ".join(tag.text.split()) + '\n')
            out_string += (Style.RESET_ALL + "\n")
        else:
            out_string += (" ".join(tag.text.split()) + '\n')
    return out_string

    # write your code here


init()
if len(argv) == 2:
    make_dir(argv[1])

while True:
    user_input = input()
    if user_input == "exit":
        break
    elif user_input == "back":
        stack_pop()
    elif user_input in hard_links or user_input.endswith('.org'):
        address = input_correction(user_input)
        if address in history:
            out_page(address)
            stack_push(history[-1])
            history.append(address)
        else:
            get_page(address)
            history.append(address)
    else:
        print('error')
        continue
reinit()
