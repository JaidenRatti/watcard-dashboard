import requests
import argparse
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from PIL import Image

from balances import basic_balance_data, full_balance_data
from login_utils import get_user_input, login
from password import changepwd
from transactions import get_interval_data



def display_results(personal_info,r,s):
    formatted = f":bust_in_silhouette: {personal_info['Name']}, 	:email: {personal_info['Email']}"
    st.divider()
    st.write(formatted)
    bal = basic_balance_data(r,s)
    st.metric("WatCard Balance :dollar:",bal)
    detail_bal = full_balance_data(r,s)
    detail_bal.T
    #confirmation = changepwd(r,s,args.pwd)
    #print(confirmation)
    #starter = get_interval_data(r,s)

def main():
    image = Image.open('logo.png')
    st.image(image)
    st.title("WatCard Dashboard")
    while True:
        number = st.text_input("Enter Student Number")
        password = st.text_input("Enter Password",type="password")
        result = st.button("Enter")
        if result:
            personal_info,r,s = login(number,password)
            if personal_info == 0:
            #since status code is not reliable
                st.header("Login Info Invalid. Try Again")
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

    
