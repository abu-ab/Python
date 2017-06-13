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

    return html


book = []
url = 'https://book.douban.com/tag/'
html = download(url)
pattern = re.compile('<a href="/tag/.*?">(.*?)</a>',re.S)
text = re.findall(pattern, html)
print text