# -*- coding: utf-8 -*-
# ======================================
# @File    : pic.py
# @Time    : 2020/5/27 16:14
# @Author  : Rivarrl
# ======================================
from baidu_crawler import Baidu
import time
import os

def name1():
    # 做一个下次扩充数据时判重
    root_dir = './image'
    people = set(os.listdir(root_dir))
    with open('./data/extend.txt', 'r', encoding='utf-8') as f:
        a = f.read()
    name_list = a.split('\n')
    print(name_list)
    # 先爬1000人
    for i in range(len(name_list)):
        name = name_list[i].strip()
        if name in people: continue
        people.add(name)
        print('+'*60)
        print('爬，{}图片'.format(name))
        bd = Baidu(name, 1, 15, root_dir)
        bd.queryset()
        print('{}的图片，爬完了'.format(name))
        print('当前进度：{}/{}'.format(i+1, len(name_list)))
        print('+'*60)
        time.sleep(2)

def name3():
    root_dir = './image/test3'
    people = set(os.listdir(root_dir))
    path = 'D:\projects\python\\face_rec\data\classify\\1'
    name_list = os.listdir(path)
    for i in range(len(name_list)):
        name = name_list[i].rstrip('.jpg')
        if name in people: continue
        people.add(name)
        print('+'*60)
        print('爬，{}图片'.format(name))
        bd = Baidu(name, 1, 35, root_dir, {'z':'2'})
        bd.queryset()
        bd = Baidu(name, 1, 35, root_dir, {'z':'3'})
        bd.queryset()
        bd = Baidu(name, 1, 30, root_dir, {'z':'9'})
        bd.queryset()
        print('{}的图片，爬完了'.format(name))
        print('当前进度：{}/{}'.format(i+1, len(name_list)))
        print('+'*60)

if __name__ == '__main__':
    name3()