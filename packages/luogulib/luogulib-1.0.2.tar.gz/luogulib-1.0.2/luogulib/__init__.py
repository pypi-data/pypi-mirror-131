# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from functools import wraps
import urllib.parse

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

class LuoguLogin(requests.auth.AuthBase):
    @Developing
    def __init__(self,username,password,captcha):
        self.username = username
        self.password = password
        self.captcha = captcha
    @Developing
    def __call__(self,r):
        # 实现
        return r

class Luogu(object):
    def __init__(self,username,password,ua):
        self.__username = username
        self.__password = password
        self.__syncToken = ''
        self.__uid = 0 # Deprecated
        self.__headers = {
            'User-Agent': ua,
            'referer': 'https://www.luogu.com.cn/',
            'x-luogu-type': 'content-only'
        }
        self.__session = requests.session()

    def getcsrf(self,addr):
        r = self.__session.get(addr,headers=self.__headers)
        if not r.status_code == 200:
            raise AttributeError()
        soup = BeautifulSoup(r.text,features='html.parser')
        self.__headers['x-csrf-token'] = soup.find(attrs={'name': 'csrf-token'})['content']

    def getLoginCaptcha(self):
        return self.__session.get('https://www.luogu.com.cn/api/verify/captcha',headers=self.__headers).content

    def login(self,captcha):
        LoginRequest = {
            'username': self.__username,
            'password': self.__password,
            'captcha': captcha
        }
        LoginResponse = self.__session.post('https://www.luogu.com.cn/api/auth/userPassLogin',headers=self.__headers,json=LoginRequest).json()
        self.__username = LoginResponse['username']
        self.__syncToken = LoginResponse['syncToken']
        self.__session.get('https://www.luogu.com.cn'+LoginResponse['redirectTo'],headers=self.__headers)

    @Deprecated
    def sync(self):
        r = self.__session.post('https://www.luogu.org/api/auth/syncLogin',headers=self.__headers,json={'syncToken':self.__syncToken}).json()
        print(r)
        self.__uid = r['uid']

    @Deprecated
    def getUid(self):
        return self.__uid

    def getUsername(self):
        return self.__username

    def getProblems(self,searchJson):
        parms = urllib.parse.urlencode(searchJson)
        return self.__session.get('https://www.luogu.com.cn/problem/list?'+parms,headers=self.__headers).json()