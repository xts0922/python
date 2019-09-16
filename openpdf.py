from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser,PDFDocument

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
#获取文档对象
fp = open("2017年天津高考成绩体育类综合分分数段情况.pdf","rb")

#创建一个与文档关联的解释器
parser = PDFParser(fp)

#PDF文档的对象
doc=PDFDocument()

#链接解释器和文档对象
parser.set_document(doc)
doc.set_parser(parser)

#初始化文档
doc.initialize("")

#创建PDF资源管理器
resource  =PDFResourceManager()

#参数分析器
laparam = LAParams()

#创建一个聚合器
device =PDFPageAggregator(resource,laparams=laparam)
#创建PDF页面解释器
interpreter =PDFPageInterpreter(resource,device)

#使用文档对象得到页面的集合
for page in doc.get_pages():

    #使用页面解释器来读取
    interpreter.process_page(page)

    #使用聚合器来获得内容
    layout =device.get_result()

    for out in layout:
        if hasattr(out,"get_text"):

            print(out.get_text())