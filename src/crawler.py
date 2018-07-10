#coding=utf-8
import requests
from bs4 import BeautifulSoup
# from CrawlerLog import *
import os
from time import sleep
import random
import re
import json

# default parameter
picturePath = 'D:/Crawler/FGO/picture_hero/'
videoPath = 'D:/Crawler/FGO/video/'
mycodePath = 'D:/Crawler/FGO/picture_mycode/'
heroPath = 'D:/Crawler/FGO/FGO Hero/'
mycodeDataPath = 'D:/Crawler/FGO/FGO Mystic Code/'
logDirectory = r'D:/Crawler/FGO/log/'


####### 程序开始 #######
traceOn = True
basedUrlHero = 'http://fgowiki.com/guide/petdetail/'
basedUrlMysticCode = 'http://fgowiki.com/guide/equipdetail/'

if(not os.path.exists(logDirectory)):
    os.makedirs(logDirectory)
    if (traceOn): print("Created - " + logDirectory)
if(not os.path.exists(picturePath)):
    os.makedirs(picturePath)
    if (traceOn): print("Created - " + picturePath)
if(not os.path.exists(videoPath)):
    os.makedirs(videoPath)
    if (traceOn): print("Created - " + videoPath)

if (traceOn): print("PictureCrawler for: " + basedUrlHero)

# header - 防止防盗链
header = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://fgowiki.com/guide/petdetail/'
}


def getFormattedIndexString(index):
    maxLen = 3
    rev = str(index)
    ilen = len(str(index))
    if(ilen < 1 or ilen > 3):
        return None

    for i in range(0, maxLen-ilen):
        rev = '0' + rev
    return rev


def crawlFGOPicture(heroList, imgType = 'A'):
    # crawling the pictures
    # img.fgowiki.com/fgo/card/servant/002A.jpg
    imgUrl = 'http://img.fgowiki.com/fgo/card/servant/'

    for heroIndex in range(1, len(heroList)+1):
        cardUrl = imgUrl + getFormattedIndexString(heroIndex) + imgType + '.jpg'
        imgHtml = requests.get(cardUrl, headers=header)

        savedFilePath = picturePath + str(heroIndex) + "_" + imgType + ".jpg"
        f = open(savedFilePath, 'wb')
        f.write(imgHtml.content)
        f.close()

        sleep(random.randint(1, 10) * 0.01)
        print("Crawling - " + cardUrl + " done.")


def crawlFGOVideo(heroList):
    # crawling the videos
    # img.fgowiki.com/fgo/card/servant/002A.jpg
    logObject = CrawlerLog(logDirectory + 'video.log')
    videoBasedUrl = 'http://img.fgowiki.com/fgo/mp4/'

    for heroIndex in range(1, len(heroList)+1):
        videoUrl = videoBasedUrl + 'No.' + getFormattedIndexString(heroIndex) + '.mp4'
        if(logObject.checkTargetIn(videoUrl)):
            print("Repeated video - " + videoUrl)
            continue

        print("Crawling new video - " + videoUrl)
        imgHtml = requests.get(videoUrl, headers=header)
        if (imgHtml.status_code != 200):
            # if respond code is not 200 -> pass
            print('invalid video - ' + videoUrl)
            continue

        savedFilePath = videoPath + str(heroIndex) + ".mp4"
        f = open(savedFilePath, 'wb')
        f.write(imgHtml.content)
        f.close()

        sleep(random.randint(1, 10) * 0.01)
        print("Crawling - " + videoUrl + " done.")
        logObject.addNewEntry(videoUrl)


def crawlFGOHeroData(heroList):
    heroLogPath = logDirectory + 'hero.log'
    heroListFilePath = heroPath + 'HeroList.txt'
    if(not os.path.exists(heroLogPath)): # if there is no log -> initialize the output file
        if(os.path.exists(heroListFilePath)):
            os.remove(heroListFilePath)
            print('Initialized the output file.')

    logObject = CrawlerLog(heroLogPath)
    # 0 and 1 are both 玛修, start from 1
    for heroIndex in range(0, len(heroList)):
        heroPageUrl = basedUrlHero + str(heroIndex + 1) # start from 1! NOT 0
        if(logObject.checkTargetIn(heroPageUrl)): # check repeating data
            print("Repeated Hero - No." + str(heroIndex+1) + ' ' + heroList[heroIndex])
            continue

        print("Getting data for New Hero - No." + str(heroIndex+1) + ' ' + heroList[heroIndex])
        print(heroPageUrl)
        pageHtml = requests.get(heroPageUrl, headers=header)
        '''
       Attention: 
       re.match only match the string ONLY from text BEGINNING, 
       re.search match the string from every char
       regular expresss to get JSON data ->  r'\[{\"ID\"(.*?)}\]'
       '''
        jsonData = re.search('\[{\"ID\"(.*?)}\];', pageHtml.text)
        #print(pageHtml.text)
        if(jsonData):
            jsonString = jsonData.group()[:-1]
            #if(traceOn): print(jsonString + " Found.")
            heroDict = json.loads(jsonString) # get dictionary of Json
            #for key in heroDict[0]: print(key),
            separator = '###'
            writeText = str(heroIndex) + separator + str(heroDict[0]['NAME']) + \
                        separator + str(heroDict[0]['CLASS']) + separator + str(heroDict[0]['STAR']) + separator + str(heroDict[0]['Gender'])\
                        + separator + str(heroDict[0]['ILLUST']) + separator + str(heroDict[0]['Property'])
            if(traceOn): print(writeText)

            #output the result
            f = open(heroListFilePath, 'a')
            f.write(writeText + '\n')
            f.close()
            print("Hero No." + str(heroIndex+1) + " downloaded.")
            # save in log
            logObject.addNewEntry(heroPageUrl)


