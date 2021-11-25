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
    return 'Битлинк {0}'.format(response.json()['link'])


def count_clicks(token, bitlink):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers={'Authorization': token}, params={'units': -1, }
    )
    response.raise_for_status()
    return 'Всего кликов {0}'.format(str(response.json()['total_clicks']))


def is_bitlink(test_bitlink, token):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{test_bitlink}',
        headers={'Authorization': token})
    return response.ok


def run(func):
    print(func())


def main():
    dotenv.load_dotenv()
    token = os.getenv('BITLINK_TOKEN')
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    url = namespace.link
    parsed = urlparse(url)
    test_bitlink = parsed.netloc + parsed.path
    if is_bitlink(test_bitlink, token):
        try:
            run(partial(count_clicks, token, parsed.netloc + parsed.path))
        except requests.exceptions.HTTPError:
            exit('Ошибка подсчета кликов!')
    else:
        try:
            run(partial(shorten_link, token, url))
        except requests.exceptions.HTTPError:
            exit('Ошибка создания Битлинка!')


if __name__ == '__main__':
    main()
