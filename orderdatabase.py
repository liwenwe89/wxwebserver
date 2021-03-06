
# -*- coding: utf-8 -*-
# filename: orderdatabase.py
__author__ = 'cherish'
# 用于数据库的相关操作

import sqlite3
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class orderdatabase(object):
    #初始化 内部变量需要加上self 如self.conn=xxxx
    def __init__(self):

        self.tablename = ""
        self.creatTabledefault()
        self.creatTablebyDate()
        print "this is orderdatabase"
    def creatTabledefault(self):
        conn = sqlite3.connect('orderdatabase.db')
        print "cur = conn.cursor();"
        sqlite3_string = '''CREATE TABLE IF NOT EXISTS SummaryTable (
                         userID TEXT PRIMARY KEY  NOT NULL,
                         userName TEXT  NOT NULL,
                         totalOrder INTEGER  NOT NULL DEFAULT 0);'''
        conn.execute(sqlite3_string)

        conn.close()

    def creatTablebyDate(self):
        ISOTIMEFORMAT='%Y%m%d'
        timestr = time.strftime(ISOTIMEFORMAT,time.localtime())
        tablenameStr="Date"+timestr
        #减少查询，同时避免由于第一次启动导致没有建立表格
        if tablenameStr == self.tablename:
            print("tablenameStr == self.tablename:")
            return tablenameStr;
        else:
            self.tablename=tablenameStr;
            print(self.tablename)
            conn = sqlite3.connect('orderdatabase.db')
            sqlite3_string = "select count(*) as 'count' from sqlite_master where type ='table' and name = '"+tablenameStr+"'"
            print(sqlite3_string)
            cursor=conn.execute(sqlite3_string)
            #这里比较奇怪的是，cusor本身是一个二维表格？
            #游标实际上是一种能从包括多条数据记录的结果集中每次提取一条记录的机制
            count = 0; #消除
            for i in cursor:
                count = i[0]
                print(count)
            if count:
                print tablenameStr+"Is Exist"
            else:
                sqlite3_string = "CREATE TABLE "+tablenameStr+" (userID TEXT PRIMARY KEY NOT NULL," \
                                                              "userName TEXT NOT NULL," \
                                                              "ordered  INT  NOT NULL DEFAULT 0);"
            print(sqlite3_string)
            conn.execute(sqlite3_string)
            conn.close()
            return tablenameStr;

    def insertNewUSER(self,userID,userName):
        #插入新的用户
        isR = self.isRegister(userID)
        if isR == 0:
            #如果用户之前已经注册成功，那么返回错误
            return -1
        elif isR== -1:
            conn = sqlite3.connect('orderdatabase.db')
            totalOrder = 0
            sqlite3_string = " INSERT INTO SummaryTable (userID,userName,totalOrder) VALUES ("+"'"+userID+"','"+userName+"',"+str(totalOrder)+");"

            conn.execute(sqlite3_string)
            conn.commit();#执行完成 提交
            conn.close()
            print("insertNewUSER is OK")
            return 0
    #是否注册过
    def isRegister(self,userID):
        print "this isRegister\n"
        isR = -1
        conn = sqlite3.connect('orderdatabase.db')
        sqlite3_string = "SELECT totalOrder FROM SummaryTable WHERE userID = '"+userID+"';"
        cusor=conn.execute(sqlite3_string)

        for i in cusor:
            isR = i[0]
        conn.close()
        if isR==-1:
            print("don't registered")
            return isR
        else:
            isR = 0
            print("registered")
            return  isR

    def getNameFromID(self,userID):
        #查询用户
         print "this is getNameFromID"
         conn = sqlite3.connect('orderdatabase.db')
         sqlite3_string = "SELECT userName FROM SummaryTable WHERE userID = '"+userID+"';"
         print sqlite3_string+"\n"
         cursor = conn.execute(sqlite3_string)
         userName = ""
         for i in cursor:

            userName = str(i[0]).encode("utf-8")
            print userName.encode("utf-8") #utf-8 都是泪
         conn.close()
         return str(userName.encode("utf-8"))

    def updateTotalOrder(self,userID,action):
        #更新一个人的总预定数目
        conn = sqlite3.connect('orderdatabase.db')
        sqlite3_string = "SELECT totalOrder FROM SummaryTable WHERE userID = '"+userID+"';"
        cursor = conn.execute(sqlite3_string)
        totalOrder = -1;
        for i in cursor:
            totalOrder = i[0]
        if totalOrder ==-1:
            print "this is no "+userID;
            conn.close()
            return -1
        else:
            if action == 1:
                totalOrder =totalOrder+1
            elif action == -1:
                totalOrder = totalOrder -1
                if totalOrder < 0:
                    totalOrder = 0
            print("totalOrder"+str(totalOrder))
            sqlite3_string="UPDATE SummaryTable SET totalOrder ="+ str(totalOrder)+" WHERE  userID = '"+userID+"';"

            conn.execute(sqlite3_string)
            conn.commit();#执行完成 提交
            conn.close()
            return 0;



    def insterOrder(self,userID,action):
        #按照ID，NAME 写入日期表格
        tablename = self.creatTablebyDate()
        #查询是否已经定过了
        conn = sqlite3.connect('orderdatabase.db')
        ordered = self.isOrdertoday(userID)
        #说明没有订餐过
        if action == 1:
            if ordered == -1:
                print "ordered == -1"
                sqlite3_string = "SELECT userName FROM SummaryTable WHERE userID = '"+userID+"';"
                cursor = conn.execute(sqlite3_string)
                userName = ""
                ordered = 1
                for i in cursor:
                    userName = i[0]
                sqlite3_string = " INSERT INTO "+tablename+" (userID,userName,ordered) VALUES ("+"'"+userID+"','"+userName.encode("utf-8")+"',"+str(ordered)+");"
                print sqlite3_string
                conn.execute(sqlite3_string)
                conn.commit()
                conn.close()
                #更新数据
                self.updateTotalOrder(userID,action)
                return 0
            elif ordered == 1:
                #说明已经订餐过
                print("ordered == 1")
                conn.close()
                return 2
            #取消又添加了
            elif ordered == 0:
                print("ordered = 0")
                ordered = 1
                sqlite3_string="UPDATE "+tablename+" SET ordered ="+str(ordered) +" WHERE  userID = '"+userID+"';"
                print(sqlite3_string)
                conn.execute(sqlite3_string)
                #执行完成 提交
                conn.commit()
                conn.close()
                self.updateTotalOrder(userID,action)
                #表示update
                return 1
            else:
                conn.close()
                return -1 #哪里出现了问题
        elif action == -1:
            #取消订单
            #还未定过，不需要任何操作
             if ordered == -1:
                return 0
             elif ordered == 1:
                #说明已经订餐过
                print("ordered == 1")
                ordered = 0
                sqlite3_string="UPDATE "+tablename+" SET ordered ="+str(ordered) +" WHERE  userID = '"+userID+"';"
                print(sqlite3_string)
                conn.execute(sqlite3_string)
                #执行完成 提交
                conn.commit()
                conn.close()
                #取消后总数也减少
                self.updateTotalOrder(userID,action)
                return 2;
             #最终取消了，不要任何操作
             elif ordered == 0:
                print("ordered = 0")
                #表示update
                return 1
             else:
                conn.close()
                return -1 #哪里出现了问题

    def isOrdertoday(self,userID):
        #查询一个人今天是否已经订饭了
        tablename = self.creatTablebyDate()
        ordered = -1
        sqlite3_string = "SELECT ordered FROM "+tablename+" WHERE userID = '"+userID+"';"
        conn = sqlite3.connect('orderdatabase.db')
        cursor = conn.execute(sqlite3_string)
        print"\n"+(sqlite3_string)
        for i in cursor:
            ordered = i[0]
        conn.close()
        print "isOrdertoday "+str(ordered)
        return ordered

    def howManyOrderToday(self):  #需要数组
        ISOTIMEFORMAT='%Y%m%d'
        timestr = time.strftime(ISOTIMEFORMAT,time.localtime())
        tablenameStr="Date"+timestr
        conn = sqlite3.connect('orderdatabase.db')
        sqlite3_string = "SELECT ordered FROM "+tablenameStr+" ;"
        print sqlite3_string+"\n"
        cursor = conn.execute(sqlite3_string)
        count = 0

        for i in cursor:
            count = count + i[0]
        sqlite3_string = "SELECT userID,userName FROM "+tablenameStr+" WHERE ordered=1;"
        print sqlite3_string+"\n"
        cursor = conn.execute(sqlite3_string)
        idAndName = {}
        idList = []
        namelist = []
        for i in cursor:
            idAndName[str(i[0]).encode("utf-8")]=str(i[1]).encode("utf-8")
            idList.append(str(i[0]).encode("utf-8"))
            namelist.append(str(i[1]).encode("utf-8"))
        return count,idList,namelist,idAndName



if __name__ == '__main__':
    a=orderdatabase()
    #创建初始数据库和表格
 #   a.creatTabledefault()
 #   a.creatTablebyDate()
 #   a.insertNewUSER("asdd","cctv")
 #   a.updateTotalOrder("asdd")
 #   a.updateTotalOrder("asdds")
 #   print a.isRegister("asdds")
 #   a.insertNewUSER("asdds","asdadasd")
    a.insterOrder("asdds")