def crawlFGOMyCode(imgType):
    logObject = CrawlerLog(logDirectory + 'mycode.log')
    basedUrlMyCode = 'http://img.fgowiki.com/fgo/card/equip/'
    for codeIndex in range(0, 10000): # up to 10000 cards so far
        # index start from 1
        codeUrl = basedUrlMyCode + getFormattedIndexString(codeIndex+1) + imgType + '.jpg'
        if(logObject.checkTargetIn(codeUrl)):
            print('Repeated Mystic Code - ' + codeUrl)
            continue

        mycodeHtml = requests.get(codeUrl, headers=header)
        if(mycodeHtml.status_code != 200):
            # if respond code is not 200 -> exit (usually no new cards get)
            print('Finished, totally get ' + str(codeIndex+1) + ' cards.')
            return codeIndex+1

        savedFilePath = mycodePath + str(codeIndex+1) + ".jpg"
        f = open(savedFilePath, 'wb')
        f.write(mycodeHtml.content)
        f.close()

        sleep(random.randint(1, 10) * 0.01)
        print("Crawling - " + codeUrl + " done.")
        logObject.addNewEntry(codeUrl)


def crawlFGOMyCodeData(maxNo):
    myCodeLogPath = logDirectory + 'mycode(data).log'
    mycodeListFilePath = mycodeDataPath + 'MysticCodeList.txt'
    if (not os.path.exists(myCodeLogPath)):  # if there is no log -> initialize the output file
        if (os.path.exists(mycodeListFilePath)):
            os.remove(mycodeListFilePath)
            print('Initialized the output file.')

    logObject = CrawlerLog(myCodeLogPath)
    # start from 1
    for codeIndex in range(1, maxNo):
        mycodePageUrl = basedUrlMysticCode + str(codeIndex)  # start from 1!
        if (logObject.checkTargetIn(mycodePageUrl)):  # check repeating data
            print("Repeated Mystic Code - No." + str(codeIndex))
            continue

        print("Getting data for New Mystic Code - No." + str(codeIndex))
        print('downloading - ' + mycodePageUrl)
        pageHtml = requests.get(mycodePageUrl, headers=header)
        '''
       Attention: 
       re.match only match the string ONLY from text BEGINNING, 
       re.search match the string from every char
       regular expresss to get JSON data ->  r'\[{\"ID\"(.*?)}\]'
       '''
        jsonData = re.search('\[{\"ID\"(.*?)}\];', pageHtml.text)
        # print(pageHtml.text)
        if (jsonData):
            jsonString = jsonData.group()[:-1] # get last matching object
            heroDict = json.loads(jsonString)  # get dictionary of Json
            # for key in heroDict[0]: print(key),
            separator = '###'
            writeText = str(heroDict[0]['ID']) + separator + str(heroDict[0]['NAME_CN']) + \
                        separator + str(heroDict[0]['STAR']) + separator + str(heroDict[0]['SKILL_E']).replace('\n', '') + \
                        separator + str(heroDict[0]['SKILLMAX_E']).replace('\n', '') + separator + \
                        str(heroDict[0]['INTRO']).replace('\n', '')
            if (traceOn): print(writeText)

            # output the result
            f = open(mycodeListFilePath, 'a')
            f.write(writeText + '\n')
            f.close()
            print("Hero No." + str(codeIndex) + " downloaded.")
            # save in log
            logObject.addNewEntry(mycodePageUrl)

    return


def crawlFGO():
    heroList = []
    html = requests.get(basedUrlHero, headers=header)
    soup = BeautifulSoup(html.text, "html.parser")  # parse this page
    allLabelA = soup.find('select', class_='pet').find_all('option')  # get list of results
    html.encoding = 'utf-8'

    for labelA in allLabelA:
        hero = labelA.get_text()  # 提取 图片主题 的 文本描述
        if (hero == ''):
            continue
        # if(traceOn): print (hero + "/")
        heroList.append(str(hero))

    sleep(random.randint(1, 10) * 0.01)
    print("共有英灵总数 - " + str(len(heroList)))

    #1 crawling hero data
    #crawlFGOHeroData(heroList)

    #2 crawling hero pictures
    ''' 
    图片索引字母imgType
        A - 1破
        B - 2破
        C - 3破
        D - 4破
        E - 愚人节  
     '''
    #crawlFGOPicture(heroList, 'C')

    #3 crawling hero final skills videos
    crawlFGOVideo(heroList)

    #4 crawling mystic code cards picture
    #mycodeMaxNo = crawlFGOMyCode('A')

    #5 crawling mystic code data data
    #crawlFGOMyCodeData(int(mycodeMaxNo))


if( __name__ == "__main__"):
    # main function
    crawlFGO()
