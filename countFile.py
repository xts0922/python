import os
def get_file_list(url):
    dirs = os.listdir(url)
    file_list = []
    for file in dirs:
        ffile = url + '\\' + file

        file_list.append(ffile)
    return file_list
a = 0
url_list = [r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2017\{}",r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2018\{}",r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2019\{}"]

# url_list = [r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\2.0\schoolplanindex\2019\{}"]
for url in url_list:
    for i in range(30, 3425):

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
                            a = a+1
                            print(a)

                        # year = url.split("\\")[-2]
                        # kelei_id = n.split("\\")[-3]
                        #
                        # try:
                        #
                        #     sql_list = run(n, year, kelei_id)
                        #     [execute(sql) for sql in sql_list]
                        # except:
                        #     continue