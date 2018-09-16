import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import lxml.etree
import time
import random
#urls = "https://www.meituri.com/s/%d/"%index

def getTree(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36","Host": "www.meituri.com"}
    try:
        r=requests.get(url, timeout=5,headers = headers, verify = False)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        tree=lxml.etree.HTML(r.text)
        return tree
    except Exception as e:
        raise Exception("404",e)
        return None
index = 1
while True:
    urlx = "https://www.meituri.com/x/%d/"%index
    try:
        tree=getTree(urlx)
        content=tree.xpath("//div[@class='fenlei']")[0]
        title=content.xpath("h1")[0].xpath("string(.)")
        detail=content.xpath("p")[0].xpath("string(.)")
        detail=detail.replace("\n"," ")
        print(index,urlx,title,detail,sep="@",end="\n")
    except Exception as e:
        print(e)
        break
    index+=1
    time.sleep(random.randint(1,3))

print("++++++++++++++")
index = 9
while True:
    urls = "https://www.meituri.com/s/%d/"%index
    try:
        tree=getTree(urls)
        content=tree.xpath("//div[@class='fenlei']")[0]
        title=content.xpath("h1")[0].xpath("string(.)")
        detail=content.xpath("p")[0].xpath("string(.)")
        print(index,urls,title,detail,sep="@",end="\n")
    except Exception as e:
        print(e)
        break
    index+=1
    time.sleep(random.randint(2,4))

"""
url = "https://www.meituri.com/x/1/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36","Host": "www.meituri.com"}
r=requests.get(url, timeout=5,headers = headers, verify = False)
print(r.status_code)
print(len(r.text))"""