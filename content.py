# -*- coding: utf-8 -*-
# filename: content.py
import web
import sqlite3
import time
class Content(object):
     def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0


if __name__ == '__main__':
    a = Content()

    conn = sqlite3.connect('test.db')
    cur = conn.cursor();
    count = 0
    print "cur = conn.cursor();"
    sqlite3_string = '''CREATE TABLE IF NOT EXISTS SummaryTable (
                         userID TEXT PRIMARY KEY  NOT NULL,
                         userName TEXT  NOT NULL,
                         totalOrder INTEGER  NOT NULL);'''
    conn.execute(sqlite3_string)


    #判断是否存在这个ID
    #总表中新增，一行
    userID = "xxxx"
    userName = "xxxxx"
    sqlite3_string= "SELECT userName FROM summaryTable WHERE userID='"+userID+"';"
    sqlite3_string= "SELECT userName FROM summaryTable WHERE userID='xxxx';"
    cursor=conn.execute(sqlite3_string)
    str_temp = 'sb'

    cursor.fetchall()
    for i in cursor:
        print(i)
        str_temp = i[0]
        print'1',str_temp,'\n'
    if str_temp == 'sb':
        print "2", str_temp,'\n'

    print "333",cursor.lastrowid
    print "444",cursor.rowcount
    sqlite3_string = " DELETE FROM SummaryTable WHERE userID='xxxx';"
    conn.execute(sqlite3_string)
    totalOrder = 0
    sqlite3_string = " INSERT INTO SummaryTable (userID,userName,totalOrder) VALUES ("+"'"+userID+"','"+userName+"',"+str(totalOrder)+");"
    print( sqlite3_string)
    conn.execute(sqlite3_string)
    conn.commit();#执行完成 提交

    #查询是否存在这个ID

    #建立 分表
    ISOTIMEFORMAT='%Y%m%d'
    timestr = time.strftime(ISOTIMEFORMAT,time.localtime())
    tablenameStr="Date"+timestr
    sqlite3_string = "select count(*) as 'count' from sqlite_master where type ='table' and name = '"+tablenameStr+"'"
    print(sqlite3_string)
    cursor=conn.execute(sqlite3_string)
    #这里比较奇怪的是，cusor本身是一个二维表格？
    count = 0; #消除
    for i in cursor:
        count = i[0]
        print(count)
    if count:
        print tablenameStr+"Is Exist"
    else:
        sqlite3_string = "CREATE TABLE "+tablenameStr+" (ID INT PRIMARY KEY NOT NULL,userName TEXT   NOT NULL);"
    print(sqlite3_string)
    conn.execute(sqlite3_string)

    #conn.execute( ''' select name from test.db where type = 'table' order by name''')
  #  conn.execute(''' select count(*) as 'count' from sqlite_master where type ='table' and name=Date20170206;''')
  #  cursor=conn.execute('''SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;''')


 #        print "NAME = ", row[1]
 #        print "ADDRESS = ", row[2]
 #        print "SALARY = ", row[3], "\n"



   # conn.execute(sqlite3_string)
    #conn.execute('''SELECT * FROM COMPANY WHERE AGE >= 25 AND SALARY >= 65000;''')
    print "Table created successfully";
    conn.close()