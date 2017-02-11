__author__ = 'cherish'


''' 有更为简单的方法 IF NOT EXISTS
    ##建立总表
    sqlite3_string = "select count(*) as 'count' from sqlite_master where type ='table' and name = 'SummaryTable'"

    cursor=conn.execute(sqlite3_string)
    for i in cursor:
        count = i[0]
    print(count)
    if count:
        print "SummaryTableIs Exist"
    else:
        sqlite3_string = 'CREATE TABLE SummaryTable (userID TEXT PRIMARY KEY  NOT NULL,userName TEXT  NOT NULL,totalOrder INTEGER  NOT NULL);'
        conn.execute(sqlite3_string)'''