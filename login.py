import requests

loginsave_url="http://www.tujidao.com/u/?action=loginsave"
tujidao_session=requests.Session()
#r=tujidao_session.get(login_url,timeout=10)
head={"Host": "www.tujidao.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Origin": "http://www.tujidao.com",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer": "http://www.tujidao.com/u/?",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"}
cookie_dict={"Cookie": "ASPSESSIONIDSSRRRTAB=GMDIJOGACJFNGEBLMCEIOBKN; UM_distinctid=1658f34b5ad0-01e2c0dde1a5f9-9393265-e1000-1658f34b5ae1b6; 7Dw1Tw3Bh2Mvfr=; CNZZDATA1257039673=1119229636-1535704471-null%7C1535787510; 7Dw1Tw3Bh2Mvu%5Fusername=; 7Dw1Tw3Bh2Mvu%5Fpw=; 7Dw1Tw3Bh2Mvu%5Fleixing=; 7Dw1Tw3Bh2Mvu%5Fid="}
postdata={"t0":"crjpub","t1":"pub62034092"}
#r=tujidao_session.post(loginsave_url,data=postdata,headers=head,timeout=10)
#r=tujidao_session.get("http://www.tujidao.com/u/?")
#r.encoding=r.apparent_encoding
#print(r.text)

 


import time
import requests

def testIP(ip):
    ip_url = "http://ip.42.pl/raw"
    proxy = {'https': ip}
    r=requests.get(ip_url, proxies=proxy)
    print(r.text)
    if ip.split(":")==r.text.split():
        return True
    else:
        return False

testIP("121.232.194.119:9000")


