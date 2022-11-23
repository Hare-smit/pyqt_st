import datetime
import hashlib
import re
import os
import json
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor
# import win32con
# from win32process import SuspendThread, ResumeThread
from PyQt5 import uic,QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication

cookie = ""
dicts = {}
class MyThread(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        global dicts,cookie
        tt = Request_main()
        tt.mains(dicts,cookie)


class MainWindow(QWidget):
    my_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cookie = ""
        self.dicts = {}

    def init_ui(self):
        self.ui =uic.loadUi("./etao.ui")
        # print(self.ui.__dict__)
        self.cookie_inp = self.ui.lineEdit_3
        self.search_inp = self.ui.lineEdit
        self.max_inp = self.ui.lineEdit_2
        self.min_inp = self.ui.lineEdit_4
        self.email = self.ui.pushButton_4
        self.timesl = self.ui.lineEdit_6
        self.mianyou = self.ui.radioButton
        self.tianmao = self.ui.radioButton_2
        self.xiaobao = self.ui.radioButton_3
        self.zhengbao = self.ui.radioButton_4
        self.qitui = self.ui.radioButton_5
        self.daofu = self.ui.radioButton_6
        self.affirm_p = self.ui.pushButton_3
        self.start_p = self.ui.pushButton
        self.end_p = self.ui.pushButton_2
        self.cleans = self.ui.pushButton_5
        self.Text_in = self.ui.textEdit

#绑定信号
        self.affirm_p.clicked.connect(self.get_data)
        self.start_p.clicked.connect(self.click_start)
        self.cleans.clicked.connect(self.clean)
        self.end_p.clicked.connect(self.restart)
        self.email.clicked.connect(self.email_click)

    def email_click(self):
        dialog = EmailDialog()
        dialog.setWindowModality(Qt.ApplicationModal)   #启动额外窗口
        dialog.exec_()


    def restart(self):
        Request_main.exits()
    def clean(self):
        self.cookie_inp.clear()
        self.search_inp.clear()
        self.max_inp.clear()
        self.min_inp.clear()
        self.timesl.clear()
        self.mianyou.setChecked(False)
        self.tianmao.setChecked(False)
        self.xiaobao.setChecked(False)
        self.zhengbao.setChecked(False)
        self.qitui.setChecked(False)
        self.daofu.setChecked(False)
        self.Text_in.clear()

    def get_data(self):
        global dicts,cookie
        cookie = self.cookie_inp.text()
        keywords = self.search_inp.text().split(",")
        maxprice = self.max_inp.text()
        minprice = self.min_inp.text()
        timesleep = self.timesl.text()
        li = []
        if self.mianyou.isChecked():
            li.append("100")
        if self.tianmao.isChecked():
            li.append("105")
        if self.xiaobao.isChecked():
            li.append("110")
        if self.zhengbao.isChecked():
            li.append("115")
        if self.qitui.isChecked():
            li.append("120")
        if self.daofu.isChecked():
            li.append("125")
        types = ",".join(li)
        if cookie=="" or keywords==[] or maxprice=="" or minprice==""or timesleep=="":
            self.Text_in.setHtml("<h3 style = 'color:red'> 信息缺漏未填写完整<h3>")
        else:
            self.Text_in.setHtml(f'已加入参数cookie:{cookie[:50]+"..."}<br>搜索词语：{keywords},最高价格：{maxprice},最低价格：{minprice},选项：{types},间隔时间{timesleep}<br>点击开始即可运行')
            dicts = {"keywords":keywords, "maxprice":maxprice, "minprice":minprice, "types":types,"timesleep":timesleep}

    def click_start(self):
        print(cookie)
        if cookie:
            self.Text_in.setHtml("开始爬取中")
            self.my_thread = MyThread()  # 创建线程
            self.my_thread.start()  # 开始线程
        else:
            self.Text_in.setHtml("<h3 style = 'color:red'>请填写信息，填写后点击确认<h3>")

################################################################
#解析程序
class Request_main():
    def __init__(self):
        self.product = {}
        self.allnum = set()
        self.newpro = []
        self.all = 0

    def get_md5(self,str):
        md5 = hashlib.md5()
        md5.update(str.encode('utf-8'))
        return md5.hexdigest()


    def get_contents(self,dicts,cookie):
        #global product  #全局定义产品，以便没次请求完后对比得知新内容
        def callback(str):
            return str
    #模拟请求通讯
        sessions = requests.Session()
        sessions.headers.update({"authority": "h5api.m.etao.com",
                                 "method": "GET",
                                 "scheme": "https",
                                 "accept": "*/*",
                                 "accept-encoding": "gzip, deflate, br",
                                 "accept-language": "zh-CN,zh;q=0.9",
                                 "cookie": cookie,
                                 "referer": "https://www.etao.com/",
                                 "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                                 "sec-ch-ua-mobile": "?0",
                                 "sec-ch-ua-platform": '"macOS"',
                                 "sec-fetch-dest": "script",
                                 "sec-fetch-mode": "no-cors",
                                 "sec-fetch-site": "same-site",
                                 "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
                                 })
    #获取参数
        se = dicts["se"]
        keyword = dicts["keyword"]
        maxprice = dicts["maxprice"]
        minprice = dicts["minprice"]
        types = dicts["types"]
    #传入方法
        data = f'{{ "s": {se},"n":99,"q":"{keyword}","needEncode":false,"sort":"default","maxPrice":{maxprice},"minPrice":{minprice},"serviceList":"{types}","navigator":"all","urlType":2}}'
        re_way = re.compile("_m_h5_tk=(?P<tok>.*?)_",re.S)
        token =re_way.search(cookie).group("tok")
        t = str(int(time.time() * 1000))    #时间戳
        appkey = "12574478" #固定
        sign = self.get_md5(token + '&' + t + "&" + appkey + '&' + data) #sign方法
        # print(t,token,sign)
    #请求参数
        params = {
            "jsv":"2.4.16,",
            "appKey":appkey,
            "t":t,
            "sign":sign,
            "api":"mtop.etao.fe.search",
            "v":"1.0",
            "AntiCreep":"true",
            "AntiFlood":"true",
            "type":"jsonp",
            "dataType":"jsonp",
            "data":data,
        }
        url = "https://h5api.m.etao.com/h5/mtop.etao.fe.search/1.0/"
        tt = eval(sessions.get(url,params=params).text)
        data_dict = tt["data"]["items"]
        print("发起了请求")
        return data_dict

    #解析获取到的字典
    def resolver(self,data):
        for item in data:
            # reback = item["data"].get('display_rebate', "")
            # sales = item["data"].get("display_sales", "")
            title = item["data"].get("name", "")
            id = item["data"].get("nid", "")
            price = item["data"].get("source_price", "")
            url = item["data"].get("src", "")
            # img = "http:" + item["data"].get("img", "")
            item_set = (title,price,url)#(img, title, price, reback, sales, url)
            if id in self.allnum:
                pass
            else:
                self.allnum.add(id)
                self.product[id] = item_set
                if self.all:
                    self.newpro.append(id)
        return self.newpro

    def send_emails(self):
        table = '<html><table border="1" cellpadding="0" cellspacing="2" width="100%">'
        table = table + '<thead><th>优惠券名称</th><th>价格</th><th>链接</th><th>采集时间</th></tr></thead>'#'<thead><tr><th>图片</th><th>优惠券名称</th><th>价格</th><th>返利</th><th>销量</th><th>链接</th><th>采集时间</th></tr></thead>'
        crawled_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st = "<tbody>"
        for id in self.newpro:
            pro_id = self.product[id]
            st += "<tr>"
            for i in range(len(pro_id)):
                st += f"<td>{pro_id[i]}</td>"
            st += f"<td>{crawled_time}</td></tr>"
        table = table + st + '</tbody></table></html>'
        from send_email import email_sen
        with open("db/email.json", "r") as f:
            email_dict = json.load(f)
            print(email_dict)
        email_sen(table, email_dict["from"], email_dict["to"], email_dict["smtp"], email_dict["pwd"])
        self.newpro = []

    def mains(self,data,cookie):
        try:
            keywords = data.get("keywords","优惠券")
            maxprice = data.get("maxprice","10000")
            minprice = data.get("minprice","0")
            types = data.get("types","105")
            timesleep = data.get("timesleep",5)

            while True:
                cookie = cookie
                keywords = keywords
                maxprice = maxprice
                minprice = minprice
                types = types
                timesleep = timesleep
                for keyword in keywords:
                    for i in range(100):
                        se = i * 99
                        datas = {"se": se, "keyword": keyword, "maxprice": maxprice, "minprice": minprice,
                                 "types": types}
                        data = self.get_contents(datas, cookie)
                        if data == []:
                            print("已是全部商品")
                            print(len(self.product))
                            break
                        self.newpro = self.resolver(data)
                self.all = 1
                print(self.newpro)
                if self.newpro:
                    print("有新的了")
                    self.send_emails()
                time.sleep(int(timesleep))
                print("监测ing")
        except:
            print("请求失败，信息未填写或cookie已失效")


    def exits(self):
        sys.exit(1)



################################################################
#邮箱窗体

from PyQt5.QtWidgets import QVBoxLayout, QDialog, QPushButton, QLabel, QLineEdit, QMessageBox, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt
EMAIL_FOLDER_PATH = os.path.join("db")
EMAIL_FILE_PATH = os.path.join("db", 'email.json')
class EmailDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filed_dict = {}
        self.init_filed_dict()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("邮箱配置")
        self.resize(300, 270)

        layout = QVBoxLayout()

        form_data_list = [
            {"title": "SMTP服务器:", "field": "smtp"},
            {"title": "发件箱:", "field": "from"},
            {"title": "密码:", "field": "pwd"},
            {"title": "收件人（多个用逗号分隔）:", "field": "to"},
        ]

        for item in form_data_list:
            layout.addWidget(QLabel(item['title']))

            field = item['field']
            txt = QLineEdit()
            if field in self.filed_dict:
                txt.setText(self.filed_dict[field])
            layout.addWidget(txt)

            self.filed_dict[field] = txt

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.event_save_click)
        layout.addWidget(btn_save, 0, Qt.AlignRight)

        self.setLayout(layout)

    def event_save_click(self):
        # 1.获取输入值
        info = {}
        for filed, obj in self.filed_dict.items():
            info[filed] = obj.text().strip()

        # 2.保存
        if not os.path.exists(EMAIL_FOLDER_PATH):
            os.makedirs(EMAIL_FOLDER_PATH)

        with open(EMAIL_FILE_PATH, mode='w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False)

        # 3.关闭窗口
        self.close()

    def init_filed_dict(self):
        if not os.path.exists(EMAIL_FILE_PATH):
            return
        with open(EMAIL_FILE_PATH, mode='r', encoding='utf-8') as f:
            self.filed_dict = json.load(f)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    # 展示窗口
    w.ui.show()
    app.exec()