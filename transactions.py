import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

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

    login_data = {}
    login_data['__RequestVerificationToken'] = soup.find('input',attrs={'name': '__RequestVerificationToken'})['value']
    response = s.post(url, data=login_data)
    print(response.text)


    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://watcard.uwaterloo.ca/OneWeb/Account/LogOn")
    inputel = driver.find_element(By.ID, "Account")
    inputel.send_keys('21002985')
    inputel = driver.find_element(By.ID, "Password")
    inputel.send_keys("hehe")
    inputel.submit()

    driver.get("https://watcard.uwaterloo.ca/OneWeb/Financial/Transactions")
    by_class = driver.find_element(By.ID,'trans_start_date')
    by_class.clear()
    by_class.send_keys(day)
    button_element = driver.find_element(By.ID,'trans_search')
    button_element.click()
    updated_content = driver.page_source
    print(updated_content)

    #keep tab open for long enough
    


def custom_interval_data(num):
    today = datetime.datetime.now()
    d = datetime.timedelta(days=num)
    diff = today - d
    converted = diff.strftime("%Y-%m-%d")
    new = datetime.datetime.strptime(converted,"%Y-%m-%d").strftime("%m/%d/%Y")
    return new

