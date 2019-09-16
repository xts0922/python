import requests
import time
import MySQLdb
from lxml import etree

#去横线
def remove(str):
    if str == "--":


        return " "
    else:
        return str

def get_proxy():
    proxy = requests.get("http://192.168.10.190:5000/random").text

    print(proxy)

    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    return proxies
start_url = "http://school.aoshu.com/province/3111/p{}"
headers = {
        'User-Agent': 'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
}
def get_finalPage(province_url):

    res = requests.get(province_url, headers=headers).text
    html = etree.HTML(res)
    final_page = html.xpath('//nav[@class="page_Box tc"]/a[last()-1]/text()')[0]
    return final_page
def get_province_url():
    home_page = "http://school.aoshu.com/province"
    res = requests.get(home_page, headers=headers).text
    html = etree.HTML(res)
    province_url_list = html.xpath('//section[@class ="filtarea clearfix"]/p[1]/a/@href')
    # 第一个url没用
    province_url_list.pop(0)
    return province_url_list
# 获取所有页码的url
def get_pageUrl(province_url):
    page_url_list = []

    final_page = int(get_finalPage(province_url)) + 1
    for i in range(1, final_page):
        url = province_url + 'p' + str(i) + '/'

        page_url_list.append(url)

    return page_url_list
def parse(school_url,province_name):
    results = []

    school_id = school_url.split("/")[-2]
    school_res = requests.get(school_url, headers=headers).text
    school_html = etree.HTML(school_res)
    school_icon = school_html.xpath('//div[@class="school"]//dt//img//@src')[0]

    try:
        school_category = school_html.xpath('//div[@class="school"]//dd//td/span/text()')[0]
    except:
        school_category = " "
    try:
        school_name = school_html.xpath('//dl[@class="clearfix"]//dd//tr[1]//td[2]//a/text()')[0]
    except:
        school_name = " "
    class_type = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[2]//td[1]//text()')[0].split("：")[-1])
    current_principal = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[2]//td[2]//text()')[0].split("：")[-1])
    accommodation = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[3]//td[1]//text()')[0].split("：")[-1])
    founding_year = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[3]//td[2]//text()')[0].split("：")[-1])
    entrance_method = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[4]//td[1]//text()')[0].split("：")[-1])
    school_telephone = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[4]//td[2]//text()')[0].split("：")[-1])
    question_type = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[5]//td[1]//text()')[0].split("：")[-1])
    school_address = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[5]//td[2]//text()')[0].split("：")[-1])
    special_enrollment = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[6]//td[1]//text()')[0].split("：")[-1])
    school_website = remove(
        school_html.xpath('//dl[@class="clearfix"]//dd//tr[6]//td[2]//text()')[0].split("：")[-1])
    url = "http://school.aoshu.com/school/sxgl/" + school_url.split("/")[-2] + "/"
    school_introduction_res = requests.get(url, headers=headers).text
    school_introduction_html = etree.HTML(school_introduction_res)
    school_introduction = school_introduction_html.xpath("//article//p//text()")
    school_introduction = "".join(school_introduction)
    temp = []
    temp.extend([school_id,school_icon,school_category,school_name,class_type,current_principal,accommodation,founding_year,entrance_method,school_telephone,question_type,school_address,special_enrollment,school_website,school_introduction,province_name])
    results.extend(temp)

    return results
def get_school_url_list(page_url):
    res = requests.get(page_url, headers=headers).text
    html = etree.HTML(res)
    school_url_list = html.xpath('//dl[@class="fl clearfix"]/dt//a/@href')
    return school_url_list
def sava(results):
    conn = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='dd_middle_school', charset='utf8')
    cursor = conn.cursor()

    print(tuple(results))

    sql = "insert into middleschool_copy1 values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (tuple(results))

    print(sql)
    #会存在第二页出现重复的学校

    cursor.execute(sql)


    conn.commit()

    cursor.close()
    conn.close()
def get_province_name(province_url):
    res = requests.get(province_url, headers=headers).text
    html = etree.HTML(res)
    province_name = html.xpath('//section[@class="filtarea clearfix"]//a[@class="cur"]/text()')[0] +"省"
    return province_name
def exist(school_url):
    conn = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='dd_middle_school', charset='utf8')
    cursor = conn.cursor()

    school_id = school_url.split("/")[-2]

    sql = "select * from middleschool_copy1 where school_id = %s" % school_id


    # 会存在第二页出现重复的学校

    cursor.execute(sql)
    results = cursor.fetchone()



    conn.close()
    return True if results else False
def crawl(province_url):

    province_name = get_province_name(province_url)

    # 获取每个省份的所有页面url

    page_url_list = get_pageUrl(province_url)


    for page_url in page_url_list:
        # 获取每个页面的学校URLi
        print(page_url)
        school_url_list = get_school_url_list(page_url)
        for school_url in school_url_list:
            if not exist(school_url):
                print(school_url)
                results = parse(school_url,province_name)
                sava(results)

if __name__ == '__main__':
    #获取所有省份URL
    province_url_list = get_province_url()
    for province_url in province_url_list:
        print("采集省份" + province_url)


        try:
            crawl(province_url)
        # 有些省份没有数据
        except:
            continue
        print("采集省份" + province_url + "采集完成")
