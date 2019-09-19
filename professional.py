import requests

import os
import  json
import time
import  re
import datetime

import MySQLdb
url = r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\school\30\special\2019\1.json"


def run(url):
    pattern = re.compile(r'<[^>]+>',re.S)
    # 获得当前时间
    now = datetime.datetime.now()  # 这是时间数组格式

    # 转换为指定的格式:
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(url, encoding='utf-8') as file_obj:
        contents = json.load(file_obj)

        college_id = contents["school_id"]
        # specials_id = contents["special_id"]
        spe_name = contents["name"]
        spe_code = contents["id"]
        spe_type = 1 if contents["level1_name"] == "本科" else 2

        content = contents["content"]
        try:
            spe_content = pattern.sub('', content)
        except:
            spe_content = " "
        created_at = otherStyleTime
        update_at = otherStyleTime

        sql = "insert into dd_college_specials(college_id,spe_name,spe_code,spe_type,spe_content,created_at,update_at) values ('%s','%s','%s','%s','%s','%s','%s')" % (college_id,spe_name,spe_code,spe_type,spe_content,created_at,update_at)
        return sql
def execute(sql):

    # 打开数据库连接
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='data_manage', charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()


    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    # for i in range(20,)
    # url = r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\school\{}\special\2019\{}.json"
    # url = url.format(i)
    #
    # sql = run(url)
    #
    # execute(sql)
    for i in range(30,3425):
        url = r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\school\{}\special\2019".format(i)
        try:
            dirs = os.listdir(url)
        except:
            continue
        for file in dirs:

            ffile =url+ '\\' +file
            print(ffile)
            sql = run(ffile)
            execute(sql)