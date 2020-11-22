#!/usr/bin/python3

import os
import sys

import bs4
import requests

YOUTUBE_URL_FORMAT = 'https://www.youtube.com/watch?v={}'
LINKS_FILE_PATH = 'videos.txt'


def get_video_links(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    num_pages = int(soup.find('div', {'class': 'pagenav'}).td.text.split()[-1])

    links = []

    for i in range(1, num_pages + 1):
        r = requests.get(url, params={'page': i})

        for line in r.text.split('\n'):
            if 'verVideo(\'' in line:
                video_id = line.split('\'')[1]
                link = YOUTUBE_URL_FORMAT.format(video_id)

                if link not in links:
                    links.append(link)

    return links


def save_to_file(links):
    with open(LINKS_FILE_PATH, 'wt') as f:
        for link in links:
            f.write(link + '\n')


def download(links):
    for link in links:
        os.system('youtube-dl {}'.format(link))


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input('Pega la URL del hilo y pulsa INTRO: ')

    print('Obteniendo lista de enlaces...')
    links = get_video_links(url)
    save_to_file(links)
    print('Lista de enlaces generada en {}'.format(LINKS_FILE_PATH))
    print('Descargando videos...')
    download(links)
    print('Hecho')


if __name__ == '__main__':
    main()
