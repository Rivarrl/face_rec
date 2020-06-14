# -*- coding: utf-8 -*-
# ======================================
# @File    : baidu_crawler.py
# @Time    : 1/14/20 11:42 PM
# @Author  : Rivarrl
# ======================================

import requests
from threading import Thread
import re
import time
import hashlib
import os

class Baidu:
    """
    爬取百度图片
    """
    def __init__(self, name, page, page_size, root_dir, params=None):
        self.start_time = time.time()
        self.name = name
        self.page = int(page)
        self.ps = int(page_size)
        self.url = 'https://image.baidu.com/search/acjson'
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}# 添加为自己的
        self.num = 0
        self.root_dir = root_dir
        self.params = params

    def queryset(self):
        """
        将字符串转换为查询字符串形式
        """
        pn = 0
        ps = self.ps
        for i in range(self.page):
            pn += ps * i
            name = {'word': self.name, 'pn': pn, 'tn':'resultjson_com', 'ipn':'rj', 'rn':ps}
            if self.params:
                for k, v in self.params.items():
                    name[k] = v
            url = self.url
            self.getrequest(url, name)

    def getrequest(self, url, data):
        """
        发送请求
        """
        print('[INFO]: 开始发送请求：' + url)
        ret = requests.get(url, headers=self.header, params=data)
        if str(ret.status_code) == '200':
            print('[INFO]: request 200 ok :' + ret.url)
        else:
            print('[INFO]: request {}, {}'.format(ret.status_code, ret.url))
        response = ret.content.decode()
        img_links = re.findall(r'thumbURL.*?\.jpg', response)
        links = []
        # 提取url
        for link in img_links:
            links.append(link[11:])
        self.thread(links)

    def saveimage(self, link):
        """
        保存图片
        """
        print('[INFO]:正在保存图片：' + link)
        m = hashlib.md5()
        m.update(link.encode())
        pic_name = m.hexdigest()
        ret = requests.get(link, headers = self.header)
        image_content = ret.content
        dir_name = '/'.join((self.root_dir, self.name))
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        filename = '/'.join((dir_name, pic_name + '.jpg'))
        with open(filename, 'wb') as f:
            f.write(image_content)
        print('[INFO]:保存成功，图片名为：{}.jpg'.format(pic_name))

    def thread(self, links):
        """多线程"""
        self.num +=1
        for i, link in enumerate(links):
            print('*'*50)
            print(link)
            print('*' * 50)
            if link:
                # time.sleep(0.5)
                t = Thread(target=self.saveimage, args=(link,))
                t.start()
                t.join()
            self.num += 1
        print('一共进行了{}次请求'.format(self.num))

    def __del__(self):
        end_time = time.time()
        print('一共花费时间:{}(单位秒)'.format(end_time - self.start_time))

def main():
    name = input('请输入你要爬取的图片类型: ')
    ps = input('请输入每页几张图片:')
    page = input('请输入你要爬取图片的页数:')
    baidu = Baidu(name, page, ps, 'D:\projects\python\\face_rec\data\\raw_data\perform', {'z':'9'})
    baidu.queryset()


if __name__ == '__main__':
    main()