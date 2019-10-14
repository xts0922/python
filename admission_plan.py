import requests

import os
import  json
import time
import  re
import datetime
import sys
import MySQLdb
def get_college_id(college_id):
    sql = "SELECT college_name FROM eol_college where college_id = %s" % college_id
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='take_data', charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    college_name  = cursor.fetchone()
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='data_manage', charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT id FROM dd_college where college_name = "%s"' % college_name

    cursor.execute(sql)
    id = cursor.fetchone()[0]

    return id
def get_specialsId(specials_title):
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='data_manage', charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT id FROM dd_specialized_subject where spe_name = "%s" and level != 0' % specials_title
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    return id
def get_provinceId(province_id):
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='take_data', charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT province_name FROM local_province where province_id = "%s"' % province_id
    cursor.execute(sql)
    province_name = cursor.fetchone()[0]
    db = MySQLdb.connect(host='192.168.0.26', user='root', passwd='54xvX$i96!5LHBfP8SyrvwB6x8q^o%DZ4', db='school_online_saas', charset='utf8')
    cursor = db.cursor()
    province_name ='%'+ province_name + '%'
    sql = 'SELECT id  FROM dd_dict_area where area_name like "%s" and level = 2' % province_name

    cursor.execute(sql)
    id = cursor.fetchone()[0]
    return id
def get_admission_group_type(kelei_id):
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='take_data', charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT local_type_name FROM local_type where local_type_id = "%s"' % kelei_id
    cursor.execute(sql)
    local_type_name = cursor.fetchone()[0]

    return local_type_name

def get_specialsCode(specials_title):
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='data_manage', charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT spe_code FROM dd_specialized_subject where spe_name = "%s" and level != 0' % specials_title
    cursor.execute(sql)
    spe_code = cursor.fetchone()[0]
    return spe_code
def get_edYear(specials_title):
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='data_manage', charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT spe_years_study FROM dd_specialized_subject where spe_name = "%s" and level != 0' % specials_title
    cursor.execute(sql)
    spe_years_study = cursor.fetchone()[0]
    return spe_years_study

