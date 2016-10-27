#!/usr/bin/env python3

import sys
sys.path.append('./.pip')
import requests
from bs4 import BeautifulSoup
import re
import shutil
import os.path

__author__ = 'Alexander Popov'
__version__ = '0.0.1'
__license__ = 'Unlicense'

IMAGES_DIR = './images'
COOKIES = dict(block='951')
URL = 'http://blog.stanis.ru/?back=%d'
PAGE = 0
with open('%s/.stanis-tits.latest' % IMAGES_DIR, 'r') as f:
    LATEST_FILE = f.read()
STOP = False
NEXT_LATEST = None

while STOP == False:
    print('Loading page %d' % PAGE)

    r = requests.get(URL % PAGE, cookies=COOKIES)
    

    soup = BeautifulSoup(r.text.encode('cp1251'),
        "html.parser", from_encoding="windows-1251")
    images = soup.findAll('img', src=re.compile('img/*'))

    for image in images:
        if image['src'].split('/')[1].split('.')[0] == LATEST_FILE:
            STOP = True

        if PAGE == 0:
            if NEXT_LATEST == None:
                NEXT_LATEST = str(image['src'].split('/')[1].split('.')[0])
                with open('%s/.stanis-tits.latest' % IMAGES_DIR, 'w+') as f:
                    f.write(NEXT_LATEST)

        if not os.path.exists('%s/%s' % (IMAGES_DIR, image['src'].split('/')[1],)):
            print('\tDownload %s' % image['src'].split('/')[1])
            response = requests.get('http://blog.stanis.ru/%s' % image['src'], stream=True)
            
            with open('%s/%s' % (IMAGES_DIR, image['src'].split('/')[1]), 'wb') as out_image:
                shutil.copyfileobj(response.raw, out_image,)

    PAGE += 1

