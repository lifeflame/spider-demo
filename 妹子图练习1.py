import requests
from bs4 import BeautifulSoup
import os


class Mzitu():

    def __init__(self):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        self.headers = headers   #定义该类的headers 属性

    def all_url(self,url):
        html = self.request(url)
        all_a = BeautifulSoup(html.text,"lxml").find("div",class_ = "all").find_all("a")
        for a in all_a:
            title = a.get_text()
            print(u"开始保存",title)
            path = str(title).replace("?","_")
            self.mkdir(path) #调用保存文件的方法
            href = a["href"]
            self.html(href)

    def request(self, url):
        content = requests.get(url,headers=self.headers)
        return content

    def mkdir(self, path):
        path = path.strip()
        final_path = os.path.join("E:\mzitu",path)
        isExists = os.path.exists(final_path)
        if not isExists:
            print(u"建了一个叫做",path,u"的文件夹")
            os.makedirs(final_path)
            os.chdir(final_path)
            return True
        else:
            print(u"名字叫做",path,u"已经存在了")
            return False

    def html(self, href):
        max_html = self.request(href)
        self.headers['referer'] = href
        max_number = BeautifulSoup(max_html.text,"lxml").find("div",class_ = "pagenavi")
        if max_number is None:
            return
        else:
            span_number = max_number.find_all("span")[-2].get_text()
            for page in range(1, int(span_number) + 1):
                span_html = href + "/" + str(page)
                self.img(span_html)

    def img(self, span_html):
        img_html = self.request(span_html)
        final_html = BeautifulSoup(img_html.text,"lxml").find("div",class_ = "main-image").find("img")["src"]
        self.save(final_html)

    def save(self, final_html):
        img = self.request(final_html)
        name = final_html[-9:-4]
        f = open(name+".jpg","ab")
        f.write(img.content)
        f.close()

meizitu = Mzitu()
meizitu.all_url("http://www.mzitu.com/all")