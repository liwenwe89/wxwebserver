# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web

class Handle(object):
    def GET(self):
        print("THIS IS GET")
        try:
            data = web.input()
            if len(data) == 0:
                print("len(data) == 0")
                return "hello, this is handle view"

            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "xiaoheidashuaige" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print ("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument
    def POST(self):
        print("THIS IS HERE")
        try:
            webData = web.data()
            if len(webData) == 0:
                return "data IS None"
            else:
                print("Handle Post webdata is", webData)   #后台打日志
                recMsg = receive.parse_xml(webData)
                if isinstance(recMsg, receive.Msg):
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                
                    if recMsg.MsgType == 'text':
                        content = "王木木是大美女"
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()
                    if recMsg.MsgType == 'image':
                        mediaId = recMsg.MediaId
                        replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                        return replyMsg.send()
                if isinstance(recMsg, receive.EventMsg):
                    if recMsg.Event == 'CLICK':
                        if recMsg.Eventkey == 'mpGuide':
                            content = u"编写中，尚未完成".encode('utf-8')
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()
                else:
                    print ("暂且不处理")
                    return "success"
        except Exception as Argment:
           return Argment
