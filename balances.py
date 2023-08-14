import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    for meep in balance_data:
        j = meep.get_text()
        data.append(j)
    pairs_list = []
    
    for i in range(0, len(data), 2):
        pair = [data[i], data[i+1]]
        pairs_list.append(pair)

    temp = ['Residence Plan','Super Saver MP','Saver MP','Casual MP','Flexible','Flexible','Transfer MP','Dons Meal Allow','Dons Flex','Unallocated','Dept Charge','Overdraft']
    #just for now since parsing this is strange
    name_dict = dict(zip(temp, pairs_list))
    return pd.DataFrame.from_dict(name_dict, orient='index')
    

