import requests
from bs4 import BeautifulSoup
import os
import re
import json

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


# crawl_video(2, "N", "../data/阿尔托莉雅·潘德拉贡/video/")

# datadetail = [{"ID":"811","NAME_CN":"\u67d0\u5ea7\u5c71\u4e0a\u53d1\u751f\u7684\u4e8b","NAME_JP":"\u3068\u3042\u308b\u5c71\u3067\u306e\u51fa\u6765\u4e8b","NAME":"","HEAD1":"811C.png","PIC1":"811A.png","PIC2":"811B.png","Avatar":"811","STAR":"4","LV1_HP":"100","LV1_ATK":"100","LVMAX_HP":"100","LVMAX_ATK":"100","COST":"9","ILLUST":"\u2014\u2014","CV":None
#                   ,"ICO":"305.png","SKILL_E":"\u53ea\u6709\u5742\u672c\u9f99\u9a6c(Rider)\u88c5\u5907\u65f6\uff0c\u81ea\u8eab\u5728\u573a\u671f\u95f4\uff0c\u5df1\u65b9\u5168\u4f53\u7684Arts\u5361\u6027\u80fd\u63d0\u534710% & \u5b9d\u5177\u5a01\u529b\u63d0\u534715%","SKILLMAX_E":"\u2014\u2014","INTRO":"\u2015\u2015\u2015\u6700\u521d\u6211\u672c\u60f3\u9a97\u4ed6\u7136\u540e\u518d\u628a\u4ed6\u5403\u6389\u3002\n\n\u6211\u601d\u8003\u7740\u5982\u4f55\u6b3a\u9a97\u90a3\u4e2a\u770b\u4e0a\u53bb\u50bb\u4e4e\u4e4e\u7684\u4eba\u7c7b\uff0c\u8ba9\u4ed6\u628a\u90a3\u4e2a\u4ee4\u4eba\u538c\u6076\u7684\u5c01\u5370\u77db\u62d4\u6389\u540e\uff0c\u518d\u4e00\u53e3\u5403\u6389\u4ed6\u3002\u4f46\u662f\u90a3\u4e2a\u4eba\u7c7b\u5b8c\u5168\u6ca1\u6709\u542c\u6211\u7684\u89e3\u91ca\uff0c\u76f4\u63a5\u6293\u4f4f\u77db\u5e76\u6beb\u65e0\u987e\u8651\u5730\u62d4\u4e86\u51fa\u6765\u3002\n\n\u5bf9\u7740\u4e00\u5fc3\u60f3\u8981\u5411\u90a3\u5e2e\u5c01\u5370\u6211\u7684\u8ba8\u538c\u7684\u5bb6\u4f19\u62a5\u4ec7\u96ea\u6068\u800c\u4e0d\u65ad\u82df\u6d3b\u7740\u7684\u6211\uff0c\u90a3\u4e2a\u4eba\u7c7b\u5c45\u7136\u53ea\u8bf4\u4e86\u300c\u90a3\u5bb6\u4f19\u6216\u8bb8\u4e5f\u5f88\u8f9b\u82e6\u5427\u300d\u8fd9\u79cd\u65e0\u6240\u8c13\u7684\u8bdd\uff0c\u5c31\u4e0b\u5c71\u4e86\u3002\n\n\u90a3\u4e2a\u4eba\u7c7b\u5e26\u7740\u4e00\u526f\u4e00\u5207\u90fd\u65e0\u6240\u8c13\u7684\u8868\u60c5\uff0c\u6240\u4ee5\u6211\u4e5f\u89c9\u5f97\u597d\u4f3c\u4ec0\u4e48\u90fd\u6ca1\u53d1\u751f\u4e00\u6837\uff0c\u5bf9\u90a3\u5e2e\u8ba8\u538c\u7684\u5bb6\u4f19\u7684\u6df1\u6df1\u7684\u4ec7\u6068\u4e5f\u5728\u4e00\u77ac\u95f4\u5fd8\u5f97\u4e00\u5e72\u4e8c\u51c0\u3002\n\n\u8fd9\u4e48\u4e00\u60f3\u7684\u8bdd\uff0c\u90a3\u4e2a\u4eba\u7c7b\u4e4b\u6240\u4ee5\u80fd\u6446\u51fa\u4e00\u526f\u65e0\u6240\u8c13\u7684\u8868\u60c5\uff0c\u662f\u56e0\u4e3a\u89c9\u5f97\u6211\u4e5f\u4e0d\u7b97\u4ec0\u4e48\u5427\u3002\n\n\u4e8e\u662f\u6211\u5c31\u628a\u60f3\u5403\u4e86\u4ed6\u7684\u76ee\u7684\u7ed9\u5fd8\u6389\u4e86\uff0c\u76f4\u63a5\u53bb\u8ffd\u968f\u90a3\u4e2a\u4eba\u7c7b\u4e86\u3002\n\n\u8fd9\u5c31\u662f\u67d0\u5ea7\u5c71\u4e0a\u53d1\u751f\u7684\u4e8b\u3002"}]
# print(datadetail)

response = requests.get("https://fgowiki.com/guide/equipdetail/811", headers=header)
response.encoding = "utf-8"
soup = BeautifulSoup(response.content, "html.parser")
scripts = soup.find_all("script")
pattern = re.compile("\nvar datadetail = (.*?);")
for script in scripts:
    m = pattern.match(str(script.string))
    if m:
        equipjson = str(m.group()).split("\nvar datadetail = ")[1]
        print(equipjson)
