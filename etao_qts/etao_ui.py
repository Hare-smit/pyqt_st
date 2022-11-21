import hashlib
import re
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor
# import win32con
# from win32process import SuspendThread, ResumeThread
from PyQt5 import uic,QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication

dicts = {}
cookie = ""
class MyThread(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        global dicts,cookie
        main(dicts,cookie)

class MainWindow(QWidget):
    my_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.init_ui()

    def printf(self,str):
        self.Text_in.setHtml(str)

    def init_ui(self):
        self.ui =uic.loadUi("./etao.ui")
        # print(self.ui.__dict__)
        self.cookie_inp = self.ui.lineEdit_3
        self.search_inp = self.ui.lineEdit
        self.max_inp = self.ui.lineEdit_2
        self.min_inp = self.ui.lineEdit_4
        self.email = self.ui.lineEdit_5
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

    def restart(self):
        exits()
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
        self.Text_in.setHtml(f'已加入参数cookie:{cookie[:10]+"..."}<br>搜索词语：{keywords},最高价格：{maxprice},最低价格：{minprice},选项：{types},间隔时间{timesleep}<br>点击开始即可运行')
        dicts = {"keywords":keywords, "maxprice":maxprice, "minprice":minprice, "types":types,"timesleep":timesleep}

    def click_start(self):
        self.my_thread = MyThread()  # 创建线程
        self.my_thread.start()  # 开始线程

################################################################
#解析程序


def get_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


product = {}
allnum = set()
newpro = []
all = 0
def get_contents(dicts,cookie):
    global product  #全局定义产品，以便没次请求完后对比得知新内容
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
    sign = get_md5(token + '&' + t + "&" + appkey + '&' + data) #sign方法
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
def resolver(data):
    global product,newpro,all
    for item in data:
        reback = item["data"].get('display_rebate', "")
        sales = item["data"].get("display_sales", "")
        title = item["data"].get("name", "")
        id = item["data"].get("nid", "")
        price = item["data"].get("source_price", "")
        url = item["data"].get("src", "")
        img = "http:" + item["data"].get("img", "")
        item_set = (img, title, price, reback, sales, url)
        if id in allnum:
            pass
        else:
            allnum.add(id)
            product[id] = item_set
            if all:
                newpro.append(id)
    return newpro

def main(data,cookie):
    global product,newpro,all
    try:
        keywords = data.get("keywords","优惠券")
        maxprice = data.get("maxprice","10000")
        minprice = data.get("minprice","0")
        types = data.get("types","105")
        timesleep = data.get("timesleep",5)
        def run(keyword):
            for i in range(100):
                se =i*99
                dicts = {"se": se, "keyword": keyword, "maxprice": maxprice, "minprice": minprice, "types": types}
                data = get_contents(dicts,cookie)
                if data == []:
                    print("已是全部商品")
                    print(len(product))
                    break
                newpro = resolver(data)
        while True:
            cookie = cookie
            keywords = keywords
            maxprice = maxprice
            minprice = minprice
            types = types
            timesleep = timesleep
            for keyword in keywords:
                run(keyword)
            all = 1
            if newpro:
                print("有新的了")
                for id in newpro:
                    print(product[id])
                newpro = []
            time.sleep(int(timesleep))
            print("开始监测")
    except:

        tt = MainWindow()
        tt.printf("请求失败，信息未填写或cookie已失效")
        print("请求失败，信息未填写或cookie已失效")






def exits():
    sys.exit(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    # 展示窗口
    w.ui.show()
    app.exec()