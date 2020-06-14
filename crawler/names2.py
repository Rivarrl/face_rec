# -*- coding: utf-8 -*-
# ======================================
# @File    : names2.py
# @Time    : 2020/6/9 17:49
# @Author  : Rivarrl
# ======================================
import requests
from bs4 import BeautifulSoup
import json


def fetch():
    url = 'https://123fans.cn/allstars.php'
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    bs = BeautifulSoup(resp.text, 'html.parser')
    slists = bs.select('#starlists .starlist')
    d = dict()
    for sl in slists:
        title = sl.select_one('h3').text
        if title in ('团体组合', '网络红人'): continue
        d[title] = set()
        stars = sl.select('a')
        for s in stars:
            print(s.text)
            d[title].add(s.text)
        d[title] = list(d[title])
    with open('./data/names2.json', 'w', encoding='utf-8') as f:
        f.write(str(d).replace("'", '"'))

def process():
    ns = set()
    with open('./data/names2.json', 'r', encoding='utf-8') as f:
        ds = f.read()
        d = json.loads(ds)
        for k, v in d.items():
            ns |= set(v)
    with open('./data/fans1.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(ns))

if __name__ == '__main__':
    fetch()
    process()