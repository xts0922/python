import requests
import MySQLdb
import re
from lxml import  etree

#数据库连接
conn =MySQLdb.connect(host='192.168.0.129',user='root',passwd='123456',db='take_data',charset='utf8')
cur= conn.cursor()



URL="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/"
start_url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html"
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
start_data = requests.get(start_url, headers=headers).content.decode("gbk")
start_html=etree.HTML(start_data)

url= start_html.xpath('//tr[@class="provincetr"]//a/@href')

name = start_html.xpath('//tr[@class="provincetr"]//a/text()')

for i in range(0,len(url)):
    print(i)
    name1=name[i]
    r=re.findall("\d+",url[i])[0]
    cur.execute("insert into qwe(id,area_name) values (%s,%s)", (r, name1))
    second_url = URL + url[i]
    #第二个页面
    second_html = requests.get(second_url, headers=headers).content.decode("gbk")
    html = etree.HTML(second_html)
    bm = html.xpath('//tr[@class="citytr"]/td[1]/a/text()')
    city = html.xpath('//tr[@class="citytr"]/td[2]/a/text()')
    next_url = html.xpath('//tr[@class="citytr"]/td[1]/a/@href')
    for k in range(0, len(bm)):

        r1=re.findall(r"/(.*)\.html",next_url[k])[0]
        cur.execute("insert into qwe(id,up_id,area_name,area_code) values (%s,%s,%s,%s)", (r1,r,city[k], bm[k]))

        third_url = URL + next_url[k]
        #第三个页面
        third_html = requests.get(third_url, headers=headers).content.decode("gbk")
        html = etree.HTML(third_html)
        bm1 = html.xpath('//tr[@class="countytr"]//td[1]//text()')
        city1 = html.xpath('//tr[@class="countytr"]//td[2]//text()')
        for j in range(0, len(bm1)):
            r3 = re.findall("\d{6}", bm1[j])[0]

            cur.execute("insert into qwe(id,up_id,area_name,area_code) values (%s,%s,%s,%s)",
                                (r3,r1, city1[j], bm1[j]))



cur.close()
conn.commit()
conn.close()
