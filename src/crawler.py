import requests
from bs4 import BeautifulSoup
import os
import re
import json


class FGOCrawler:

    def __init__(self, dest):
        # dest is the root directory of download data
        self.dest = dest
        self.header = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Referer": "http://fgowiki.com/guide/petdetail/"
        }
        self.servantlist = []

    def crawl_servant(self):
        self.crawl_servant_name()
        # TODO crawl servant detail
        # TODO make this task parallel, it's too slow now
        idx = 1
        for name in self.servantlist:
            # crawl servant images
            for srctype in "ABCDE":
                self.crawl_servant_img(idx, srctype, self.dest + "/" + name + "/img/")
                #return
            # crawl noble phantasm video
            # self.crawl_noble_phantasm_video(idx, self.dest + "/" + name + "/video/")
            idx += 1

    def crawl_servant_name(self, baseurl="https://fgowiki.com/guide/petdetail/"):
        response = requests.get(baseurl, headers=self.header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, "html.parser")
        servants = soup.find('select', class_='pet').find_all('option')
        for servant in servants[1:]:
            self.servantlist.append(str(servant.get_text()))
        for servant in self.servantlist:
            self.checkdir(servant)

    def checkdir(self, servant):
        """ before crawling, first check the dest directory """
        dest = self.dest
        if not os.path.exists(dest):
            os.mkdir(dest)

        svdest = dest + "/" + servant
        print(svdest)
        if not os.path.exists(svdest):
            os.mkdir(svdest)
        imgdest = svdest + "/img"
        if not os.path.exists(imgdest):
            os.mkdir(imgdest)
        videodest = svdest + "/video"
        if not os.path.exists(videodest):
            os.mkdir(videodest)

    def crawl_servant_img(self, idx, srctype, dest, baseurl="https://img.fgowiki.com/fgo/card/servant/"):
        """
        :param idx: indicates the servant id
        :param srctype:
        [A - 1
         B - 2
         C - 3
         D - 4
         E - Fool's day]
        :param dest: dest directory
        :param baseurl: "https://img.fgowiki.com/fgo/card/servant/"
        :return:
        """
        # invalid index
        if idx <= 0:
            return
        url = baseurl + ("00" + str(idx))[-3:] + srctype + ".jpg"
        print(url)
        response = requests.get(url, headers=self.header)
        destfolder = dest + ("00" + str(idx))[-3:] + "_" + srctype + ".jpg"
        print(destfolder)
        f = open(destfolder, 'wb')
        f.write(response.content)
        f.close()

    def crawl_noble_phantasm_video(self, idx, dest, baseurl="https://img.fgowiki.com/fgo/mp4/"):
        """
        :param idx: indicates the servant id
        :param dest: dest directory
        :param baseurl: "https://img.fgowiki.com/fgo/mp4/"
        :return:
        """
        # invalid index
        if idx <= 0:
            return
        url = baseurl + "No." + ("00" + str(idx))[-3:] + ".mp4"
        print(url)
        response = requests.get(url, headers=self.header)
        f = open(dest + "No." + ("00" + str(idx))[-3:] + "_" + ".mp4", 'wb')
        f.write(response.content)
        f.close()

    def crawl_equip_img(self, idx, srctype, dest, baseurl="https://img.fgowiki.com/fgo/card/equip/"):
        """
        :param idx: indicates the equip card id
        :param srctype: currently should always be "A"
        :param dest: dest directory
        :param baseurl: "https://img.fgowiki.com/fgo/card/equip/"
        :return:
        """
        # invalid index
        if idx <= 0:
            return
        url = baseurl + ("00" + str(idx))[-3:] + srctype + ".jpg"
        print(url)
        response = requests.get(url, headers=self.header)
        f = open(dest + ("00" + str(idx))[-3:] + "_" + srctype + ".jpg", 'wb')
        f.write(response.content)
        f.close()

    def crawl_equip(self, idx, dest, baseurl="https://fgowiki.com/guide/equipdetail/"):
        """ crawl and save to json file

        :param idx: indicates the equip card id
        :param dest: dest directory
        :param baseurl: "https://fgowiki.com/guide/equipdetail/"
        :return:
        """
        # invalid index
        if idx <= 0:
            return
        url = baseurl + idx
        print(url)
        response = requests.get(url, headers=self.header)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script")
        pattern = re.compile("\nvar datadetail = (.*?);")
        for script in scripts:
            m = pattern.match(str(script.string))
            if m:
                equipjson = str(m.group()).split("\nvar datadetail = ")[1]
                # print(equipjson)
                jo = json.loads(equipjson[1:-2], encoding="utf-8")
                with open(dest + ".json", "w") as fp:
                    json.dump(jo, fp)


fgocrawl = FGOCrawler("/Users/kankun/Documents/pic")
fgocrawl.crawl_servant()