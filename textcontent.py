# -*- coding: utf-8 -*-
# filename: content.py
import time
import orderdatabase
class textcontent(object):
     def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
     #解析字符串，用于除了字符串
     def parseTextContent(self,text):
        if text=="我要订饭":
            #判断时间
            ISOTIMEFORMAT='%H'
            hour = int(time.strftime(ISOTIMEFORMAT,time.localtime()))
            print hour
            if hour>6 and (hour <16):
                replyText  = "您好，小的已经知道了。"
            else:
                replyText = "您好，请在上午六点到下午4点之间订饭，如果紧急需要请主动联系万主任。"


        print(replyText)
        return replyText;


if __name__ == '__main__':
    a = textcontent()
    a.parseTextContent("我要订饭")
