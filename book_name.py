# -*- coding: utf-8 -*-：
import urllib2
import re

def download(url):
    print  'Downloading：',url
    try:
        html = urllib2.urlopen(url).read()

    except urllib2.URLError as e:
        print  'Download error ：',e.reason
        html = None;

    return html.decode('utf-8');


book = []
url = 'https://book.douban.com/tag/'
pattern = re.compile('<a href="/tag/.*?">(.*?)</a>',re.S)
print download(url)