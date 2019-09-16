import requests
import time

import hashlib

def hex_md5(s):
    m = hashlib.md5()
    m.update(s.encode('UTF-8'))
    return m.hexdigest()
url="https://h5api.m.taobao.com/h5/mtop.wdetail.getitemdescx/4.9/?jsv=2.4.11&appKey=12574478&t=1566357361930&sign=edf05683918fe4a0d0695913605f6256&api=mtop.wdetail.getItemDescx&v=4.9&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data=%7B%22item_num_id%22%3A%22544895066973%22%7D"
data ='{"item_num_id":"544895066973"}'
params = {
        'appKey': 12574478,
        'data':  data
}
appKey='12574478'
# 请求空获取cookies

t = str(int(time.time() * 1000))
html = requests.get(url, params=params)
print(html.cookies)
m_h5_tk = html.cookies['_m_h5_tk']
m_h5_tk_enc = html.cookies['_m_h5_tk_enc']
token = m_h5_tk.split('_')[0]

print(token)
u = token + '&' + t + '&' + appKey + '&' + data

sign = hex_md5(u)
headers = {
        'cookie': '_m_h5_tk=' + m_h5_tk + '; _m_h5_tk_enc=' + m_h5_tk_enc,
    }
params = {
        'appKey': appKey,
        't': t,
        'sign': sign,
        'data': data
    }
html = requests.get(url, headers=headers, params=params)
print(html.text)