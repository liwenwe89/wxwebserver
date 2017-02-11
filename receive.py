# -*- coding: utf-8 -*-
# filename: receive.py
import xml.etree.ElementTree as ET

def parse_xml(web_data):

    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'event':
        event_type = xmlData.find('Event').text
        if event_type == 'CLICK':
            print "CLICK"
            return Click(xmlData)
        #elif event_type in ('subscribe', 'unsubscribe'):
            #return Subscribe(xmlData)
        #elif event_type == 'VIEW':
            #return View(xmlData)
        #elif event_type == 'LOCATION':
            #return LocationEvent(xmlData)
        #elif event_type == 'SCAN':
            #return Scan(xmlData)
    elif msg_type == 'text':
        print("text")
        return TextMsg(xmlData)
    elif msg_type == 'image':
        print("image")
        return ImageMsg(xmlData)
    print ("parse_xml this is here")


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

class EventMsg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.Event = xmlData.find('Event').text
class Click(EventMsg):
    def __init__(self, xmlData):
        EventMsg.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text