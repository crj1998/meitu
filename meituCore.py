import os
import requests
import lxml.etree
from PyQt5.QtCore import QThread, pyqtSignal
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import logging
 
class meituInfoThread(QThread):
    download_info_signal = pyqtSignal(str)
    download_error_signal = pyqtSignal(int)
    @staticmethod
    def getTree(url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
        try:
            r=requests.get(url, timeout=5,headers = headers, verify = False)
            r.raise_for_status()
            r.encoding=r.apparent_encoding
            tree=lxml.etree.HTML(r.text)
            logging.info("Successed to getTree @ %s"%url)
            return tree
        except Exception as e:
            logging.warning("Failed to getTree @ %s for %s"%(url,e))
            return None

    def __init__(self,start_url):
        super().__init__()
        self.start_url = start_url
        self.title = None
        self.imgdict = {}
        self.maxpage = ""
        self.nextpage = ""

    def startPage(self):
        tree = self.getTree(self.start_url)
        if tree is not None:
            self.title = tree.xpath("//title")[0].xpath("string(.)")
            content = tree.xpath("//div[@class='content']")[0]
            imglist = []
            for img in content.xpath("img"):
                imglist.append(img.get("src"))
            self.imgdict[self.start_url] = imglist
            content = tree.xpath("//div[@id='pages']")[0]
            self.nextpage = content.xpath("a")[-1].get("href")
            self.maxpage = content.xpath('a')[-2].get("href")
            del imglist,content
            logging.info("Successd to start @ %s"%self.start_url)
        else:
            logging.warning("Tree is None")
            raise Exception("Not Valid URL")

    def nextPage(self):
        while self.nextpage != self.maxpage:
            tree = self.getTree(self.nextpage)
            if tree is not None:
                content = tree.xpath("//div[@class='content']")[0]
                imglist = []
                for img in content.xpath("img"):
                    imglist.append(img.get("src"))
                self.imgdict[self.nextpage] = imglist
                content = tree.xpath("//div[@id='pages']")[0]
                self.nextpage = content.xpath("a")[-1].get("href")
                logging.info("Successd to start @ %s"%self.nextpage)
                del imglist,content
            else:
                logging.warning("Tree is None")
                raise Exception("Not Valid URL")
        else:
            tree = self.getTree(self.nextpage)
            if tree is not None:
                content = tree.xpath("//div[@class='content']")[0]
                imglist = []
                for img in content.xpath("img"):
                    imglist.append(img.get("src"))
                self.imgdict[self.nextpage] = imglist
                logging.info("Successd to start @ %s"%self.nextpage)
                del imglist,content
            else:
                logging.warning("Tree is None")
                raise Exception("Not Valid URL")

    def sendInfo(self):
        page = list(self.imgdict.values())[-1][-1]
        page = page.split("/")[-1][:-4]
        self.download_info_signal.emit("%s,%s"%(self.title, page))

    def getData(self):
        return (self.title, self.imgdict)

    def run(self):
        try:
            self.startPage()
            self.nextPage()
            self.sendInfo()
            self.exit(1)
        except Exception as e:
            logging.error("Wrong @ class meituInfoThread func run for %s"%e)
            self.download_error_signal.emit(404)


class meituDownThread(QThread):
    download_process_signal = pyqtSignal(int)

    def __init__(self, root, filedata):
        super().__init__()
        self.filename = filedata[0]
        self.imgdict = filedata[1]
        self.__root = os.path.join(root,"Picture")

    def savePic(self, referer, url):
        headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36","Referer": "https://www.meituri.com/a/10068/"}
        path=os.path.join(self.__root,url.split('/')[-1])
        try:
            if not os.path.exists(self.__root):
                os.mkdir(self.__root)
            if not os.path.exists(path):
                r=requests.get(url, headers=headers)
                with open(path,'wb') as f:
                    f.write(r.content)
                    f.close()
                    logging.info("Picture @ %s saved Successfully!(Referer: %s)"%(url,referer))
            else:
                logging.warning("File %s Existed"%path)
        except Exception as e:
            logging.warning("Picture @ %s Failed!(Referer: %s) for %s"%(url,referer,e))

    def run(self):
        try:
            process = 0
            if not os.path.exists(self.__root):
                os.mkdir(self.__root)
            self.__root = os.path.join(self.__root,self.filename)
            for r,urls in self.imgdict.items():
                for url in urls:
                    process += 1
                    self.savePic(r,url)
                    self.download_process_signal.emit(process)
            self.exit(1)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    url="https://www.meituri.com/a/19250/"
    p = meituScrapy(url)
    p.saveAllPics()