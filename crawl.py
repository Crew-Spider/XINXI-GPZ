# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
url='http://news.baidu.com/ns?word=%E4%B8%8A%E6%B5%B7%E6%B5%B7%E4%BA%8B%E5%A4%A7%E5%AD%A6&pn=0&rn=20&cl=2'
res=requests.get(url)
soup = BeautifulSoup(res.text,'html.parser')
info = soup.find_all("div", {"class": "result"})

for i in info:
    time = i.find("p").get_text().split("\xa0")[-1]
    a = i.find("a")
    title = a.get_text()
    href = a["href"]
    with open("f:/1.txt", 'a', encoding="utf-8") as f:
        f.write(href + "," + title + "," + time + "\n")


