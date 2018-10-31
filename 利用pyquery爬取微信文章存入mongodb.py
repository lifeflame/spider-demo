import requests
import pymongo
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

client = pymongo.MongoClient("localhost")
db = client["weixin"]

def get_html(keyword, page):
    base_url = "https://weixin.sogou.com/weixin?"
    params = {"query":keyword,
              "type":2,
              "page":page}
    headers = {"Cookie":"CXID=87A70B989BE9764F9D0606A0CF98A90F; SUID=953A133A4B238B0A5AF8E8EA000C93FE; SUV=007617893A133BCE5B03934DD4F9B434; ad=ec9BvZllll2bYQo0lllllVsRGIZlllll$T3j9yllll9lllllRklll5@@@@@@@@@@; IPLOC=CN4401; ABTEST=6|1540889196|v1; weixinIndexVisited=1; ppinf=5|1540890620|1542100220|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTUlODglQjklRTklODIlQTMlRTYlQjAlQjglRTYlODElOTJ8Y3J0OjEwOjE1NDA4OTA2MjB8cmVmbmljazozNjolRTUlODglQjklRTklODIlQTMlRTYlQjAlQjglRTYlODElOTJ8dXNlcmlkOjQ0Om85dDJsdURBZ1U5NGRNbVlJdjJVNVI2VEJPa29Ad2VpeGluLnNvaHUuY29tfA; pprdig=W15pNY07peWPH3nwpWOiDeIs8ni8kCgwkQVg7ZRA7eN0MJH_0Eka99HGBHT455HmTfMv2viWuaJCRoG4WBhJZ96fwRk1DzZsmHaQ9kQe4N8m5Ae3MKOONky6dlRlW4T7bpaKPclD_beYMUm9z3fut2O-mIz7HM91RPWrQhNwr9k; sgid=05-35622367-AVvYHicw33LRQuQTx4qD3oao; sct=4; JSESSIONID=aaaz1IjnM9Ja_-L8yn-Aw; PHPSESSID=mfvm9mdudk1mfhqf0r44bcq9p4; SUIR=AF7677DAE7ED9E86D1C20E57E8E78509; SNUID=2B1517BA8783FF06CF8139CD8785B9B0; ppmdig=1540972911000000454420f48e4269688233982f73738363"
                ,"Host": "weixin.sogou.com"
                ,"Upgrade-Insecure-Requests": "1"
                ,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        #params可以作为requests库重构url
        response = requests.get(base_url,params=params,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("error")
            #如果连接不上，重新发起该请求
    except ConnectionError:
        return get_html(keyword, page)


def parse_index(html):
    doc = pq(html)
    #找出所有含有具体链接的标签，items（）返回的是一个迭代器
    items = doc(".news-box .news-list .txt-box h3 a").items()
    for item in items:
        yield item.attr.href


def get_detail(url):
    #对每个url入口进行访问
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("error")
    except ConnectionError:
        return get_detail(url)


def parse_detail(html):
    doc = pq(html)
    #获取有关内容的标题，内容，日期，昵称，公众号
    title = doc("#activity-name").text()
    content = doc("#js_content").text().replace("\n", "").replace("\xa0", "")
    date = doc("#publish_time").text()
    nickname = doc("#js_name").text()
    wechat = doc("#js_profile_qrcode > div > p:nth-child(3) > span").text()
    return {"title":title,
            "content":content,
            "date":date,
            "nickname":nickname,
            "wechat":wechat}


def save_to_mongo(data):
    if db["jingyong_detail"].update({"title":data["title"]},{"$set":data},True):
        print("Saved to mongo",data["title"])
    else:
        print("Failed to save to Mongo")


def main():
    for page in range(1,100):
        html = get_html("金庸", page)
        if html:
            urls = parse_index(html)
            for url in urls:
                if url:
                    html = get_detail(url)
                    data = parse_detail(html)
                    save_to_mongo(data)


if __name__ == '__main__':
    main()
