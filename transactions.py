import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import matplotlib.pyplot as plt
import plotly.express as px

def get_interval_data(r,s):
    url = "https://watcard.uwaterloo.ca/OneWeb/Financial/Transactions"
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    r = s.post(url)
    data = soup.find_all(class_="form-control date")
    lst = []
    for datum in data:
        lst.append(datum)
    
    day = custom_interval_data(400)
    lst[0]['value'] = day

    login_data = {}
    login_data['__RequestVerificationToken'] = soup.find('input',attrs={'name': '__RequestVerificationToken'})['value']
    response = s.post(url, data=login_data)
    #print(response.text)


    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://watcard.uwaterloo.ca/OneWeb/Account/LogOn")
    inputel = driver.find_element(By.ID, "Account")
    inputel.send_keys('21002985')
    inputel = driver.find_element(By.ID, "Password")
    inputel.send_keys(";)")
    inputel.submit()

    driver.get("https://watcard.uwaterloo.ca/OneWeb/Financial/Transactions")
    by_class = driver.find_element(By.ID,'trans_start_date')
    by_class.clear()
    by_class.send_keys(day)
    button_element = driver.find_element(By.ID,'trans_search')
    button_element.click()
    

    wait = WebDriverWait(driver,10)
    new = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ow-table-responsive")))
    updated_content = driver.page_source

    soup = BeautifulSoup(updated_content, 'html5lib')

    table_body = soup.find('tbody')
    rows = table_body = table_body.find_all('tr')

    data_new = []

    for row in rows:
        cells = row.find_all('td')
        date = cells[0].get_text()
        amount = cells[1].get_text()
        balance = cells[2].get_text()
        units = cells[3].get_text()
        trantype = cells[4].get_text()
        terminal = cells[5].get_text()
        data_new.append([date,amount,balance,units,trantype,terminal])

    transaction_df = pd.DataFrame(data_new,columns=['Date','Amount','Balance','Units','Trantype','Terminal'])
    print(transaction_df)
    line_chart(transaction_df)


def line_chart(df):
    df['Amount'] = df['Amount'].str.replace('[\$,]','',regex=True).astype(float)
    df = df.iloc[::-1]
    df['Running Balance'] = df['Amount'].cumsum()
    df = df.iloc[::-1]
    sub_df = df[['Date','Running Balance']].copy()
    sub_df = sub_df.iloc[::-1].reset_index(drop=True)
    print(sub_df)

    fig = px.line(sub_df,x="Date",y="Running Balance")

    st.plotly_chart(fig)


def custom_interval_data(num):
    today = datetime.datetime.now()
    d = datetime.timedelta(days=num)
    diff = today - d
    converted = diff.strftime("%Y-%m-%d")
    new = datetime.datetime.strptime(converted,"%Y-%m-%d").strftime("%m/%d/%Y")
    return new




#all features should work based on # of days user wants to see

#chart of balance history 
#mean expenditure per day (flex & meal plan) (make sure to only check negatives)
#distribution of where money is spent (type) pie chart
#2,3,4 ,7 are potential mps
#5,6,9 are flex
#times of purchases

#terminal
#show vending machine VM_BUILDING (trantype is vend (money))
#show fs FS-BUILDING (trantype is financial vend)
#show building after fs  - you frequently buy things from x,y,z

#heatmap for plotly of time purchases