#-*- coding:utf-8  -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import StringIO
from bs4 import BeautifulSoup
from PIL import Image
import urllib2

driver = webdriver.Firefox()
driver.get("http://bbs.byr.cn/index")
driver.find_element_by_xpath('//input[@name="id"]').send_keys('GentlyGuitar')
driver.find_element_by_xpath('//input[@name="passwd"]').send_keys('123456')
driver.get_screenshot_as_file('show.png')
driver.find_element_by_xpath('//form[@id="f_login"]').submit()#questions
time.sleep(2)

pagePointer = 0
globalCount = 0

while pagePointer <=179:
    pagePointer += 1
    print pagePointer
    currentUrl = "http://bbs.byr.cn/board/Friends?p="+str(pagePointer)
    driver.get(currentUrl)
    driver.get_screenshot_as_file('show.png')
    soup=BeautifulSoup(driver.page_source)

    all = soup.find_all('tr')
    for each in all:
        if each.contents[1] != None:
            title = each.contents[1].get_text()
            if title.find(u'王道')!=-1 or title.find(u'照片')!=-1:
                link = each.contents[1].contents[0]['href']
                articlUrl='http://bbs.byr.cn'+link
                driver.get(articlUrl)
                driver.get_screenshot_as_file('show.png')
                soup=BeautifulSoup(driver.page_source)
                allImg=soup.find_all('img')
                allImg=soup.find_all(attrs={'title':True, 'alt':True})
                for each in allImg:
                    imgUrl = 'http://bbs.byr.cn'+each['src']
                    try:
                        imgString=urllib2.urlopen(imgUrl).read()
                        im = Image.open(StringIO.StringIO(imgString))
                    except:
                        continue

                    imgPath='/home/fiona/beiyou/photo/'+str(globalCount)+"_"+each['title']
                    globalCount+=1

                    im.save(imgPath)

driver.quit()





