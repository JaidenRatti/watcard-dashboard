import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

def basic_balance_data(r,s):
    r = s.get("https://watcard.uwaterloo.ca/OneWeb/Financial/Balances")
    soup = BeautifulSoup(r.content, 'html5lib')
    balance_data = soup.find(class_="pull-right")
    return balance_data.get_text()

def full_balance_data(r,s):
    r = s.get("https://watcard.uwaterloo.ca/OneWeb/Financial/Balances")
    soup = BeautifulSoup(r.content, 'html5lib')
    balance_data = soup.find_all(class_="ow-align-right")
    data = []
    for elem in balance_data:
        elem_text = elem.get_text()
        data.append(elem_text)
    pairs_list = []
    
    for i in range(0, len(data), 2):
        pair = [data[i], data[i+1]]
        pairs_list.append(pair)

    temp = ['','Residence Plan','Super Saver MP','Saver MP','Casual MP','Flexible ','Flexible','Transfer MP','Dons Meal Allow','Dons Flex','Unallocated','Dept Charge','Overdraft']
    #just for now since parsing this is strange
    name_dict = dict(zip(temp, pairs_list))
    df = pd.DataFrame.from_dict(name_dict,orient="index")
    df.columns =df.iloc[0]
    df = df[1:]
    return df


def pie_chart(df):
    df['Amount'] = df['Amount'].str.replace('[\$,]','',regex=True).astype(float)
    mp = df['Amount'][0] + df['Amount'][1] + df['Amount'][2] + df['Amount'][3] + df['Amount'][6]
    flex = df['Amount'][4] + df['Amount'][5] + df['Amount'][8]
    values = [mp,flex]
    names = 'Meal Plan','Flex'
    fig = px.pie(values=values,names=names)
    st.header("Meal Plan vs Flex :pie:")
    st.plotly_chart(fig,theme="streamlit")