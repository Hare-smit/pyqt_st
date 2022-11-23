import hashlib
import re
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor
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
        print("请求失败，信息未填写或cookie已失效")
def exits():
    sys.exit(1)

if __name__ == "__main__":
    cookie = "cna=DKL4G1GW6EQCAXWIIUARHcEq; t=3f4b06ecfe911de5b09dfc2ec0e3dd17; tracknick=qq%5Cu98DE%5Cu8F66%5Cu5927%5Cu4E70%5Cu5BB6; lgc=qq%5Cu98DE%5Cu8F66%5Cu5927%5Cu4E70%5Cu5BB6; _tb_token_=7ee33643eb956; cookie2=173b5584b19e142aeeab65d3d78994a6; xlly_s=1; _m_h5_tk=e97c1e2c972480f836d92b7948734e88_1668931601464; _m_h5_tk_enc=c8f25857d01d996381fdfaafc67277bf; dnk=qq%5Cu98DE%5Cu8F66%5Cu5927%5Cu4E70%5Cu5BB6; uc1=cookie14=UoeyBrL%2Fz8siXQ%3D%3D&existShop=false&cookie21=VT5L2FSpczFp&cookie15=VT5L2FSpMGV7TQ%3D%3D; uc3=lg2=URm48syIIVrSKA%3D%3D&nk2=EuTVwBAXfYBJZrII&id2=W8CJpUPUF9nj&vt3=F8dCvjT9nF%2FOU1L3tNw%3D; _l_g_=Ug%3D%3D; uc4=nk4=0%40EJt2vbyFsaeKqVrYq3X0mkARjyqkeog%3D&id4=0%40WeNTnHMql52fGxZNe4pzYEhUrcY%3D; unb=894951437; cookie1=UonfY0HzW0fmCdBPbq0Plrbm7nSlz0W6YRYkDgbeaeU%3D; login=true; cookie17=W8CJpUPUF9nj; _nk_=qq%5Cu98DE%5Cu8F66%5Cu5927%5Cu4E70%5Cu5BB6; sgcookie=E100gOc6Z3FYQPRa107S%2B8gVA%2BXesWqU0Y82CSKJvp1rxattMS4r8tESBSsx3VaMMi6KTHWrEuBJrVdw7EGlEumYazZWVD9Hy23Nq6525X3STWEWg20CQc2Z1HZKq4q%2Ba6Tg; cancelledSubSites=empty; sg=%E5%AE%B676; csg=92fb9922; x5sec=7b226d746f703b32223a2232396266653937396631323463656162313835393737363839653463303936364350717135357347454c6d3675494f312f34583357786f4c4f446b304f5455784e444d334f7a49776b594b6c5a454144227d; l=eBQL0LKITUliqBxjBOfw-urza77tGIRfDuPzaNbMiOCPOGCycaplW6z1vX82CnhVnsEeR3o34xxwB-LLYyzshYlerO16kYD8zdTh.; tfstk=clMcB69Tjz_Q21ptPqwXdCi-wY3cZrszkVujU3vAEQXxfkHPifCPT6jDZzYBu11..; isg=BDU164c4uo32ld4OXNegPa1wRLfvsunE4S_N0bdalKzrjlSAfwJWlctI2VK4ggF8"
    keywords = ["优惠券1"]
    maxprice = 20
    minprice = 1
    types = "100,105"
    timesleep=5
    dicts = {"keywords":keywords, "maxprice":maxprice, "minprice":minprice, "types":types,"timesleep":timesleep}
    main(dicts,cookie)
