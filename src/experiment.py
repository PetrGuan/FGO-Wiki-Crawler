import requests
from bs4 import BeautifulSoup
import os

header = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://fgowiki.com/guide/petdetail/'
}

# basedUrlHero = "http://fgowiki.com/guide/petdetail/"
# htmlResponse = requests.get(basedUrlHero, headers=header)
# htmlResponse.encoding = 'utf-8'
# soup = BeautifulSoup(htmlResponse.content, "html.parser")  # parse this page
# servants = soup.find('select', class_='pet').find_all('option')  # get list of results
# servantList = []
# for servant in servants:
#     servantList.append(servant.get_text)

# since the servant page is like "http://fgowiki.com/guide/petdetail/0...1"

servantlist = []

def crawl_servant(baseurl="http://fgowiki.com/guide/petdetail/"):
    response = requests.get(baseurl, headers=header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, "html.parser")
    servants = soup.find('select', class_='pet').find_all('option')
    for servant in servants[1:]:
        servantlist.append(str(servant.get_text()))
    mkdir(servantlist)


def crawl_img(idx, srctype, dest, baseurl="http://img.fgowiki.com/fgo/card/servant/"):
    # invalid index
    if idx <= 0:
        return
    url = baseurl + ("00" + str(idx))[-3:] + srctype + ".jpg"
    print(url)
    response = requests.get(url, headers=header)
    f = open(dest + ("00" + str(idx))[-3:] + "_" + srctype + ".jpg", 'wb')
    f.write(response.content)
    f.close()


def crawl_video(idx, srctype, dest, baseurl="http://img.fgowiki.com/fgo/mp4/"):
    # invalid index
    if idx <= 0:
        return
    url = baseurl + "No." + ("00" + str(idx))[-3:] + srctype + ".mp4"
    print(url)
    response = requests.get(url, headers=header)
    f = open(dest + "No." + ("00" + str(idx))[-3:] + "_" + srctype + ".mp4", 'wb')
    f.write(response.content)
    f.close()


def mkdir(servants):
    dest = "../data"
    if not os.path.exists(dest):
        os.mkdir(dest)
    for name in servants:
        svdest = dest + "/" + name
        print(svdest)
        if not os.path.exists(svdest):
            os.mkdir(svdest)
        imgdest = svdest + "/img"
        if not os.path.exists(imgdest):
            os.mkdir(imgdest)
        videodest = svdest + "/video"
        if not os.path.exists(videodest):
            os.mkdir(videodest)


def test_crawl_img():
    crawl_img(1, "A", "../data/玛修·基列莱特/img/")


crawl_video(2, "N", "../data/阿尔托莉雅·潘德拉贡/video/")
