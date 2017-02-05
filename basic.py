# -*- coding: utf-8 -*-
# filename: basic.py
__author__ = 'cherish'
import urllib2

import time
import json

class Basic:
    def __init__(self):
        print("this is basic")
        self.__accessToken = ''
        self.__leftTime = 0
    def __real_get_access_token(self):
        appId = "wx9a2257e132f7a201"
        appSecret = "76dc377dcdd798c25bfb654acc9ecad3"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        print(postUrl,"\n")
        urlResp = urllib2.urlopen(postUrl)
        print(urlResp,"\n")
        urlResp = json.loads(urlResp.read().decode('utf-8'))

        self.__accessToken = urlResp['access_token']
        print(self.__accessToken,'\n')
        self.__leftTime = urlResp['expires_in']
        print(self.__leftTime,'\n')
    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
                print("lefttime",self.__leftTime)
            else:
                self.__real_get_access_token()

if __name__ == '__main__':
    a = Basic()
    a.run()
