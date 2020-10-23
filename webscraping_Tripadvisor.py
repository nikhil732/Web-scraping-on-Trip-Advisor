from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from re import findall,sub
from lxml import html
from time import sleep
import requests
import urllib.request
import bs4
import pandas as pd
PATH= "C:\Program Files (x86)\chromedriver.exe"


def parse(url):
    searchKey = "New Delhi" # Change this to your city 
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    element = driver.find_element_by_link_text("Hotels")
    element.click()
    sleep(5)
    search_bar = driver.find_element_by_css_selector("input[placeholder='Where to?']")
    search_bar.send_keys("New Delhi")
    search_bar.send_keys(Keys.RETURN)
    sleep(10)
    element=driver.find_element_by_xpath('//*[@id="search-filters"]/ul/li[2]/a')
    element.click()
    sleep(15)
    man=driver.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div')
    s=man.text
    s=s.split("\n")
    name_rev=[]
    for i in range(0,len(s),6):
        name_rev.append([s[i+1],s[i+2]])
    sleep(5)
    df = pd.DataFrame(name_rev, columns = ['Hotel Name', 'Reviews'])
    df.to_csv('CSV_DATA.csv')
    for i in range(33):
        names_revs=[]
        lik=driver.find_element_by_link_text('Next')
        lik.click()
        sleep(5)
        man=driver.find_element_by_xpath('//*[@id="BODY_BLOCK_JQUERY_REFLOW"]/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div')
        # print(man.text)
        s=man.text
        s=s.split("\n")
        # print(s)
        print(len(s))
        p=[]
        for j in range(len(s)):
            # print(s[j])
            if s[j]=='Hotels':
                p.append(s[j+1])
                # print(s[j+1])
            try:
                if s[j].split(" ")[1]=='reviews':
                    p.append(s[j])
            except:
                continue
        # print(len(p))
        if len(p)%2!=0:
            for i in range(0,len(p)-1,2):
                names_revs.append([p[i],p[i+1]])
        else:
            for i in range(0,len(p),2):
                names_revs.append([p[i],p[i+1]])
        df=pd.read_csv("CSV_DATA.csv")
        df1 = pd.DataFrame(names_revs, columns = ['Hotel Name', 'Reviews'])
        df=pd.concat([df,df1])
        df.append(df1,ignore_index=True)
        df.to_csv("CSV_DATA.csv")
            name_rev.append(p)
        sleep(3)


parse('https://www.tripadvisor.com/')