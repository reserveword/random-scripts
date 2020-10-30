# -*- coding: UTF-8 -*-
# pylint: disable=C0103
from __future__ import unicode_literals
import os
import random
import win32gui
import win32con
import win32api

# 备选图片的文件夹
img_dir = "D:\\greens\\wallpaper"
imgs = []
total_weight = 0


def setWallpaper(imagepath, mode=1):
    dat = ["10", "6", "2", "0", "0", "22"]
    regkey = win32api.RegOpenKeyEx(
        win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regkey, "WallpaperStyle", 0,
                           win32con.REG_SZ, dat[mode])    
    win32api.RegSetValueEx(regkey, "TileWallpaper", 0,
                           win32con.REG_SZ, str(int(mode == 3)))  # 2拉伸适应桌面,0桌面居中
    win32gui.SystemParametersInfo(
        win32con.SPI_SETDESKWALLPAPER, imagepath, 1 + 2)

'''解析单个图片,返回三元组'''
def parseimg(name):
    global total_weight
    attr = name.split('.')
    if not attr[-1] in ('bmp', 'jpg', 'png', 'jpeg', 'gif'):
        return None
    if not (len(attr) > 2 and attr[0].isdigit() and attr[1].isdigit()):
        return None
    mod = int(attr[0])
    if mod not in (1, 2, 3, 4, 5):
        return None
    if len(attr) > 3 and attr[2].isdigit():
        height = int(attr[2])
        if height == 0:
            height = 100
    else:
        height = 100
    weight = int(attr[1]) / height
    total_weight += weight
    return (weight, mod)

'''取得folder内所有图片存进img[],不匹配模式'''
def parsedir(folder):
    global total_weight
    attr = folder.name.split('.')
    if not (len(attr) > 2 and attr[0].isdigit() and attr[1].isdigit()):
        print("dir",folder.name,"is not well-formed, skipping...")
        return None
    mod = int(attr[0])
    if mod not in (1, 2, 3, 4, 5):
        print("dir",folder.name,"does not have valid mode, skipping...")
        return None
    if len(attr) > 3 and attr[2].isdigit():
        height = int(attr[2])
        if height == 0:
            height = 100
    else:
        height = 100
    if attr[-1] == 'single':
        items = []
        for img in os.scandir(folder.path):
            if img.name.split('.')[-1] in ('bmp', 'jpg', 'png', 'jpeg'):
                items.append(img.path)
        weight = int(attr[1])/height
        for img in items:
            imgs.append((weight/len(items), mod, img))
            total_weight += weight
    elif attr[-1] == 'multi':
        for img in os.scandir(folder.path):
            if img.name.split('.')[-1] in ('bmp', 'jpg', 'png', 'jpeg'):
                weight = int(attr[1])/height
                imgs.append((weight, mod, img.path))
                total_weight += weight

#从目录下取得命名正确的图片,存放于imgs[]的三元组(权重,模式,路径)内'''
def getimgs(path):
    items = os.scandir(path)
    for item in items:
        if os.path.isdir(item.path):
            parsedir(item)
            continue
        img = parseimg(item.name)
        if img != None:
            imgs.append(img+(item.path,))
    return

''' 取随机图片'''
def randomimage(path):
    getimgs(path)
    weight = total_weight
    ran = weight * random.random()
    for img in imgs[1:]:
        if img[0] > ran:
            return img
        ran -= img[0]
    return randomimage(path)


image = randomimage(img_dir)
setWallpaper(image[2], image[1])
