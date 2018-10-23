import requests
from lxml import etree
import csv
import os


class Lianjia():
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

    def all_page_url(self, url):
        for i in range(1, 101):   #生成100页
            page_url = url + "pg" + str(i)    #这就生成了100页的url地址
            print("开始下载第%d"%i)
            self.one_page(page_url)
        print("Done")

    def request(self, page_url):
        content = requests.get(page_url,headers=self.headers)
        return content

    def one_page(self, page_url):
        page_html = self.request(page_url)
        selector = etree.HTML(page_html.text)  #解析网页
        houseinfoes = selector.xpath("//li[@class='clear LOGCLICKDATA']")#提取所有的li标签
        d = {}
        for each in houseinfoes:
            d["name"] = each.xpath(".//div[@class='houseInfo']/a/text()")[0]
            d["price"] = each.xpath('.//div[@class="totalPrice"]/span/text()')[0]
        self.save(d)

    def save(self,d):

        path = "D:\数据分析\草稿\测试"  # 指定电脑里面的一个路径
        os.chdir(path)  # 切换工作路径为指定的path
        with open("lian1.csv", "a",newline="") as file:  # 需要设置newline,否则csv文件中会出现空行
            mywriter = csv.writer(file)
            for k in d:
                mywriter.writerow([k, d[k]])  # 将指定信息逐行写入csv文件中

lianjia = Lianjia()
lianjia.all_page_url("https://bj.lianjia.com/ershoufang/")