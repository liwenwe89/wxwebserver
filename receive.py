# -*- coding: utf-8 -*-
# filename: receive.py
import xml.etree.ElementTree as ET

def parse_xml(web_data):
    print ("parse_xml this is here")
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    print("\nxmlData",xmlData)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        print("\ntext\n")
        return TextMsg(xmlData)
    elif msg_type == 'image':
        print("\nimage\n")
        return ImageMsg(xmlData)

class Msg(object):
  
    def __init__(self, xmlData):
        print("\ninit  Msg \n ")
        self.ToUserName = xmlData.find('ToUserName').text
        print("\n self.ToUserName ",self.ToUserName)
        self.FromUserName = xmlData.find('FromUserName').text
        print("\n self.FromUserName  ",self.FromUserName )
        self.CreateTime = xmlData.find('CreateTime').text
        print("\n self.CreateTime ",self.CreateTime)
        self.MsgType = xmlData.find('MsgType').text
        print("\n self.MsgType ",self.MsgType)
        self.MsgId = xmlData.find('MsgId').text
        print("\n self.MsgId ",self.MsgId)

class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text
