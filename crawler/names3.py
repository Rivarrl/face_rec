# -*- coding: utf-8 -*-
# ======================================
# @File    : names3.py
# @Time    : 2020/6/9 18:19
# @Author  : Rivarrl
# ======================================
from bs4 import BeautifulSoup
import os, shutil

f = open('./mxk.html', 'r', encoding='utf-8')
html = f.read()
bs = BeautifulSoup(html, 'html.parser')
lis = bs.select('body > div.wrapper > div.container > div.outer > div.mod-list > ul > li')
for li in lis:
    imga = li.select_one('a.avatar > img')
    namea = li.select_one('a.name')
    img_path = imga['src']
    name = namea.text
    print(img_path, name)
    shutil.copy(img_path, './image/names3/{}.jpg'.format(name))
