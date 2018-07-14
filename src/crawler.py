import requests
from bs4 import BeautifulSoup
import os
import re
import json
import sys
import concurrent.futures


class FGOCrawler:

    # currently completed piece
    count = 0
    # all pieces to complete
    total = 0

    def __init__(self, dest):
        # dest is the root directory of download data
        self.dest = dest
        self.header = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Referer": "http://fgowiki.com/guide/petdetail/"
        }
        self.servantnames = []
        self.servantdict = {}

        # servant used url
        self.svdetailurl = "https://fgowiki.com/guide/petdetail/"
        self.svimgurl = "https://img.fgowiki.com/fgo/card/servant/"
        self.svvideourl = "https://img.fgowiki.com/fgo/mp4/"

        # equip used url
        self.eqdetailurl = "https://fgowiki.com/guide/equipdetail/"
        self.eqimgurl = "https://img.fgowiki.com/fgo/card/equip/"

        # # currently completed piece
        # self.count = 0
        # # all pieces to complete
        # self.total = 0

    # def crawl_servant(self):
    #     # first get all servant names
    #     self.crawl_servant_name()
    #     idx = 1
    #     for name in self.servantnames:
    #         self.crawl_servant(idx)
    #         idx += 1

    def crawl_servant(self, idx):
        if len(self.servantnames) > 0 and idx <= len(self.servantnames):
            name = self.servantnames[idx]
            for srctype in "ABCDE":
                self.crawl_servant_detail(idx, self.dest + "/" + name + "/")
                # crawl servant image
                self.crawl_servant_img(idx, srctype, self.dest + "/servant/")
                # crawl noble phantasm video
                # self.crawl_noble_phantasm_video(idx, self.dest + "/" + name + "/")

    # TODO this func is still under develop
    def crawl_servant_detail(self, idx, dest):
        return

    def crawl_servant_img(self, idx, srctype, dest):
        """
        :param idx: indicates the servant id
        :param srctype:
        [A - 1
         B - 2
         C - 3
         D - 4
         E - Fool's day]
        :param dest: dest directory
        :return:
        """
        # invalid index
        if idx <= 0:
            return
        url = self.svimgurl + ("00" + str(idx))[-3:] + srctype + ".jpg"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            destfolder = dest + self.servantdict[idx] + "/" + ("00" + str(idx))[-3:] + "_" + srctype + ".jpg"
            if not os.path.exists(destfolder):
                f = open(destfolder, 'wb')
                f.write(response.content)
                f.close()
        else:
            print("failed to crawl the image of servant " + self.servantdict[idx])

    # TODO this func is still under develop
    def crawl_noble_phantasm_video(self, idx, dest):
        """
        :param idx: indicates the servant id
        :param dest: dest directory
        :return:
        """
        # invalid index
        if idx <= 0:
            return
        url = self.svvideourl + "No." + ("00" + str(idx))[-3:] + ".mp4"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            destfile = dest + "No." + ("00" + str(idx))[-3:] + "_" + ".mp4"
            if not os.path.exists(destfile):
                f = open(destfile, 'wb')
                f.write(response.content)
                f.close()
        else:
            print("failed to crawl the video of servant " + self.servantnames[idx])

    def crawl_servant_name(self):
        response = requests.get(self.svdetailurl, headers=self.header)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, "html.parser")
            servants = soup.find('select', class_='pet').find_all('option')
            servantid = 1
            for servant in servants[1:]:
                self.servantnames.append(str(servant.get_text()))
                self.servantdict[servantid] = str(servant.get_text())
                servantid += 1
        else:
            print("failed to crawl the names of all servants. Could be Internet issue")

    def servantdir(self, servant, dest):
        """ before crawling, first check the dest directory """
        if not os.path.exists(dest):
            os.mkdir(dest)

        svdest = dest + "/" + servant
        if not os.path.exists(svdest):
            os.mkdir(svdest)
        imgdest = svdest + "/img"
        if not os.path.exists(imgdest):
            os.mkdir(imgdest)
        videodest = svdest + "/video"
        if not os.path.exists(videodest):
            os.mkdir(videodest)

    def crawl_equip_detail(self, idx, dest):
        """ crawl and save to json file

        :param idx: indicates the equip card id
        :param dest: dest directory
        :return:
        """
        # invalid index
        if idx <= 0:
            return
        url = self.eqdetailurl + str(idx)
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.content, "html.parser")
            scripts = soup.find_all("script")
            pattern = re.compile("\nvar datadetail = (.*?);")
            for script in scripts:
                m = pattern.match(str(script.string))
                if m:
                    equipjson = str(m.group()).split("\nvar datadetail = ")[1]
                    jo = json.loads(equipjson[1:-2], encoding="utf-8")
                    filedest = dest + "/" + str(idx) + ".json"
                    if not os.path.exists(filedest):
                        with open(filedest, "w") as fp:
                            json.dump(jo, fp)
        else:
            print("Failed to crawl equip image of " + str(idx) + " detail")

    def crawl_equip_img(self, idx, srctype, dest):
        """
        :param idx: indicates the equip card id
        :param srctype: currently should always be "A"
        :param dest: dest directory
        :return:
        """
        # print("crawling equip image of " + str(idx) + "...")
        # invalid index
        if idx <= 0:
            return
        url = self.eqimgurl + ("00" + str(idx))[-3:] + srctype + ".jpg"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            filedest = dest + ("00" + str(idx))[-3:] + "_" + srctype + ".jpg"
            if not os.path.exists(filedest):
                f = open(filedest, 'wb')
                f.write(response.content)
                f.close()
        else:
            print("failed to crawl equip image of " + str(idx))

    def crawl_equip(self, idx):
        dest = self.dest + "/equip"
        self.crawl_equip_detail(idx, dest + "/" + str(idx))
        self.crawl_equip_img(idx, "A", dest + "/" + str(idx) + "/")
        FGOCrawler.progress(FGOCrawler.count, FGOCrawler.total)

    def crawl_equip_job(self, amount):
        if not os.path.exists(self.dest + "/equip"):
            os.mkdir(self.dest + "/equip")
        for idx in range(1, amount+1):
            eqdest = self.dest + "/equip/" + str(idx) + "/"
            if not os.path.exists(eqdest):
                os.mkdir(eqdest)
        ids = list(range(1, amount+1))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            fgo = {executor.submit(self.crawl_equip, idx): idx for idx in ids}
            for _ in concurrent.futures.as_completed(fgo):
                FGOCrawler.count += 1
                FGOCrawler.progress(FGOCrawler.count, FGOCrawler.total)

    def crawl_servant_job(self):
        self.crawl_servant_name()
        FGOCrawler.total = len(self.servantnames)
        if not os.path.exists(self.dest + "/servant"):
            os.mkdir(self.dest + "/servant")
        for name in self.servantnames:
            svdest = self.dest + "/servant/" + name + "/"
            if not os.path.exists(svdest):
                os.mkdir(svdest)
        ids = list(range(1, len(self.servantnames) + 1))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            fgo = {executor.submit(self.crawl_servant, idx): idx for idx in ids}
            for _ in concurrent.futures.as_completed(fgo):
                FGOCrawler.count += 1
                FGOCrawler.progress(FGOCrawler.count, FGOCrawler.total)

    @staticmethod
    def progress(count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()


if __name__ == '__main__':
    # dest = "/Users/kankun/Documents/fgo"
    cwd = os.getcwd() + "/fgo"
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    dest = cwd
    crawler = FGOCrawler(dest)
    print("Welcome to FGO-Crawler!\n")
    while True:
        print("1. Crawl all servants")
        print("2. Crawl all equip cards")
        # print("3. Crawl a servant")
        print("3. Quit\n")
        choice = input("Input your choice (1 ~ 3): ")
        if choice == "1":
            FGOCrawler.count = 0
            crawler.crawl_servant_job()
            crawler.progress(FGOCrawler.count, FGOCrawler.total)
        elif choice == "2":
            FGOCrawler.count = 0
            # FGOCrawler.total = 811
            FGOCrawler.total = 811
            crawler.crawl_equip_job(811)
            crawler.progress(FGOCrawler.count, FGOCrawler.total)
            print("\n")
        elif choice == "3":
            print("bye~")
            exit()