def get_specials_group_name(specials_group_code):
    db = MySQLdb.connect(host='192.168.0.129', user='root', passwd='123456', db='data_manage', charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT spe_name FROM dd_specialized_subject where spe_code = "%s" and level != 0' % specials_group_code
    cursor.execute(sql)
    spe_name = cursor.fetchone()[0]
    return spe_name
def run(url,admission_year,kelei_id):
    pattern = re.compile(r'<[^>]+>',re.S)
    # 获得当前时间
    now = datetime.datetime.now()  # 这是时间数组格式
    global  xx
    # 转换为指定的格式:
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(url, encoding='utf-8') as file_obj:

        contents = json.load(file_obj)

        contents_list = contents["data"]["item"]
        sql_list = []
        for contents in contents_list :
            # print(contents)

            college_id = contents["school_id"]
            college_id = get_college_id(college_id)
            # specials_id = contents["special_id"]
            if contents["spname"].find("（") == -1:
                specials_title = contents ["spname"]
                specials_extra_info = " "
            else :
                specials_title = contents["spname"].split("（")[0]
                specials_extra_info = "（" + contents["spname"].split("（")[1]
            specials_id = get_specialsId(specials_title)
            admission_plan_num = contents["num"]
            admission_year = admission_year
            education_length_year = get_edYear(specials_title)
            specials_code = get_specialsCode(specials_title)
            specials_group_code = specials_code[0:4]
            specials_group_name = get_specials_group_name(specials_group_code)
            province_id = contents["province"]
            province_id = get_provinceId(province_id)
            admission_batch = dict[contents["local_batch_name"]]
            admission_group_type = dict1[get_admission_group_type(kelei_id)]
            comment = contents["remark"]
            if contents["level1_name"] == "本科":
                admission_level = 10200
            elif contents["level1_name"] == "专科":
                admission_level = 10201
            else:
                admission_level = 10202

            # # specials_id = contents["special_id"]
            # spe_name = contents["name"]
            # spe_code = contents["id"]
            # spe_type = 1 if contents["level1_name"] == "本科" else 2
            #
            # content = contents["content"]
            # try:
            #     spe_content = pattern.sub('', content)
            # except:
            #     spe_content = " "
            created_at = otherStyleTime
            updated_at = otherStyleTime



            xx = xx + 1
            print(xx)
            sql = "insert into dd_college_admission_plan_copy1(college_id,specials_title,specials_group_code,specials_group_name,education_length_year,admission_group_type,specials_code,admission_year,specials_extra_info,specials_id,admission_plan_num,province_id,admission_batch,comment,admission_level,created_at,updated_at) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s','%s')" \
                  % (college_id, specials_title, specials_group_code, specials_group_name, education_length_year,
                     admission_group_type, specials_code, admission_year, specials_extra_info, specials_id,
                     admission_plan_num, province_id, admission_batch, comment, admission_level, created_at, updated_at)
            print(sql)
            sql_list.append(sql)
        return sql_list
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
def get_file_list(url):
    dirs = os.listdir(url)
    file_list = []
    for file in dirs:
        ffile = url + '\\' + file

        file_list.append(ffile)
    return file_list

if __name__ == '__main__':


    dict = {'本科提前批': 10601, '本科提前一批': 10602, '本科提前二批': 10603, '本科一批': 10604, '本科二批': 10605, '本科三批': 10606, '本科批': 10607,
            '本科提前批A段': 10608, '本科提前批B段': 10609, '本科提前批C段': 10610, '本科批A段': 10611, '本科批B段': 10612, '本科一批A段': 10613,
            '本科一批B段': 10614, '本科二批A段': 10615, '本科二批B段': 10616, '本科二批C段': 10617, '本科三批A段': 10618, '本科提前批自主招生': 10619,
            '本科第一批专项': 10620, '本科第一批预科': 10621, '本科第二批预科A': 10622, '本科第二批预科B': 10623, '本科二批预科A类': 10624,
            '本科二批预科B类': 10625, '本科一批预科班': 10626, '本科二批预科班': 10627, '本科二批及预科班': 10628, '本科普通批A': 10629, '本科普通批B': 10630,
            '本科“专项生”批': 10631, '本科一批A1段': 10632, '本科一批H段（特殊类型招生批）': 10633, '本科一批I段': 10634, '本科一批J段': 10635,
            '本科一批K段': 10636, '本科一批L段': 10637, '本科一批M段': 10638, '本科一批N段': 10639, '本科甲批': 10640, '本科乙批': 10641,
            '本科综合评价批': 10642, '本科零批': 10643, '单设本科批次': 10644, '专科提前批': 10645, '专科一批': 10646, '专科二批': 10647,
            '专科批': 10648, '专科批A段': 10649, '专科批B段': 10650, '专科预科班': 10651, '高职（专科）批P段': 10652, '高职（专科）批Q段': 10653,
            '高职（专科）批R段': 10654, '高职（专科）批S段': 10655, '专项批': 10656, '专项计划批': 10657, '国家专项计划批': 10658, '国家专项计划本科批': 10659,
            '国家专项计划本科一批': 10660, '国家专项计划本科二批': 10661, '地方专项计划本科批': 10662, '地方专项计划本科一批': 10663, '地方专项计划本科二批': 10664,
            '地方农村专项计划本科批': 10665, '地方专项计划批': 10666, '农村专项计划批': 10667, '精准脱贫专项计划本科批': 10668, '精准脱贫专项计划（本科）': 10669,
            '精准脱贫专项计划（专科）': 10670, '贫困专项、南疆单列、对口援疆计划本科一批': 10671, '贫困专项、南疆单列、对口援疆计划本科二批': 10672, '提前批专项计划': 10673,
            '国家专项批': 10674, '地方专项批': 10675, '提前专项批': 10676, '高校专项批': 10677, '专项计划本科一批（贫困专项、南疆单列、对口援疆计划本科一批次）': 10678,
            '专项计划本科二批（贫困专项、南疆单列、对口援疆计划本科二批次）': 10679, '普通类提前批': 10680, '普通类平行录取段': 10681, '平行录取一段': 10682,
            '平行录取二段': 10683, '平行录取三段': 10684, '自主招生批': 10685, '免费师范生批': 10686, '特殊类批': 10687, '无批次': 10688,
            '上海海关学院': 10689, '特殊类型招生批': 10690, '本一特殊类型招生批': 10691, '本二特殊类型招生批': 10692, '省内预科': 10693,
            '艺术本科第一批专项': 10694}
    dict1={'音乐类': '10522', '蒙授艺术': '10516', '蒙授理科': '10515', '蒙授文科': '10514', '蒙授体育': '10517',
           '艺术类': '10506', '艺术理': '10505', '艺术文': '10504', '舞蹈类': '10524', '美术类': '10523',
           '美术理': '10529', '美术文': '10528', '综合': '10503', '理科': '10502', '理工（藏文）': '10518',
           '理工（蒙文）': '10520', '民语言艺术类': '10512', '民语言理科': '10511', '民语言文科': '10510',
           '民语言体育类': '10513', '文科': '10501', '文史（藏文）': '10519', '文史（蒙文）': '10521', '广播电视编导类': '10525',
           '声乐类': '10526', '器乐类': '10527', '体育类': '10509', '体育理': '10508', '体育文': '10507'}

    # for i in range(20,)
    # url = r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\school\{}\special\2019\{}.json"
    # url = url.format(i)
    #
    # sql = run(url)
    #
    # execute(sql)
    xx = 0
    url_list = [r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2017\{}",r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2018\{}",r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2019\{}"]
    # url_list=[r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2019\{}"]
    for url in url_list:
        for i in range(30,3425):

                try:
                    file1 = get_file_list(url.format(i))
                except:
                    continue
                for i in file1:
                    file2 = get_file_list(i)
                    for j in file2:
                        file3 = get_file_list(j)
                        for k in file3:
                            file4 = get_file_list(k)
                            for n in file4:
                                print(n)
                                year = url.split("\\")[-2]
                                kelei_id = n.split("\\")[-3]


                                try:

                                    sql_list = run(n,year,kelei_id)
                                    (execute(sql) for sql in sql_list)
                                except:
                                    continue

    print(xx)
    #
    # print(get_id(307))
    # print(get_specialsId("哲学"))
    # print(get_provinceId(12))
        # url = r"http://of.1zy.me/static-data.eol.cn/www/school/{}/news/68007/5263.json".format(105)
        # print(url)
        #
        # dirs = os.listdir(url)
        # # except:
        # #     continue
        # for file in dirs:
        #
        #     ffile =url+ '\\' +file
        #     print(ffile)
        #     dirs = os.listdir(ffile)
        #     for file1 in dirs:
        #         print(file1)
            # run(ffile)
            # execute(sql)
        # res = requests.get(url)
        # print(res.text.decode())
        # print(type(res.text))

        # content = res.content["title"].decode('utf-8')
        #
        #
        # print(content)
