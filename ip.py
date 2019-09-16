import requests
from bs4 import BeautifulSoup
from lxml import etree
url = "http://www.xicidaili.com/nn/{}"
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"}
# 记录次数
http_url = "http://www.baidu.com"
num = 0
# 我们循环10页抓取
for p in range(1, 11):
    re = requests.get(url.format(p), headers=headers)
    html =etree.HTML(re.content)
    all_trs = html.xpath('//table[@id="ip_list"]')[0]
    tr_list = all_trs.xpath("//tr")[1:]  # 去掉标题
    for tr in tr_list:
        # 提取ip
        ip = tr.xpath('./td[2]/text()')[0]
        # 提取端口
        port = tr.xpath('./td[3]/text()')[0]
        # proxy_info['address'] = tr.xpath('./td[4]/a/text()').extract()[0]
        # 提取速度
        speed = tr.xpath('./td[7]/div/@title')[0]
        speed = (speed.split("秒"))[0]  # 从中把数字数据提取出来
        # 提取类型(http或者https)
        type = tr.xpath('./td[6]/text()')[0]
        # 把延迟速度小于2秒的存入数据可
        if float(speed)<2:
            # print("爬取的ip", ip, port, type, speed)
            proxy_ip = type+"://"+ip+":"+port
            # print(proxy_ip)
            try:
                proxy_dict = {
                    type: proxy_ip
                }
                print("****************")
                print(proxy_dict)
                print(http_url)
                response = requests.get(http_url, proxies=proxy_dict)
                print(response)
                print("---------------")
            except Exception as e:
                print("invalid ip and port", ip, port, type, e)
            else:
                code = response.status_code
                if code == 200:
                    print("有效", ip, port, type)



