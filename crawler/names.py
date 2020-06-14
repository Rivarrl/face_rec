# -*- coding: utf-8 -*-
# ======================================
# @File    : names.py
# @Time    : 2020/1/15 13:08
# @Author  : Rivarrl
# ======================================
import requests
from bs4 import BeautifulSoup
import re
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

def mkd(path):
    if not os.path.exists(path):
        os.mkdir(path)

def fetch_movie_stars():
    # 影视明星名字网站
    url = "http://www.manmankan.com/dy2013/mingxing/yanyuan/"
    resp = requests.get(url, headers)
    resp.encoding = resp.apparent_encoding
    xf = BeautifulSoup(resp.text, 'html.parser')
    actor_names = xf.find_all(class_='i_cont_s')
    col_names = ['中国大陆', '中国香港', '中国台湾', '日本', '韩国', '欧美']
    actor_path = 'data/'
    mkd(actor_path)

    for i, an in enumerate(actor_names):
        rs = []
        for row in str(an).split('\n'):
            if row.startswith('<a'):
                x = re.search('title=\"(.*?)\">', row).group(1)
                rs.append(x)
        with open(os.path.join(actor_path, col_names[i]+'.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(rs))

def cs(n):
    import random
    bound = 498
    d = {}
    res = []
    for _ in range(n):
        rd = random.randint(0, bound)
        if rd in d:
            res.append(d[rd])
        else:
            res.append(rd)
        d[rd] = d.get(bound, bound)
        bound -= 1
    return sorted(res)

def rs():
    col_names = ['中国大陆', '中国香港', '中国台湾', '日本', '韩国', '欧美']
    ss = [180, 180, 180, 180, 180, 100]
    res = []
    for i in range(6):
        sl = cs(ss[i])
        with open('data/{}.txt'.format(col_names[i]), 'r', encoding='utf-8') as f:
            x = f.readline()
            tot = i = 0
            while x and i < len(sl):
                if tot == sl[i]:
                    i += 1
                    res.append(x.strip())
                tot += 1
                x = f.readline()
    return res

def f():
    col_names = ['中国大陆', '中国香港', '中国台湾', '日本', '韩国', '欧美']
    res = []
    for i in range(6):
        with open('data/{}.txt'.format(col_names[i]), 'r', encoding='utf-8') as f:
            x = f.read().strip('\n').split('\n')
            res.extend(x)
    return res

if __name__ == '__main__':
    # fetch_movie_stars()
    # rs_list = rs()
    # with open('data/all.txt', 'w', encoding='utf-8') as f:
    #     f.write('\n'.join(rs_list))
    slist = f()
    with open('data/extend.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(slist))
