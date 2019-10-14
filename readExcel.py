import xlrd
import pymysql


# import importlib
# importlib.reload(sys) #出现呢reload错误使用

#
def open_excel():
    try:
        book = xlrd.open_workbook(r"C:\Users\Administrator\Documents\Tencent Files\624912911\FileRecv\2021年（3+1+2模式）8省数据统计(0910第一版).xlsx")  # 文件名，把文件与py文件放在同一目录下
    except:
        print("open excel file failed!")
    try:
        sheet = book.sheet_by_name("sheet名称")  # execl里面的worksheet1
        return sheet
    except:
        print("locate worksheet in excel failed!")


if __name__ == '__main__':
    sheet = open_excel()

    for i in range(1, sheet.nrows):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1

        name = sheet.cell(i, 0).value  # 取第i行第0列
        data = sheet.cell(i, 1).value  # 取第i行第1列，下面依次类推
        print(name)
        print(data)
        value = (name, data)
        print(value)

#
#
# # 连接数据库
# try:
#     db = pymysql.connect(host="127.0.0.1", user="root",
#                          passwd="XXX",
#                          db="XXX",
#                          charset='utf8')
# except:
#     print("could not connect to mysql server")
#
#
# def search_count():
#     cursor = db.cursor()
#     select = "select count(id) from XXXX"  # 获取表中xxxxx记录数
#     cursor.execute(select)  # 执行sql语句
#     line_count = cursor.fetchone()
#     print(line_count[0])
#
#
# def insert_deta():
#     sheet = open_excel()
#     cursor = db.cursor()
#     for i in range(1, sheet.nrows):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
#
#         name = sheet.cell(i, 0).value  # 取第i行第0列
#         data = sheet.cell(i, 1).value  # 取第i行第1列，下面依次类推
#         print(name)
#         print(data)
#         value = (name, data)
#         print(value)
#         sql = "INSERT INTO XXX(name,data)VALUES(%s,%s)"
#         cursor.execute(sql, value)  # 执行sql语句
#         db.commit()
#     cursor.close()  # 关闭连接
#
#
# insert_deta()
#
# db.close()  # 关闭数据
# print("ok ")