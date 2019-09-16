
import os
from retrying import retry
import  shutil

# del_dir = r"C:\Users\Administrator\Desktop\school\{}\special"
dir = r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\school\{}"
del_dir = r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\school\{}\special\2018"
@retry
def delete_dir(del_dir):
    if(os.path.exists(del_dir)):
        shutil.rmtree(del_dir)
        os.mkdir(del_dir.format(i))
        print("移除文件：%s" % del_dir)
    else :
        print("文件不存在")

if __name__ == '__main__':

    # for i in range(1,3450):
    #     try:
    #         delete_dir(del_dir.format(i))
    #
    #     except:
    #         delete_dir(del_dir.format(i))
    for i in range(1,3450):
        if (os.path.exists(dir.format(i))):
            if (os.path.exists(del_dir.format(i))):
                pass
            else:
                print(del_dir.format(i) + "文件不存在")
                # os.mkdir(del_dir.format(i))