import requests
import argparse
from bs4 import BeautifulSoup
import pandas as pd

from balances import basic_balance_data, full_balance_data
from login_utils import get_login_data, get_personal_info
from password import changepwd

def get_user_input():
    ar = argparse.ArgumentParser()
    ar.add_argument('-s', '--student_num',required=True,help="Input Student Number", type=int)
    ar.add_argument('-p', '--pwd', required=True, help="Input Watcard Password",type=str)
    args = ar.parse_args()
    return args

def main():
    args = get_user_input()
    url = "https://watcard.uwaterloo.ca/OneWeb/Account/LogOn"
    login_data = {
        'Account': args.student_num,
        'Password': args.pwd
    }

    with requests.Session() as s:
        r = s.get(url)
        login_data = get_login_data(r,url,login_data,s)
        r = s.post(url, data=login_data)
        personal_info = get_personal_info(r,s)
    print(personal_info)
    bal = basic_balance_data(r,s)
    print(bal)
    detail_bal = full_balance_data(r,s)
    print(detail_bal)
    #confirmation = changepwd(r,s,args.pwd)
    #print(confirmation)
    

    


if __name__ == "__main__":
    main()

#TODO
#detailed transaction history 
    #see where things are bought (building + store/restaurant)
#connect to frontend using streamlit

    
