from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import os
import requests

options = Options()
options.add_argument("--disable-notifications")
# * 上兩行用來取消網頁中的彈出視窗 避免妨礙網路爬蟲的執行
# options.add_argument('headless') #* 不跳出視窗
options.add_argument("--start-maximized")     #最大化視窗
options.add_argument("--incognito")           #開啟無痕模式

chrome = webdriver.Chrome('./chromedriver', chrome_options=options)

chrome.get('https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx')

email = chrome.find_element_by_name('Txt_UserID')
password = chrome.find_element_by_name('Txt_Password')
signIn= chrome.find_element_by_name('ibnSubmit')

email.send_keys('') #Portal帳號
password.send_keys('') #Portal密碼
signIn.click()

time.sleep(2)
# 判断是否有弹出框
def alert_is_present(driver):
    try:
        alert = driver.switch_to.alert
        alert.text
        return alert
    except:
        return False

# 如果有弹出框 点击确定
if alert_is_present(chrome):
    chrome.switch_to.alert.accept()

time.sleep(2)
chrome.get('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/IFrameRight.aspx')
time.sleep(2)
chrome.switch_to.frame(0)
print(chrome.page_source)
soup = BeautifulSoup(chrome.page_source, 'html.parser')

sels = soup.select('td a')

# print(sels)

allQuest=[]
for sel in sels:#<a href:>
    if(sel['href'].startswith('F02_QuestionnaireDetail') and (sel['href'] not in allQuest)):
        allQuest.append(sel['href'])

oldPortal='https://portal.yzu.edu.tw/NewSurvey/std/'

for quest in allQuest:
    chrome.get(oldPortal+quest)
    time.sleep(2)
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    sels = soup.select('table')
    print(sels)
    for sel in sels:
        try:
            id=sel['id']
            button=chrome.find_element_by_id(id+"_0")
            button.click()
        except:
            continue
    finish=chrome.find_element_by_id('btOK')
    finish.click()
    # 如果有弹出框 点击确定 
    if alert_is_present(chrome):
        chrome.switch_to.alert.accept()

print('finish')