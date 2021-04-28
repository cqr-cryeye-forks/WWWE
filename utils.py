import argparse
import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import NoReturn

from aiohttp import ClientSession
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

default_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
}


@contextmanager
def driver():
    options = Options()
    options.headless = False
    log_path = Path('logs').joinpath('geckodriver.log')
    with webdriver.Firefox(options=options, log_path=log_path) as d:
        yield d


def print_error(e: Exception, service: str):
    name = clear_service_name(string=service)
    print(f'{name}. An error occurred!\nError: {e}\n')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='email [example@dd.com]', type=str)
    return parser.parse_args()


def set_headers(s: ClientSession, headers: dict = None) -> NoReturn:
    if headers:
        default_headers.update(headers)
    s.headers.update(default_headers)


def clear_service_name(string: str) -> str:
    return string.replace('_', '').split('.')[-1]


async def unexpected_status(resp, service: str) -> NoReturn:
    name = clear_service_name(string=service)
    time = datetime.now().__str__()  # todo reformat time
    file_path = Path('logs').joinpath('requests').joinpath(f'{name}_{time.replace(" ", "_")}.log')
    print(f'Unexpected behavior. {name.title()} returned a response with a status: {resp.status}.\n'
          f'More info in {file_path}\n')
    with open(file_path, 'w') as f:
        json.dump({
            'time': time,
            'service': name,
            'status_code': resp.status,
            'response_content': await resp.text()
        }, f, indent=2)
