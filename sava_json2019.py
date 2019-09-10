from retrying import retry
import requests
import MySQLdb
import os
import time
@retry
def get_proxy():
    proxy = requests.get("http://192.168.10.190:5000/random").text

    print(proxy)

    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    return proxies
def select_db():
    conn = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='take_data', charset='utf8')
    cur = conn.cursor()
    cur.execute("select school_id,id from professional_copy")
    id_list = cur.fetchall()
    return id_list
def sava_file(res,sava_dir):

    with open(sava_dir, 'wb') as f:
        f.write(res)
    print(sava_dir+"已入库")

@retry(stop_max_attempt_number=3)
def get_content1(url,proxies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
    }
    try:
        res = requests.get(url, headers=headers,timeout=5,proxies=proxies).content
    except:
        time.sleep(3)
        res = requests.get(url, headers=headers).content
    return res
def get_content(url,proxies):

    try :

        res = get_content1(url,proxies)

    except:
        proxies = get_proxy()
        res = get_content1(url, proxies)
    return res

def get_content2(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
    }

    res = requests.get(url, headers=headers).content
    return res
if __name__ == '__main__':
    #1 从数据库查询id_list
    id_list=select_db()
    # proxies = get_proxy()
    count = 0
    for id in id_list:
        base_dir = "D:/xiatian/static-data.eol.cn/static-data.eol.cn/www/school/{}/special/2018".format(id[0])

        sava_dir = base_dir + "/%s.json" % str(id[1])
        print(sava_dir)

        if os.path.exists(base_dir) is False:
            os.makedirs(base_dir)
        if os.path.exists(sava_dir) is False:

            # count += 1
            # if count % 1 == 0:
            #     proxies = get_proxy()
            url = "https://static-data.eol.cn/www/school/{}/special/2018/{}.json".format(id[0], id[1])

            # 2 访问url获取内容



            # 3 保存文件
            res = get_content2(url)
            sava_file(res,sava_dir)
			
			####3





