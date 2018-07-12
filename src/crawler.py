import requests
from bs4 import BeautifulSoup
import os
import re
import json
import sys
#from multiprocessing import Pool as ThreadPool
import threading
import time


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
        self.servantlist = []

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


    def crawl_servant(self):
        # first get all servant names
        self.crawl_servant_name()
        idx = 1
        for name in self.servantlist:
            self.crawl_servant(idx)
            idx += 1

    def crawl_servant(self, idx):
        if len(self.servantlist) > 0 and idx <= len(self.servantlist):
            name = self.servantlist[idx]
            for srctype in "ABCDE":
                self.crawl_servant_detail(idx, self.dest + "/" + name + "/")
                # crawl servant image
                self.crawl_servant_img(idx, srctype, self.dest + "/" + name + "/img/")
                # crawl noble phantasm video
                self.crawl_noble_phantasm_video(idx, self.dest + "/" + name + "/video/")
        FGOCrawler.count += 1

    # TODO
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
        print("crawling the image of servant " + self.servantlist[idx] + "...")
        # invalid index
        if idx <= 0:
            return
        url = self.svimgurl + ("00" + str(idx))[-3:] + srctype + ".jpg"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            destfolder = dest + ("00" + str(idx))[-3:] + "_" + srctype + ".jpg"
            if not os.path.exists(destfolder):
                f = open(destfolder, 'wb')
                f.write(response.content)
                f.close()
        else:
            print("failed to crawl the image of servant " + self.servantlist[idx])

    def crawl_noble_phantasm_video(self, idx, dest):
        """
        :param idx: indicates the servant id
        :param dest: dest directory
        :return:
        """
        print("crawling the video of servant " + self.servantlist[idx] + "...")
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
            print("failed to crawl the video of servant " + self.servantlist[idx])

    def crawl_servant_name(self):
        print("crawling the names of all servants...")
        response = requests.get(self.svdetailurl, headers=self.header)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, "html.parser")
            servants = soup.find('select', class_='pet').find_all('option')
            for servant in servants[1:]:
                self.servantlist.append(str(servant.get_text()))
                FGOCrawler.total += 1
            for servant in self.servantlist:
                self.servantdir(servant, self.dest + "/servant")
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
        print("crawling equip image of " + str(idx) + " detail...")
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
                    if not os.path.exists(dest + ".json"):
                        with open(dest + ".json", "w") as fp:
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
        if not os.path.exists(dest):
            os.mkdir(dest)
        url = self.eqimgurl + ("00" + str(idx))[-3:] + srctype + ".jpg"
        response = requests.get(url, headers=self.header)
        if response.status_code == 200:
            destfile = dest + ("00" + str(idx))[-3:] + "_" + srctype + ".jpg"
            if not os.path.exists(destfile):
                f = open(destfile, 'wb')
                f.write(response.content)
                f.close()
        else:
            print("failed to crawl equip image of " + str(idx))

        FGOCrawler.count += 1
        self.progress(FGOCrawler.count, FGOCrawler.total)

    def crawl_equip(self, amount):
        FGOCrawler.total += amount
        dest = self.dest + "/equip"
        if not os.path.exists(dest):
            os.mkdir(dest)
        for idx in range(1, amount):
            eqdest = self.dest + "/equip/" + str(idx) + "/"
            if not os.path.exists(eqdest):
                    os.mkdir(eqdest)
            self.crawl_equip_detail(idx, dest + str(idx) + "/" + str(idx))
            self.crawl_equip_img(idx, "A", dest + str(idx) + "/" + str(idx))
            FGOCrawler.count += 1

    def progress(self, count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()

if __name__ == '__main__':
    dest = "/Users/kankun/Documents/fgo/"
    crawler = FGOCrawler(dest)
    print("Welcome to FGO-Crawler!\n")
    # print("1. Crawl all servants")
    # print("2. Crawl all equip cards")
    # choice = input("Input your choice (1 or 2): ")
    # print(choice)

    # make the Pool of workers
    # pool = ThreadPool(10)

    # open the urls in their own threads
    # and return the result
    if not os.path.exists(dest + "equip/"):
        os.mkdir(dest + "equip/")

    FGOCrawler.total = 20
    thread_list = []
    for idx in range(10, 30):
        # Instantiates the thread
        # (i) does not make a sequence, so (i,)
        t = threading.Thread(target=crawler.crawl_equip_img,
                             args=(idx, "A", dest + "equip/" + str(idx) + "/"))
        # Sticks the thread in a list so that it remains accessible
        thread_list.append(t)

        #crawler.crawl_equip_img(idx, "A", dest + "equip/"+ str(idx) + "/")
        #crawler.count += 1
        # pool.apply(crawler.progress, (crawler.count, crawler.total))
        # pool.apply(crawler.crawl_equip_img, (idx, "A", dest + "equip/" + str(idx) + "/"))

    # Starts threads
    for thread in thread_list:
        thread.start()

    # This blocks the calling thread until the thread whose join() method is called is terminated.
    # From http://docs.python.org/2/library/threading.html#thread-objects
    for thread in thread_list:
        thread.join()

    crawler.progress(FGOCrawler.count, FGOCrawler.total)

    # close the pool and wait for the work to finish
    # pool.close()
    # pool.join()

    # try:
    #     beforeBegin(classNum=4)
    #     lock.acquire()
    #     for i in range(1, 75):
    #         t = threading.Thread(target=getMaterial, args=(i,))
    #         t.start()
    #
    #     for i in range(1, 150):
    #         t = threading.Thread(target=getHero, args=(i,))
    #         t.start()
    # finally:
    #     quitAllClass()