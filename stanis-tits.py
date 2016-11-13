#!/usr/bin/env python3

import re
import shutil
import os.path
import requests
from bs4 import BeautifulSoup

__author__ = 'Alexander Popov'
__version__ = '0.1.0'
__license__ = 'Unlicense'

dwnImageDir = './images'
cookies = dict(block='951')
siteUrl = 'http://blog.stanis.ru/?back=%d'
imgPage = 0

# create .stanis-tits.latest file and download image directory
if not os.path.exists('%s/.stanis-tits.latest' % dwnImageDir):
    if not os.path.exists('%s' % dwnImageDir):
        os.mkdir('%s' % dwnImageDir)

    with open('%s/.stanis-tits.latest' % dwnImageDir, 'w') as f:
        f.write('0')

with open('%s/.stanis-tits.latest' % dwnImageDir, 'r') as f:
    latestDwnFile = f.read()

STOP = False
NEXT_LATEST = None

while STOP is False:
    print('Loading page %d' % imgPage)

    r = requests.get(siteUrl % imgPage, cookies=cookies)
    soup = BeautifulSoup(r.text.encode('cp1251'),
                         "html.parser", from_encoding="windows-1251")
    images = soup.findAll('img', src=re.compile('img/*'))

    for image in images:
        if image['src'].split('/')[1].split('.')[0] == latestDwnFile:
            STOP = True

        if imgPage == 0:
            if NEXT_LATEST is None:
                NEXT_LATEST = str(image['src'].split('/')[1].split('.')[0])
                with open('%s/.stanis-tits.latest' % dwnImageDir, 'w+') as f:
                    f.write(NEXT_LATEST)

        if not os.path.exists('%s/%s' % (dwnImageDir,
                              image['src'].split('/')[1],)):
            print('\tDownload %s' % image['src'].split('/')[1])
            response = requests.get('http://blog.stanis.ru/%s'
                                    % image['src'], stream=True)
            with open('%s/%s' % (dwnImageDir, image['src'].split('/')[1]),
                      'wb') as out_image:
                shutil.copyfileobj(response.raw, out_image,)

    imgPage += 1
