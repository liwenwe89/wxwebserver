# -*- coding: utf-8 -*-
# filename: handle.py
import hashlib
import reply
import receive
import web
import orderdatabase
import traceback
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
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
        print("THIS IS POST")
        try:

            webData = web.data()
            if len(webData) == 0:
                return "data IS None"
            else:
                print "Handle Post webdata is "+webData+"\n"   #后台打日志
                recMsg = receive.parse_xml(webData)
                print"@@@@@@@@ 3  isinstance(recMsg, receive.Msg)"
                if isinstance(recMsg, receive.Msg): #判断类型是否一致
                    toUser = recMsg.FromUserName
                    userID = str(recMsg.FromUserName)
                    fromUser = recMsg.ToUserName
                    print  "@@@@@@@@@@4 this is  "+ str(recMsg.MsgType)
                    print "fromUser = recMsg.ToUserName "+str(fromUser)
                    if recMsg.MsgType == 'text':
                        #判断ID是否注册
                        print "this is rec"
                        obj_temp=orderdatabase.orderdatabase()
                        #为什么self 不能省略？？？
                        print recMsg.content

                        if orderdatabase.orderdatabase.isRegister(obj_temp,str(recMsg.FromUserName)) == -1:
                            #加上注册的判断
                            if str(recMsg.content)[0:3] == ":::":#第1到第三，而不是第一到第四
                                orderdatabase.orderdatabase.insertNewUSER(obj_temp,recMsg.FromUserName,str(recMsg.content)[3:20] )
                                content="您已经注册成功，亲爱的"+str(recMsg.content)[3:20]+"\n @王木木"
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                print content
                                return replyMsg.send()
                            content = '''您还未注册，请先进行注册。一旦注册将和微信绑定，无法进行修改。注册方式如下：在对话框内输入如下括号内字符（:::我是xxxx),其中xxxx将作为您的正式名称。'''
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            print content
                            return replyMsg.send()

                        if recMsg.content == "帮助":
                            content = '''订晚饭，请输入 “王木木，订午饭”。取请输入，"王木木，不订饭了"。 开放时间：0:00-16:00'''
                            print content
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                        #做主要判断
                        elif recMsg.content == "王木木，订午饭xxx":
                            content = "午饭已经预定"
                            print content
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                        elif  recMsg.content == "王木木，订晚饭":
                            try:
                                username = orderdatabase.orderdatabase.getNameFromID(obj_temp,str(recMsg.FromUserName))
                                content = username+"：晚饭已经预定。"
                                orderdatabase.orderdatabase.insterOrder(obj_temp,str(recMsg.FromUserName),1)
                                print content
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                            except:
                                print 'catch and show'
                                traceback.print_exc()
                            return replyMsg.send()
                        elif  recMsg.content == "王木木，不订饭了":
                            username = orderdatabase.orderdatabase.getNameFromID(obj_temp,str(recMsg.FromUserName))
                            content = username+"：晚饭已经取消。"
                            orderdatabase.orderdatabase.insterOrder(obj_temp,str(recMsg.FromUserName),-1)
                            print content

                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            return replyMsg.send()
                        elif recMsg.content == "今天多少人订饭":
                            try:
                                if str(recMsg.FromUserName) == "oyePbvjkGXL8VAvtny8MyX4NVX7I" or str(recMsg.FromUserName) == "oyePbvqWHLM0qInHeO3Vaq-dlS_c" : #超级权限
                                    b=orderdatabase.orderdatabase.howManyOrderToday(obj_temp)
                                    print(b)
                                    content = "今天有"+str(b[0]).encode("utf-8")+"人订饭"

                                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                                    return replyMsg.send()
                                else:
                                    content = "请咨询王木木"
                                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                                    return replyMsg.send()
                            except:
                                 print 'catch and show'
                                 traceback.print_exc()
                        elif recMsg.content == "今天哪些人订饭":
                            if str(recMsg.FromUserName) == "oyePbvjkGXL8VAvtny8MyX4NVX7I" or str(recMsg.FromUserName) == "oyePbvqWHLM0qInHeO3Vaq-dlS_c" : #超级权限
                                b=orderdatabase.orderdatabase.howManyOrderToday(obj_temp)
                                content = "今天订饭人员名单如下：\n"
                                for i in b[2]:
                                    content = content+str(i)+"\n"
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                return replyMsg.send()
                            else:
                                content = "请咨询王木木"
                                replyMsg = reply.TextMsg(toUser, fromUser, content)
                                return replyMsg.send()
                        #群发接口被限制，这个功能无法实现，有需求可以做成查询
                        # elif recMsg.content == "通知同学们来拿饭":
                        #     if str(recMsg.FromUserName) == "oyePbvjkGXL8VAvtny8MyX4NVX7I" or str(recMsg.FromUserName) == "oyePbvqWHLM0qInHeO3Vaq-dlS_c" : #超级权限
                        #         b=orderdatabase.orderdatabase.howManyOrderToday(obj_temp)
                        #         content = "饭已经到了，请及时来领取"
                        #         for i in b[1]: #id
                        #             print("饭已经到了，请及时来领取" +i)
                        #             replyMsg = reply.TextMsg(str(i).encode("utf-8"), fromUser, content)
                        #             time.sleep(1)
                        #             replyMsg.send()
                        #         content = "已经通知大家"
                        #         replyMsg = reply.TextMsg(toUser, fromUser, content)
                        #         replyMsg.send()
                        #         return 1.
                        #     else:
                        #         content = "请咨询王木木"
                        #         replyMsg = reply.TextMsg(toUser, fromUser, content)
                        #         return replyMsg.send()


                        #默认值
                        content = "输入括号内文字：（王木木，订晚饭）预定今天晚饭。输入括号内文字：（王木木，不订饭了）取消预定今天晚饭。输入括号内文字：（今天多少人订饭），查询今天定晚饭人数。" \
                                  "输入括号内文字：（今天哪些人订饭），查询具体订饭人员名单。" 

                        print content
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
