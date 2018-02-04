# -*-encoding:utf8-*-
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import pymysql.cursors

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'UTF-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

if __name__ == "__main__":
    # pdf폴더에있느걸 모두변환하여 txt폴더에
    folder_root = os.getcwd() + "/pdf/"
    txt_root = os.getcwd() + "/txt/"
    filelist = os.listdir(folder_root)
    # pdf to txt
    for idx in range(len(filelist)):
        if  filelist[idx].split('.')[1]=='pdf':
            txt = convert_pdf_to_txt(folder_root + filelist[idx])
            text_file = open(txt_root + filelist[idx].split('.')[0] + '.txt', "w")
            text_file.write(txt)
            text_file.close()
    # txt parsing
    txtlist = os.listdir(txt_root)
    for idx in range(len(filelist)):
        with open(txt_root + txtlist[idx], 'r') as f:
            read_data = f.readlines()
            # 제출일 8 , 발명국문 10, 발명영문 12, 출원인성명코드 14,15 줄에있음
            # 아니면 정규표현식으로 추출하는 방법도있는데 특허출원서 양식이
            # 동일해서 대부분 이경우에서 걸린다.
            date = read_data[8].strip()
            korName = read_data[10].strip()
            engName = read_data[12].strip()
            name = read_data[14].strip()
            code = read_data[15].strip()
            print date,korName,engName,name,code
            # 이런식으로 데이터를 추출해서
            # 아래 코드를 이용 DB에 넣으면된다
            # 위치는 프로그램 특성에따라 조절
            # Connect to the database
            """
            connection = pymysql.connect(host='localhost',
                                         user='user',
                                         password='passwd',
                                         db='db',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO `특허` (`email`, `password`) VALUES (%s, %s)"
                    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                    cursor.execute(sql, ('webmaster@python.org',))
                    result = cursor.fetchone()
                    print(result)
            finally:
                connection.close()
            """





