#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup

now = time.strftime('%m/%d/%y %H:%M', time.gmtime(time.time()+32400))
url = 'http://truewarrant.elwprice.tk/elw/search/search.jsp'
#url = 'http://www.junkim.ga/elw/search/search.jsp'
#url = 'http://www.truewarrant.com/elw/search/search.jsp'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
data = {'gb1_1':'2001'}
file = '/var/www/html/result.html'
file2 = '/var/www/html/realtime-elw-price.html'
head = """<html>
<head>
<title>ELW price</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<table>
"""
head2 = """<html>
<head>
<title>ELW price</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
"""
footer = """
</table>
</body>
</html>
"""
body = ""
jongmoks = ['00003','00005']
durations = ['1','2','3']

def sum_of_option():
    base_url = 'http://esignal.co.kr/get/get_jupo.php'
    query_string = {'_': str(int(time.time()))+'000'}
    fin = requests.get(base_url, params=query_string, headers=headers)
    now_list = fin.json()[-1]
    sum_value = now_list[1]
    return sum_value

def getData(jongmok,duration):
    min = 0
    max = 0
    nextKey = ''
    _body = ''

    while True:
        data['gb2_1'] = jongmok
        data['gb4_1'] = duration
	data['nextKey'] = nextKey
        html = requests.post(url,data,headers=headers)
        source = BeautifulSoup(html.text, "html.parser")
        target_list = source.findAll(attrs={'name':'data_check'})
        if not target_list:
            break
        else:
            for l in target_list:
                _body = _body + str(l.findParent().findParent())
            if min is 0 and max is 0:
                nextKey = '00000|00031'
                min = 0
                max = 31
            else:
                min = max
                max = max + 30
                nextKey = '%s|%s'%(str(min).zfill(5),str(max).zfill(5))
        time.sleep(0.2)
    return(_body)

for duration in durations:
    for jongmok in jongmoks:
        body = body + getData(jongmok,duration)

sumOfOption = sum_of_option()
body2 = """<tr><td/><td>Sum of Option</td><td>{}</td><td>{}</td></tr><tr><td></td><td>종목코드</td><td>종목명</td><td>현재가</td><td>거래량(천)</td><td>행사가</td><td>전환비율</td><td>패리티</td><td>잔존일</td><td>레버리지</td><td>델타</td></td></tr>""".format(sumOfOption,now)

final_content = head + body + footer
final_content = final_content.replace('<td width="1"></td>','')
final_new_content = head + body2 + body + footer
final_new_content = final_new_content.replace('<td width="1"></td>','')

f = open(file,"w")
f.write(final_content)
f.close

f = open(file2,"w")
f.write(final_new_content)
f.close
