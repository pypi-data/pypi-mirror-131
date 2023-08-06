# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from functools import wraps
import urllib.parse
from PIL import Image

def Deprecated(func):
    @wraps(func)
    def wrapper(*args):
        print('函数已经被弃用:',func.__name__)
        return func(*args)
    return wrapper

def Developing(func):
    @wraps(func)
    def wrapper(*args):
        print('函数还在开发中:',func.__name__)
        return func(*args)
    return wrapper

codec = {
    '0': (0, 0, 0),
    '1': (255, 255, 255),
    '2': (170, 170, 170),
    '3': (85, 85, 85),
    '4': (254, 211, 199),
    '5': (255, 196, 206),
    '6': (250, 172, 142),
    '7': (255, 139, 131),
    '8': (244, 67, 54),
    '9': (233, 30, 99),
    'a': (226, 102, 158),
    'b': (156, 39, 176),
    'c': (103, 58, 183),
    'd': (63, 81, 181),
    'e': (0, 70, 112),
    'f': (5, 113, 151),
    'g': (33, 150, 243),
    'h': (0, 188, 212),
    'i': (59, 229, 219),
    'j': (151, 253, 220),
    'k': (22, 115, 0),
    'l': (55, 169, 60),
    'm': (137, 230, 66),
    'n': (215, 255, 7),
    'o': (255, 246, 209),
    'p': (248, 203, 140),
    'q': (255, 235, 59),
    'r': (255, 193, 7),
    's': (255, 152, 0),
    't': (255, 87, 34),
    'u': (184, 63, 39),
    'v': (121, 85, 72)
}

class PictureCodec:
    @staticmethod
    @Developing
    def encode(r,g,b):
        pass
    @staticmethod
    def decode(code):
        global codec
        return codec[code]

class PaintBoard(object):
    def __init__(self,addr):
        self.__addr = addr
        self.__img = Image.new('RGB',(5000,3000),0x0)