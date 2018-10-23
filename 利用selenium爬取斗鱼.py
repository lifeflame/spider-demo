"""
目的：利用selenium爬取斗鱼上的内容
思路：
获取页面的源码
利用xpath获取类别，房间号，人气值
"""
from selenium import webdriver
import time
from lxml import etree

class Douyu():
    def setup(self):
        self.url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()

    def doyu(self):
        self.driver.get(self.url)
        time.sleep(3)
        tree = etree.HTML(self.driver.page_source)
        infoes = tree.xpath('//*[@id="live-list-contentbox"]/li')
        for info in infoes:
            cate = info.xpath('.//span[@class="tag ellipsis"]/text()')[0]
            anchor = info.xpath('./a/div/p/span[1]/text()')[0]
            number = info.xpath('./a/div/p/span[2]/text()')[0]
            print("类别：%s ;主播：%s ;人气：%s ." % (cate,anchor,number))

    def destr(self):
        self.driver.quit()
if __name__ == '__main__':
    douyu =Douyu()
    douyu.setup()
    douyu.doyu()
    douyu.destr()

