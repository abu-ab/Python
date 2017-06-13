# -*- coding: utf-8 -*-
import re
import urllib2
import requests
import MySQLdb

username = "1524051107"
password = "9763428118"


lt_url = "http://my.siit.edu.cn"
login_url = "http://cas.siit.edu.cn:88/cas/login?service=http://my.siit.edu.cn/c/portal/login"
cookies_url = "http://cas.siit.edu.cn:88/cas/login?service=http://jw.siit.edu.cn/login_cas.aspx/"
ve_url = "http://jw.siit.edu.cn/xscj_gc.aspx?xh=%s" % username
check_url = "http://jw.siit.edu.cn/style/js/check.js"

session = requests.session()
coon = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='siit',
    charset='utf8'
)

cur = coon.cursor()
sql = "insert into siit_tb(username,password,name,college,major,class,course," \
      "course_nature,credit,grade_point,achievement,course_college)" \
      " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
def return_re(rule,html):
    pattern = re.compile(rule, re.S)
    text = re.findall(pattern, html)
    return text



def download( url, headers={}, from_data={}):
    print from_data
    print headers
    print 'Downloading:', url
    try:
        html = session.post(url, headers=headers, data=from_data)
    except urllib2.URLError as e:
        print 'Download Error:', e.reason
        html = None

    return html.text


def get_lt():
    html = session.get(lt_url).text
    lt = return_re("<input type=\"hidden\" name=\"lt\" value=\"(.*?)\" />", html)
    return lt


def login():

    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1",
        "Host": "cas.siit.edu.cn:88"
    }

    from_data = {
        "username": username,
        "password": password,
       "_rememberMe": "on",
        "lt": get_lt(),
        "_eventId": "submit"
    }

    download(login_url, headers, from_data)
    # 登录成功
    #print session.get(login_url).text

def get_ve():

    # 获取cookies
    session.get(cookies_url)
    # 获取提交参数
    html = session.get(ve_url).text
    VIEWSTATE = return_re('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', html)
    EVENTVALIDATION = return_re('<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', html)
    print VIEWSTATE
    print EVENTVALIDATION
    return VIEWSTATE,EVENTVALIDATION

def response_item():
    VIEWSTATE,EVENTVALIDATION = get_ve()

    from_data = {
        "Button2": "在校学习成绩查询",
        "__VIEWSTATE": VIEWSTATE,
        "ddlXN": "",
        "ddlXQ": "",
        "__EVENTVALIDATION": EVENTVALIDATION
    }

    session.get(check_url)
    html = session.post("http://jw.siit.edu.cn/xscj_gc.aspx?xh=1524051107", headers={
        "Host": "jw.siit.edu.cn",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1",
    }, data=from_data).text
    print html
    table = return_re(
        '<table class="datelist" cellspacing="0" cellpadding="3" border="0" id="Datagrid1" style="width:100%;border-collapse:collapse;">(.*?)</table>',
        html)
    print
    #print table[0]
    # table = str(table[0])
    table = table[0]
    items = return_re(
        "<tr.*?>.*?<td>.*?</td.*?><td>.*?</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?</tr>",
        table)

    name = return_re('<span id="Label5">(.*?)</span>',html)[0][3:]
    college = return_re('<span id="Label6">(.*?)</span>', html)[0][3:]
    major = return_re('<span id="Label7">(.*?)</span>',html)[0]
    _class = return_re('<span id="Label8">(.*?)</span>',html)[0][4:]
    print name,major,_class
    for i in range(1,len(items)):
        str_symptom = str(items[i]).replace('u\'', '\'')
        print str_symptom.decode("unicode-escape")
        cur.execute(sql,(username,password,name,college,major,_class,items[i][0],items[i][1],items[i][2],items[i][3],items[i][4],items[i][5]))
        coon.commit()


login()
response_item()

# f = open("pass.txt")             # 返回一个文件对象
# line = f.readline()             # 调用文件的 readline()方法
# while line:
#     print line,               # 后面跟 ',' 将忽略换行符
#     # print(line, end = '')　　　# 在 Python 3中使用
#     line = f.readline()
#
# f.close()