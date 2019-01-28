# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 19:16:02 2018

@author: xy
"""
#This script is used to learn the grammar of Python
from bs4 import BeautifulSoup as BS
import re
import urllib
import time
import os
import win32api, win32con, win32gui

def isExisted(path):
    #判断今天的图片是否已存在
    #生成今天的图片的名字
    t=time.localtime(time.time())
    today_name = str(t[1])+'月'+str(t[2])+'日.jpg'
    #读取存图片文件夹下所有图片名称
    files = get_filenames(path)
    #如果已存在 返回空字符串 如果不存在 返回今天应存储的图片名称
    if today_name in files:
        return ''
    else:
        return today_name

def get_filenames(path):
    for root, dirs, files in os.walk(path):
        filenames = files
    return filenames

def download_picture(img_name):
    #下载必应背景图
    #访问必应 解析html
    path = 'https://cn.bing.com'
    page = urllib.request.urlopen(path)
    htmlcode = page.read().decode()
    '''
    此为必应背景图在源码中的url
    g_img={url: "/az/hprichbg/rb/OceanDrive_ZH-CN8199064696_1920x1080.jpg"}
    '''
    #构造正则表达式 针对bing网站的html文件，只需要搜索img标签下的.jpg即可得到想要的图片的URL
    #2019 1 19更新 bing改版了，图片的url存在background-image:后面了。
    reg = r'background-image:.*?\.jpg'
    
    res = re.findall(reg,htmlcode)
    idx = res[0][22:]
    imgPath = path+'/'+idx
    #下载图片 并以指定名称存到指定位置
    f = urllib.request.urlopen(imgPath)
    data = f.read()
    with open(img_name,'wb') as code:
        code.write(data)

def change_desktop(img_name):
    #修改注册表以更换桌面
    #打开对应注册表
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
        "Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    #修改相应键值
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2") 
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    #指定桌面图片路径
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_name, 1+2)

def run():
    while True:    
        #因为我设置该程序开机自启动，开机可能未联网，故设置5秒等待时间。
        time.sleep(5)
        #path为图片存储路径
        path = 'C:\\Users\\xy\\bingpictures\\'
        image_name = isExisted(path)
        if len(image_name) != 0:
            download_picture(path+image_name)
            change_desktop(path+image_name)
        else:
            break
run()
