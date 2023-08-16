import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_interval_data(r,s):
    url = "https://watcard.uwaterloo.ca/OneWeb/Financial/Transactions"
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    r = s.post(url)
    data = soup.find_all(class_="form-control date")
    lst = []
    for datum in data:
        lst.append(datum)
    
    day = custom_interval_data(200)
    lst[0]['value'] = day
    print(data)

    
    driver = webdriver.Chrome()

    driver.get("https://watcard.uwaterloo.ca/OneWeb/Account/LogOn")
    inputel = driver.find_element(By.ID, "Account")
    inputel.send_keys('21002985')
    inputel = driver.find_element(By.ID, "Password")
    inputel.send_keys("ma12vr21UW!!")
    inputel.submit()

    driver.get("https://watcard.uwaterloo.ca/OneWeb/Financial/Transactions")
    button = driver.find_element(By.ID, "trans_search")
    button.click()

    #button_element = driver.find_element('class','btn ow-btn-primary btn-block-xs pull-right')
    #button_element.click()
    updated_content = driver.page_source
    print(updated_content)
    



def custom_interval_data(num):
    today = datetime.datetime.now()
    d = datetime.timedelta(days=num)
    diff = today - d
    converted = diff.strftime("%Y-%m-%d")
    new = datetime.datetime.strptime(converted,"%Y-%m-%d").strftime("%m/%d/%Y")
    return new

