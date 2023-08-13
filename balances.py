import requests
from bs4 import BeautifulSoup

def basic_balance_data(r,s):
    r = s.get("https://watcard.uwaterloo.ca/OneWeb/Financial/Balances")
    soup = BeautifulSoup(r.content, 'html5lib')
    balance_data = soup.find_all(class_="pull-right")
    for element in balance_data:
        data = element.get_text()
        print("WatCard Balance ",data)
