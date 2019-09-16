import requests

import  json
import  MySQLdb
import  os

import lxml
def get_professional_id(school_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
    }
    res = requests.get(school_url,headers=headers).text
    res = json.loads(res)
    res_list = res["special_detail"]["1"]
    if res_list:
        id_list =  [i["id"] for i in res_list]
    else:
        res_list = res["special_detail"]["2"]
        id_list = [i["id"] for i in res_list]
    return id_list


def select_db():
    conn = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='take_data', charset='utf8')
    cur = conn.cursor()
    cur.execute("select college_id from eol_college group by college_id")
    id_list = cur.fetchall()
    return  id_list
def sava_file(res,sava_dir):

        with open(sava_dir, 'wb') as f:
            f.write(res)

school_list = select_db()
# url_list = ("https://static-data.eol.cn/www/school/{}/pc_special.json".format(i[0]) for i in school_list)
#
# pre_school_url = ("https://static-data.eol.cn/www/school/{}/special/2019/".format(i[0]) for i in school_list)
# https://static-data.eol.cn/www/school/38/special/2019/650.json

for school_id in school_list:
    school_url = "https://static-data.eol.cn/www/school/{}/pc_special.json".format(school_id[0])
    print(school_url)

    try:
        id_list = get_professional_id(school_url)
    except:
        continue

    print(id_list)
    for id in id_list:
        json_url = "https://static-data.eol.cn/www/school/{}/special/2019/{}.json".format(school_id[0],id)
        sava_url = "D:/xiatian/static-data.eol.cn/static-data.eol.cn/www/school/{}/special/2019/{}.json".format(school_id[0],id)
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
        }
        if os.path.exists(sava_url) is False:
            res =  requests.get(json_url,headers=headers).content
            sava_file(res,sava_url)
            print(json_url + "已入库")




