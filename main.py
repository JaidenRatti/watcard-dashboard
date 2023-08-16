import requests
import argparse
from bs4 import BeautifulSoup
import pandas as pd

from balances import basic_balance_data, full_balance_data
from login_utils import get_user_input, login, get_login_data, get_personal_info
from password import changepwd


def display_results(personal_info,r,s):
    print(personal_info)
    bal = basic_balance_data(r,s)
    print(bal)
    detail_bal = full_balance_data(r,s)
    print(detail_bal)
    #confirmation = changepwd(r,s,args.pwd)
    #print(confirmation)

def main():
    while True:
        args = get_user_input()
        personal_info,r,s = login(args)

        if personal_info == 0:
            #since status code is not reliable
            print("Login Info Invalid. Restarting")
            break
        else:
            print("Success!")
        display_results(personal_info,r,s)
        break
        

if __name__ == "__main__":
    main()

#TODO
#detailed transaction history 
    #see where things are bought (building + store/restaurant)
#connect to frontend using streamlit

    
