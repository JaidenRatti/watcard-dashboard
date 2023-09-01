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

def get_interval_data(r,s, number, password):
    url = "https://watcard.uwaterloo.ca/OneWeb/Financial/Transactions"
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    r = s.post(url)
    data = soup.find_all(class_="form-control date")
    lst = []
    for datum in data:
        lst.append(datum)
    
    day = custom_interval_data(2000)
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
    inputel.send_keys(number)
    inputel = driver.find_element(By.ID, "Password")
    inputel.send_keys(password)
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
    #print(transaction_df)
    line_chart(transaction_df)
    avg_expend(transaction_df)
    freq_locations(transaction_df)
    heatmap(transaction_df)

def line_chart(df):
    df['Amount'] = df['Amount'].str.replace('[\$,]','',regex=True).astype(float)
    df = df.iloc[::-1]
    df['Running Balance'] = df['Amount'].cumsum()
    df = df.iloc[::-1]
    sub_df = df[['Date','Running Balance']].copy()
    sub_df = sub_df.iloc[::-1].reset_index(drop=True)

    sub_df['Date'] = pd.to_datetime(sub_df['Date']).dt.strftime("%m/%d/%Y")

    fig = px.line(sub_df,x="Date",y="Running Balance")

    st.header("Running WatCard Balance :runner:")

    st.plotly_chart(fig)


def custom_interval_data(num):
    today = datetime.datetime.now()
    d = datetime.timedelta(days=num)
    diff = today - d
    converted = diff.strftime("%Y-%m-%d")
    new = datetime.datetime.strptime(converted,"%Y-%m-%d").strftime("%m/%d/%Y")
    return new


def avg_expend(df):
    #exclude the major balance transfers that waterloo adds
    negative_df = df[(df['Amount'] < 0) & (~df['Trantype'].str.startswith('136'))]
    #print(negative_df)
    mean = round(abs(negative_df['Amount'].mean()),2)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mean Daily Expenditure",f'${mean}')
    median = abs(negative_df['Amount'].median())
    with col2:
        st.metric("Median Daily Expenditure",f'${median}')
    sum = round(abs(negative_df['Amount'].sum()),2)
    with col3:
        st.metric("Total Expenditure",f'${sum}')


def freq_locations(df):
    #where you buy things from 
    filtered = df[df['Terminal'].str.extract(r':\s(FS|VM)',expand=False).notnull()]
    simplify = filtered[['Amount','Terminal']].copy()
    simplify['extract_vm'] = df['Terminal'].str.extract(r'VM_(\w+)(?:_|$)',expand=False)
    simplify['extract_fs'] = df['Terminal'].str.extract(r'FS-(\w+)',expand=False)

    simplify['Building'] = simplify['extract_vm'].fillna(simplify['extract_fs'])

    simplify.drop(['extract_vm','extract_fs','Terminal'],axis=1,inplace=True)

    simplify['Amount'] = simplify['Amount'].abs()
    simplify.loc[simplify['Building'] == 'UWP', 'Building'] += '/CMH'
    st.header("Food Spending per Building Breakdown :takeout_box:")
    st.bar_chart(simplify,x="Building",y="Amount")



def heatmap(incoming_df):
    df = incoming_df[(incoming_df['Amount'] < 0) & (~incoming_df['Trantype'].str.startswith('136'))]

    #fig = px.imshow(data,labels=dict(x="Day of Week",y="Time of Day"),
    #x=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    #y=['00','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'])
    #st.plotly_chart(fig)


    df['Date'] = pd.to_datetime(df['Date'])

    #print(df['Date'])

    df['day_of_week'] = df['Date'].dt.day_name()
    #print(df['day_of_week'])
    df['hour'] = df['Date'].dt.hour
    #midnight = 0

    grouped = df.groupby(['day_of_week','hour'])['Amount'].sum().reset_index()
    #print(grouped)

    day_index = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

    new_df = pd.DataFrame()

    for day in day_index:
        day_df = pd.DataFrame({'hour': range(24)})
        day_df['day_of_week'] = day
        merge_df = pd.merge(day_df, grouped, on=['day_of_week','hour'],how='left')

        merge_df['Amount'].fillna(0,inplace=True)
        new_df = pd.concat([new_df,merge_df],ignore_index=True)


    hourly_amount_arrays = []

    for hour in range(24):

        hour_df = new_df[new_df['hour']==hour]

        hour_amount_array = []
        for day in day_index:
            amount = abs(hour_df[hour_df['day_of_week'] == day]['Amount'].values)
            hour_amount_array.append(amount[0])

        hourly_amount_arrays.append(hour_amount_array)

    reverse = hourly_amount_arrays[::-1]
    hours = [f"{str(i).zfill(2)}:00" for i in range(23,-1,-1)]

    fig = px.imshow(reverse,labels=dict(x="day of week",y="time of day"),
    x=day_index,
    y=hours)
    st.header("Spending / Date+Time Heatmap :alarm_clock:")
    st.plotly_chart(fig, use_container_width=False,theme="streamlit")











