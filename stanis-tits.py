#!/usr/bin/env python3

import re
import shutil
import os.path
import requests
from bs4 import BeautifulSoup

__author__ = 'Alexander Popov'
__version__ = '1.0.0'
__license__ = 'Unlicense'

DOWNLOAD_DIR = './images'


def checkResumeFile():
    if not os.path.exists('{0}/.resume'.format(DOWNLOAD_DIR,)):
        if not os.path.exists(DOWNLOAD_DIR):
            os.mkdir(DOWNLOAD_DIR)

        with open('{0}/.resume'.format(DOWNLOAD_DIR,), 'w') as f:
            f.write('0')
            return([0])
    else:
        with open('{0}/.resume'.format(DOWNLOAD_DIR,), 'r') as f:
            lines = [line.split('\n')[0] for line in f][-20:]

            return(lines)


def saveResume(resumeList):
    resumeList.sort()
    with open('{0}/.resume'.format(DOWNLOAD_DIR,), 'w', encoding='utf-8') as f:
        for item in resumeList[-20:]:
            f.write('{0}\n'.format(item))


def getImagesLinks(page):
    URL = lambda page: 'http://blog.stanis.ru/?back={0}'.format(page,)
    COOKIES = dict(block='951')

    r = requests.get(URL(page), cookies=COOKIES)
    soup = BeautifulSoup(r.text.encode('cp1251'),
                         "html.parser", from_encoding="windows-1251")

    imagesData = soup.findAll('img', src=re.compile('img/*'))

    imagesUrl = list()

    for image in imagesData:
        imagesUrl.append(image['src'].split('/')[1])

    return(imagesUrl)


def imageDownload(image):
    response = requests.get('https://blog.stanis.ru/img/{0}'.format(image,),
                            stream=True)

    with open('{0}/{1}'.format(DOWNLOAD_DIR, image),
              'wb') as out_image:
        shutil.copyfileobj(response.raw, out_image,)


if __name__ == '__main__':
    resumeFiles = checkResumeFile()

    LOOP = True
    downloadPage = 0

    while LOOP:
        imagesLinks = getImagesLinks(downloadPage)
        imagesLinks.sort()

        for image in imagesLinks:
            if not image.split('.')[0] in resumeFiles:
                imageDownload(image)
                resumeFiles.insert(0, image.split('.')[0],)
            else:
                LOOP = False

        downloadPage += 1

    saveResume(resumeFiles)
