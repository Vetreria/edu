import dotenv
import requests
from urllib.parse import urlparse
import os
import argparse
import sys
from functools import partial


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link')
    return parser


def shorten_link(token, url):
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers={
          'Authorization': token}, json={"long_url": url, })
    response.raise_for_status()
    return 'Битлинк ' + response.json()['link']


def count_clicks(bitlink):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers={'Authorization': token}, params={'units': -1, }
    )
    response.raise_for_status()
    return 'Всего кликов ' + str(response.json()['total_clicks'])


def is_bitlink(test_bitlink):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{test_bitlink}',
        headers={'Authorization': token})
    return response.ok


def run(func):
    print(func())


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    url = namespace.link
    parsed = urlparse(url)
    test_bitlink = parsed.netloc + parsed.path
    a1 = partial(count_clicks, parsed.netloc + parsed.path)
    m1 = partial(shorten_link, token, url)
    if is_bitlink(test_bitlink):
        try:
            run(a1)
        except requests.exceptions.HTTPError:
            exit('Ошибка подсчета кликов!')
    else:
        try:
            run(m1)
        except requests.exceptions.HTTPError:
            exit('Ошибка создания Битлинка!')


if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('BITLINK_TOKEN')
    main()
