import requests
import argparse
from bs4 import BeautifulSoup

from balances import basic_balance_data
from login_utils import get_login_data

def main():
    ar = argparse.ArgumentParser()
    ar.add_argument('-s', '--student_num',required=True,help="Input Student Number", type=int)
    ar.add_argument('-p', '--pwd', required=True, help="Input Watcard Password",type=str)
    args = ar.parse_args()

    url = "https://watcard.uwaterloo.ca/OneWeb/Account/LogOn"
    
    login_data = {
        'Account': args.student_num,
        'Password': args.pwd
    }

    with requests.Session() as s:
        r = s.get(url)
        login_data = get_login_data(r,url,login_data,s)
        r = s.post(url, data=login_data)
        basic_balance_data(r,s)


if __name__ == "__main__":
    main()

#TODO
#add error handling
#non-zero balances to balances.py
#detailed transaction history 
    #see where things are bought (building + store/restaurant)
#get basic personal info + contact info
#change password 
#make into a chrome extension 

    
