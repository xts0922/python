import shutil
import  os
src_dir=r"C:\Users\Administrator\Desktop\school\{}\special\2018"


target_path = r"D:\xiatian\static-data.eol.cn\static-data.eol.cn\www\school\{}\special\2018"


for i in range(1,3450):
    if (os.path.exists(src_dir.format(i))):
        print(i)
        shutil.move(src_dir.format(i),target_path.format(i))
