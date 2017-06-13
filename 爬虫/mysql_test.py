# -*- coding: utf-8 -*-：
import urllib2
import re
import MySQLdb
import datetime
import urlparse
import time
import urllib

coon = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='book',
    charset='utf8'
)

cur = coon.cursor()

sql = "insert into test(name) VALUES (%s)"
cur.execute(sql,("zzz"))
coon.commit()