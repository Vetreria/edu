from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import requests
from urllib.parse import urlparse
import os
import argparse
import sys
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())
# parser = argparse.ArgumentParser()
# parser.add_argument("url", help="ссылка для проверки")
# args = parser.parse_args()

token = os.getenv('BL_TOKEN')


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-l', '--link')
 
    return parser


def shorten_link(token, url):
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        headers={
          'Authorization': token}, json={"long_url": url, })
    return response.json()['link']


def count_clicks(bitlink):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers={'Authorization': token}, params={'units': -1, }
    )
    return response.json()['total_clicks']


def is_bitlink(test_bitlink):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{test_bitlink}',
        headers={'Authorization': token})
    return response.ok


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    url = namespace.link
    
    # url = input("Введите URL начиная с протокола(Например - https:// ):")
    
    parsed = urlparse(url)
    test_bitlink = parsed.netloc + parsed.path
    if is_bitlink(test_bitlink):
      
          try:
            bitlink = test_bitlink
            print('Всего кликов', count_clicks(bitlink))

          except requests.exceptions.HTTPError:
            exit('Ошибка подсчета кликов!')
    else:
        try:
            print('Битлинк', shorten_link(token, url))
        except requests.exceptions.HTTPError:
            exit('Ошибка создания Битлинка!')


if __name__ == '__main__':
    main()
