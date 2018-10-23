# -*- coding: utf-8 -*-
import requests
import re,os
import json
from multiprocessing import Pool
from requests.exceptions import RequestException

class Maoyan():

    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}

    def get_one_page(self,url):
        try:
            response = requests.get(url,headers=self.headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None
    def page_parse(self,html):
        #re.S 作用：使.匹配包括换行符在内的所有字符
        pattern = re.compile('<dd>.*?board-index.*?>(\d+).*?data-src="(.*?)".*?<a.*?>(\w+)</a>.*?star">(.*?)'
                             '</p>.*?>(.*?)</p.*?integer">(.*?)</i>.*?fraction">(.*?)</i.*?</dd>',re.S)
        items = re.findall(pattern,html)
        for item in items:
            yield {
                "index":item[0],
                "image_url":item[1],
                "name":item[2],
                "actor":item[3].strip()[3:],
                "time":item[4][5:],
                "score":item[5]+item[6]
            }

    def write_to_file(self,content):
        os.chdir("D:\crawl picture")
        with open("maoyan.txt","a",encoding="utf-8") as file:
            file.write(json.dumps(content,ensure_ascii=False)+"\n")

    def main(self,offset):
        print("正在爬取第"+str(offset+1)+"页")
        url = "http://maoyan.com/board/4?offset="+str(offset*10)
        html = self.get_one_page(url)
        for item in self.page_parse(html):
            self.write_to_file(item)

if __name__ == '__main__':
    maoyan = Maoyan()
    #生成进程池
    pool = Pool()
    pool.map(maoyan.main,list(range(10)))






